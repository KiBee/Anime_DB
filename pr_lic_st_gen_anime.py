import pandas as pd
import sqlalchemy

# import data from animelist to tables:
#           producer, licensor, studio, genres,
#           animelist_producer, animelist_licensor, animelist_studio, animelist_genres
#  and create .csv files to */csv

st_csv_filename = 'csv\\initial csv\\anime_filtered.csv'

mysql_engine = 'mysql://root@localhost:3306/anime_norm_maria?charset=utf8'
engine = sqlalchemy.create_engine(mysql_engine)

anime = pd.read_csv(st_csv_filename)

# main_files
prods_file = 'csv\\producer.csv'
licens_file = 'csv\\licensor.csv'
studs_file = 'csv\\studio.csv'
genres_file = 'csv\\genres.csv'

# staging_files
prods_animelist_file = 'csv\\anime_producer.csv'
licens_animelist_file = 'csv\\anime_licensor.csv'
studs_animelist_file = 'csv\\anime_studio.csv'
genres_animelist_file = 'csv\\anime_genres.csv'

# sets
prods = set()
licens = set()
studs = set()
genres = set()

# main_lists
prods_list = list()
licens_list = list()
studs_list = list()
genres_list = list()

# staging_lists
prods_animelist_list = list()
licens_animelist_list = list()
studs_animelist_list = list()
genres_animelist_list = list()

anime_table = 'test_anime'

cols = ['producer', 'licensor', 'studio', 'genre']
sets = [prods, licens, studs, genres]

# списки для основных таблиц
main_lists = [prods_list, licens_list, studs_list, genres_list]
main_files = [prods_file, licens_file, studs_file, genres_file]

# списки для промежуточных таблиц
staging_lists = [prods_animelist_list, licens_animelist_list, studs_animelist_list, genres_animelist_list]
staging_files = [prods_animelist_file, licens_animelist_file, studs_animelist_file, genres_animelist_file]


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


# перезапись полей с url_image(битые ссылки)
def change_url_img(x):
    if type(x) != float:
        x = str(x.replace('https://myanimelist.cdn-dena.com/', 'https://cdn.myanimelist.net/'))
    return x


# смещение индекса для корректной записи в таблицы и csv
def reindexing(lst):
    rdf = pd.DataFrame(lst)
    rdf.index = rdf.index + 1
    return rdf


def clear_table(table_name):
    q = f"""
            DELETE
            FROM {table_name}
        """
    cursor = engine.connect()
    cursor.execute(q)


for i in cols:
    clear_table(i)
    clear_table(f'anime_{i}')
clear_table(anime_table)

# добавление  полей с сылками на myanimelist и shikimori
anime['url_mal'] = 'https://myanimelist.net/anime/' + anime.anime_id.apply(str)
anime['url_shiki'] = 'https://shikimori.one/animes/' + anime.anime_id.apply(str)
anime['airing'] = anime.airing.apply(bool) + 1

# перезапись поля duration (перевод в минуты)
anime.duration = anime.duration.apply(change_dur)

# перезапись полей с url_image(битые ссылки)
anime.image_url = anime.image_url.apply(change_url_img)

# образование списков основных таблиц
for s, c, m, f, stl, stf in zip(sets, cols, main_lists, main_files, staging_lists, staging_files):
    for k, v in anime.iterrows():
        if not v[c] is None and str(v[c]) != 'nan':
            v[c] = v[c].replace('&#039;', "'").replace('&amp;', "&")
            s.update(set(list(map(str, v[c].split(', ')))))
    m.append('None')
    m.extend(sorted(s))

    # запись основных таблиц в csv
    reindexing(m).to_csv(f, header=None, encoding='utf-8-sig')
    print(f, 'updated!')

    # запись основных таблиц в базу
    reindexing(m).rename(columns={0: f'title_{c}'}).to_sql(c, index=f'id_{c}', if_exists='append', con=engine)
    print(f'Table {c} updated!')
    print()

    for k, v in anime.iterrows():
        if not v[c] is None and str(v[c]) != 'nan':
            v[c] = v[c].replace('&#039;', "'").replace('&amp;', "&")
            buf_list = list(map(str, v[c].split(', ')))
            for i in range(len(buf_list)):
                stl.append(list(map(int, (v.anime_id, m.index(buf_list[i])))))
        else:
            stl.append(list(map(int, (v.anime_id, 1))))

    reindexing(stl).to_csv(stf, header=None, index=None, encoding='utf-8-sig')
    print(stf, 'updated!')

    reindexing(stl).rename(columns={0: 'id_anime', 1: f'id_{c}'}).to_sql(f'anime_{c}', index=False, if_exists='append',
                                                                         con=engine)
    print(f'Table {c}_anime updated!')
    print()

anime.drop(
    columns=['aired_string', 'aired', 'score', 'scored_by', 'rank', 'popularity', 'members', 'favorites',
             'background', 'premiered', 'broadcast', 'related', 'producer', 'licensor', 'studio', 'genre'],
    inplace=True)

anime.rename(columns={0: 'anime_id',
                      1: 'title',
                      2: 'title_english',
                      3: 'title_japanese',
                      4: 'title_synonyms',
                      5: 'image_url',
                      6: 'type',
                      7: 'source',
                      8: 'episodes',
                      9: 'status',
                      10: 'airing',
                      13: 'duration',
                      14: 'rating',
                      19: 'opening_theme',
                      20: 'ending_theme',
                      21: 'url_mal',
                      22: 'url_shiki'
                      }).to_sql(anime_table, index=False, if_exists='append', con=engine)

print('Table test_anime updated!')

print('Complete!')
