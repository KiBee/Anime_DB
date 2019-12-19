import pandas as pd
# import sqlalchemy
import json
from bd import Db

# import data from animelist to tables:
#           producer, licensor, studio, genres, relation
#           animelist_producer, animelist_licensor, animelist_studio, animelist_genres
#  and create .csv files to */csv/

# ссылка на начальную таблицу, откуда берутся все данные
st_csv_filename = 'csv\\initial csv\\anime_filtered.csv'

# mysql_engine = 'mysql://root@localhost:3306/anime_norm_maria?charset=utf8'
# engine = sqlalchemy.create_engine(mysql_engine)

engine = Db('anime_norm_maria')
connect = engine.connect()

anime = pd.read_csv(st_csv_filename).rename(columns={'anime_id': 'id_anime'})

# список с id anime (для заполнения таблицы relation)
id_anime_list = list(anime.id_anime)

# названия таблиц
anime_table = 'anime'
relation_table = 'relation'
prods_table = 'producer'
licens_table = 'licensor'
studs_table = 'studio'
genres_table = 'genre'

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
sets = [set(), set(), set(), set()]

# списки для основных таблиц (названия и файлы)
main_lists = [prods_list, licens_list, studs_list, genres_list]

# списки для промежуточных таблиц (названия и файлы)
staging_lists = [prods_anime_list, licens_anime_list, studs_anime_list, genres_anime_list]


def get_stf_name(t):
    return 'csv\\anime_' + t + '.csv'


def get_mf_name(t):
    return 'csv\\' + t + '.csv'


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
for i in cols:
    st = 'anime_' + i
    engine.clear_table(st)
    engine.clear_table(i)
engine.clear_table(relation_table)
engine.clear_table(anime_table)

# Заполнение списка relation
for ind, data in anime.iterrows():
    if data.related != '[]':
        js_dic = json.loads(data.related.replace('\"', '+-=-+').replace('\'', '\"').replace('+-=-+', '\''))
        for i in js_dic:
            if i == 'Adaptation':
                continue
            for j in js_dic[i]:
                subid = j['mal_id']
                if subid in id_anime_list:
                    if subid != data.id_anime:
                        relation.append((data.id_anime, i, subid))

relation = pd.DataFrame(sorted(relation, key=lambda x: (x[0], x[1], x[2]))).rename(
    columns={0: 'id_anime_object', 1: 'title_relation', 2: 'id_anime_subject'})

# добавление  полей с сылками на myanimelist и shikimori
anime['url_mal'] = 'https://myanimelist.net/anime/' + anime.id_anime.apply(str)
anime['url_shiki'] = 'https://shikimori.one/animes/' + anime.id_anime.apply(str)

# перевод airing из string в bool (запись в tinyint 0/1)
anime['airing'] = anime.airing.apply(bool)

# замена амперсандов и апострофов во всей таблице
anime = anime.replace(to_replace=r'&#039;', value="'", regex=True).replace(to_replace=r'&amp;', value="&", regex=True)

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
anime = anime.join(anime.aired_string.str.split(' to ', expand=True)).rename(
    columns={0: 'start_date', 1: 'finish_date'})

# перезапись поля duration (перевод в минуты)
anime.duration = anime.duration.apply(change_dur)

buf = anime.drop(
    columns=['aired_string', 'aired', 'score', 'scored_by', 'rank', 'popularity', 'members', 'favorites',
             'background', 'premiered', 'broadcast', 'related', 'producer', 'licensor', 'studio', 'genre'])

# Запись главной таблицы anime в csv
buf.to_csv(get_mf_name(anime_table), index=None, encoding='utf-8-sig')
print('File', get_mf_name(anime_table), 'updated!')

# Запись главной таблицы anime в базу
buf.to_sql(anime_table, index=False, if_exists='append', con=connect)
print('Table', anime_table, 'updated!')
print()

for s, col, mlist, slist in zip(sets, cols, main_lists, staging_lists):
    # образование списков для основных таблиц
    for ind, data in anime.iterrows():
        if not data[col] is None and str(data[col]) != 'nan':
            s.update(set(list(map(str, data[col].split(', ')))))
    mlist.append('None')
    mlist.extend(sorted(s))

    # запись основных таблиц в csv
    reindexing(mlist).to_csv(get_mf_name(col), header=None, encoding='utf-8-sig')
    print('File', get_mf_name(col), 'updated!')

    # запись основных таблиц в базу
    reindexing(mlist).rename(
        columns={0: f'title_{col}'}).to_sql(col, index=f'id_{col}', if_exists='append', con=connect)
    print(f'Table {col} updated!')

    # образование списков для промежуточных таблиц
    for ind, data in anime.iterrows():
        if not data[col] is None and str(data[col]) != 'nan':
            buf_list = list(map(str, data[col].split(', ')))
            for i in range(len(buf_list)):
                slist.append(list(map(int, (data.id_anime, mlist.index(str(buf_list[i])) + 1))))
        else:
            slist.append(list(map(int, (data.id_anime, 1))))

    # запись промежуточных таблиц в csv
    pd.DataFrame(slist).to_csv(get_stf_name(col), header=None, index=None, encoding='utf-8-sig')
    print('File', get_stf_name(col), 'updated!')

    # запись промежуточных таблиц в базу
    pd.DataFrame(slist).rename(
        columns={0: 'id_anime', 1: f'id_{col}'}).to_sql(
        f'anime_{col}', index=False, if_exists='append', con=connect)
    print(f'Table {col}_anime updated!')
    print()

# Запись таблицы relation (связи между аниме)
relation.to_sql(relation_table, index=False, if_exists='append', con=connect)
print('Table', relation_table, 'updated!')

# Запись файла relation.csv (связи между аниме)
relation.to_csv(get_mf_name(relation_table), header=None, index=False, encoding='utf-8-sig')
print('File', get_mf_name(relation_table), 'updated!')
print('Complete!')
