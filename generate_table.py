import pandas as pd
import sqlalchemy
import json

# import data from animelist to tables:
#           producer, licensor, studio, genres, relation
#           animelist_producer, animelist_licensor, animelist_studio, animelist_genres
#  and create .csv files to */csv/

# ссылка на начальную таблицу, откуда берутся все данные
st_csv_filename = 'csv\\initial csv\\anime_filtered.csv'

mysql_engine = 'mysql://root@localhost:3306/anime_norm_maria?charset=utf8'
engine = sqlalchemy.create_engine(mysql_engine)

anime = pd.read_csv(st_csv_filename)

# список с id anime (для заполнения таблицы relation)
anime_id_list = list(anime.anime_id)

# названия таблиц
anime_table = 'anime'
relation_table = 'relation'
prods_table = 'producer'
licens_table = 'licensor'
studs_table = 'studio'
genres_table = 'genre'

# main_files (ссылки на файлы основных таблиц)
prods_file = 'csv\\' + prods_table + '.csv'
licens_file = 'csv\\' + licens_table + '.csv'
studs_file = 'csv\\' + studs_table + '.csv'
genres_file = 'csv\\' + genres_table + '.csv'
relation_file = 'csv\\' + relation_table + '.csv'
anime_file = 'csv\\' + anime_table + '.csv'

# staging_files (ссылки на файлы промежуточных таблиц)
prods_anime_file = 'csv\\anime_' + prods_table + '.csv'
licens_anime_file = 'csv\\anime_' + licens_table + '.csv'
studs_anime_file = 'csv\\anime_' + studs_table + '.csv'
genres_anime_file = 'csv\\anime_' + genres_table + '.csv'

# sets (множества для отбора уникальных значений для заполнения основных таблиц)
prods = set()
licens = set()
studs = set()
genres = set()

# main_lists (списки для основных таблиц)
prods_list = list()
licens_list = list()
studs_list = list()
genres_list = list()

# staging_lists (списки для промежуточных таблиц)
prods_anime_list = list()
licens_anime_list = list()
studs_anime_list = list()
genres_anime_list = list()

relation = list()

# списки названий колонок
cols = [prods_table, licens_table, studs_table, genres_table]

# список множеств для отбора уникальных значений для заполнения основных таблиц
sets = [prods, licens, studs, genres]

# списки для основных таблиц (названия и файлы)
main_lists = [prods_list, licens_list, studs_list, genres_list]
main_files = [prods_file, licens_file, studs_file, genres_file]

# списки для промежуточных таблиц (названия и файлы)
staging_lists = [prods_anime_list, licens_anime_list, studs_anime_list, genres_anime_list]
staging_files = [prods_anime_file, licens_anime_file, studs_anime_file, genres_anime_file]


# перезапись поля duration (перевод в минуты)
def change_dur(x):
    if 'per ep' in x:
        x = x[:-8]

    if 'min' in x:
        x = x[:-5]

    if 'hr' in x and len(x) > 5:
        x = int(60 * int(x[0])) + int(x[6:])
    elif 'hr' in x:
        x = int(60 * int(x[0]))

    if type(x) != int and 'sec' in x:
        x = '1'
    if type(x) != int and 'Unknown' in x:
        x = 0

    return x


# смещение индекса для корректной записи в таблицы и csv
def reindexing(lst):
    rdf = pd.DataFrame(lst)
    rdf.index = rdf.index + 1
    return rdf


# Очистка таблиц перед заполнением
def clear_table(table_name):
    q = f"""
            DELETE
            FROM {table_name}
        """
    cursor = engine.connect()
    cursor.execute(q)


# Очистка таблиц перед заполнением
for i in cols:
    clear_table(i)
    clear_table(f'anime_{i}')
clear_table(relation_table)
clear_table(anime_table)

# Заполнение списка relation
for ind, data in anime.iterrows():
    if data.related != '[]':
        js_dic = json.loads(data.related.replace('\"', '+-=-+').replace('\'', '\"').replace('+-=-+', '\''))
        for i in js_dic:
            if i == 'Adaptation':
                continue
            for j in js_dic[i]:
                subid = j['mal_id']
                if subid in anime_id_list:
                    if subid != data.anime_id:
                        relation.append((data.anime_id, i, subid))
relation = sorted(relation, key=lambda x: (x[0], x[1], x[2]))

