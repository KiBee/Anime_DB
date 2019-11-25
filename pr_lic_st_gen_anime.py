import pandas as pd
import numpy as np
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
prods_animelist_file = 'csv\\animelist_producer.csv'
licens_animelist_file = 'csv\\animelist_licensor.csv'
studs_animelist_file = 'csv\\animelist_studio.csv'
genres_animelist_file = 'csv\\animelist_genres.csv'

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


for i in cols:
    q = f"""
        DELETE
        FROM {i}
    """
    cursor = engine.connect()
    cursor.execute(q)

# добавление  полей с сылками на myanimelist и shikimori
anime['url_mal'] = 'https://myanimelist.net/anime/' + anime.anime_id.apply(str)
anime['url_shiki'] = 'https://shikimori.one/animes/' + anime.anime_id.apply(str)

# перезапись поля duration (перевод в минуты)
anime.duration = anime.duration.apply(change_dur)

# перезапись полей с url_image(битые ссылки)
anime.image_url = anime.image_url.apply(change_url_img)

# запись основных таблиц в csv
for s, c, l, f in zip(sets, cols, main_lists, main_files):
    for k, v in anime.iterrows():
        if not v[c] is None and str(v[c]) != 'nan':
            v[c] = v[c].replace('&#039;', "'").replace('&amp;', "&")
            s.update(set(list(map(str, v[c].split(', ')))))
    l.append('None')
    l.extend(sorted(s))
    reindexing(l).to_csv(f, header=None, encoding='utf-8-sig')
    print(f, 'updated')


# запись основных таблиц в базу
print()
reindexing(prods_list).rename(columns={0: 'title_producer'}).to_sql('producer', index='id_producer',  if_exists='append', con=engine)
print('Table Producer updated')
reindexing(licens_list).rename(columns={0: 'title_licensor'}).to_sql('licensor', index='id_licensor',  if_exists='append', con=engine)
print('Table Licensor updated')
reindexing(studs_list).rename(columns={0: 'title_studio'}).to_sql('studio', index='id_studio',  if_exists='append', con=engine)
print('Table Studio updated')
reindexing(genres_list).rename(columns={0: 'title_genre'}).to_sql('genre', index='id_genre',  if_exists='append', con=engine)
print('Table Genres updated')

# запись промежуточных таблиц в csv
for c, m, stl, stf in zip(cols, main_lists, staging_lists, staging_files):
    for k, v in anime.iterrows():
        if not v[c] is None and str(v[c]) != 'nan':
            v[c] = v[c].replace('&#039;', "'").replace('&amp;', "&")
            buf_list = list(map(str, v[c].split(', ')))
            for i in range(len(buf_list)):
                stl.append(list(map(int, (v.anime_id, m.index(buf_list[i])))))
        else:
            stl.append(list(map(int, (v.anime_id, 1))))
    reindexing(stl).to_csv(stf, header=None, index=None, encoding='utf-8-sig')
    print(stf, 'updated')

# запись промежуточных таблиц в базу
reindexing(prods_animelist_list).rename(columns={0: 'id_anime', 1: 'id_producer'}).to_sql('anime_producer', index=False,  if_exists='replace', con=engine)
print('Table Animelist_producer updated')
reindexing(licens_animelist_list).rename(columns={0: 'id_anime', 1: 'id_licensor'}).to_sql('anime_licensor', index=False,  if_exists='replace', con=engine)
print('Table Animelist_licensor updated')
reindexing(studs_animelist_list).rename(columns={0: 'id_anime', 1: 'id_studio'}).to_sql('anime_studio', index=False,  if_exists='replace', con=engine)
print('Table Animelist_studio updated')
reindexing(genres_animelist_list).rename(columns={0: 'id_anime', 1: 'id_genre'}).to_sql('anime_genre', index=False,  if_exists='replace', con=engine)
print('Table Animelist_genre updated')
print('Completed!')


anime.drop(
    columns=['airing', 'aired_string', 'aired', 'score', 'scored_by', 'rank', 'popularity', 'members', 'favorites',
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
                      13: 'duration',
                      14: 'rating',
                      19: 'opening_theme',
                      20: 'ending_theme',
                      21: 'url_mal',
                      22: 'url_shiki'
                      }).to_sql('test_anime', index=False, if_exists='replace', con=engine)