# добавление  полей с сылками на myanimelist и shikimori
anime['url_mal'] = 'https://myanimelist.net/anime/' + anime.anime_id.apply(str)
anime['url_shiki'] = 'https://shikimori.one/animes/' + anime.anime_id.apply(str)

# перевод airing из string в bool (запись в tinyint 0/1)
anime['airing'] = anime.airing.apply(bool)

# замена амперсандов и апострофов во всей таблице
anime = anime.replace(
    to_replace=r'&#039;', value="'", regex=True).replace(to_replace=r'&amp;', value="&", regex=True)

# замена ссылок на картинки на корректные
anime.image_url = anime.image_url.replace(
    to_replace='https://myanimelist.cdn-dena.com/', value='https://cdn.myanimelist.net/', regex=True)

# разделение поля premiered на season и year
anime = anime.join(anime.premiered.str.split(expand=True)).rename(
    columns={0: 'premiered_season', 1: 'premiered_year'})

# разделение broadcast (время и день показа) на day и time
anime = anime.join(anime.broadcast.str.replace(r' .JST.', '').str.split(' at ', expand=True)).rename(
    columns={0: 'broadcast_day', 1: 'broadcast_time'})

# разделение aired(даты показа) на start date и finish date
anime = anime.join(
    anime.aired_string.str.split(' to ', expand=True)).rename(columns={0: 'start_date', 1: 'finish_date'})

# перезапись поля duration (перевод в минуты)
anime.duration = anime.duration.apply(change_dur)

for s, col, mlist, mfile, slist, sfile in zip(sets, cols, main_lists, main_files, staging_lists, staging_files):
    # образование списков для основных таблиц
    for ind, data in anime.iterrows():
        if not data[col] is None and str(data[col]) != 'nan':
            s.update(set(list(map(str, data[col].split(', ')))))
    mlist.append('None')
    mlist.extend(sorted(s))

    # запись основных таблиц в csv
    reindexing(mlist).to_csv(mfile, header=None, encoding='utf-8-sig')
    print('File', mfile, 'updated!')

    # запись основных таблиц в базу
    reindexing(mlist).rename(columns={0: f'title_{col}'}).to_sql(col, index=f'id_{col}', if_exists='append', con=engine)
    print(f'Table {col} updated!')

    # образование списков для промежуточных таблиц
    for ind, data in anime.iterrows():
        if not data[col] is None and str(data[col]) != 'nan':
            buf_list = list(map(str, data[col].split(', ')))
            for i in range(len(buf_list)):
                slist.append(list(map(int, (data.anime_id, mlist.index(buf_list[i])))))
        else:
            slist.append(list(map(int, (data.anime_id, 1))))

    # запись промежуточных таблиц в csv
    reindexing(slist).to_csv(sfile, header=None, index=None, encoding='utf-8-sig')
    print('File', sfile, 'updated!')

    # запись промежуточных таблиц в базу
    reindexing(slist).rename(
        columns={0: 'id_anime', 1: f'id_{col}'}).to_sql(f'anime_{col}', index=False, if_exists='append', con=engine)
    print(f'Table {col}_anime updated!')
    print()

# Удаление лишних колонок
anime.drop(
    columns=['aired_string', 'aired', 'score', 'scored_by', 'rank', 'popularity', 'members', 'favorites',
             'background', 'premiered', 'broadcast', 'related', 'producer', 'licensor', 'studio', 'genre'],
    inplace=True)

# Запись главной таблицы anime в csv
anime.to_csv(anime_file, index=None, encoding='utf-8-sig')
print('File', anime_file, 'updated!')

# Запись главной таблицы anime в базу
anime.to_sql(anime_table, index=False, if_exists='append', con=engine)
print('Table', anime_table, 'updated!')

# Запись таблицы relation (связи между аниме)
pd.DataFrame(relation).replace(
    to_replace=r'&#039;', value="'", regex=True).replace(
    to_replace=r'&amp;', value="&", regex=True).rename(
    columns={0: 'id_anime_object', 1: 'id_relation', 2: 'id_anime_subject'}).to_sql(
    relation_table, index=False, if_exists='append', con=engine)
print('Table', relation_table, 'updated!')

# Запись файла relation.csv (связи между аниме)
pd.DataFrame(relation).replace(
    to_replace=r'&#039;', value="'", regex=True).replace(
    to_replace=r'&amp;', value="&", regex=True).to_csv(
    relation_file, header=None, index=False, encoding='utf-8-sig')
print('File', relation_file, 'updated!')
print('Complete!')
