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

q = """
        SELECT *
        FROM anime_filtered_full
    """


plsg = pd.read_csv(st_csv_filename)


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


# смещение индекса для корректной записи в таблицы и csv
def reindexing(lst):
    rdf = pd.DataFrame(lst)
    rdf.index = rdf.index + 1
    return rdf


# запись основных таблиц в csv
for s, c, l, f in zip(sets, cols, main_lists, main_files):
    for k, v in plsg.iterrows():
        if not v[c] is None and str(v[c]) != 'nan':
            v[c] = v[c].replace('&#039;', "'").replace('&amp;', "&")
            s.update(set(list(map(str, v[c].split(', ')))))
    l.append('None')
    l.extend(sorted(s))
    reindexing(l).to_csv(f, header=None, encoding='utf-8-sig')
    print(f, 'updated')


# # запись основных таблиц в базу
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
    for k, v in plsg.iterrows():
        if not v[c] is None and str(v[c]) != 'nan':
            v[c] = v[c].replace('&#039;', "'").replace('&amp;', "&")
            buf_list = list(map(str, v[c].split(', ')))
            for i in range(len(buf_list)):
                stl.append(list(map(int, (v.anime_id, m.index(buf_list[i])))))
        else:
            stl.append(list(map(int, (v.anime_id, 1))))
    reindexing(stl).to_csv(stf, header=None, index=None, encoding='utf-8-sig')
    print(stf, 'updated')


# # запись промежуточных таблиц в базу
reindexing(prods_animelist_list).rename(columns={0: 'id_anime', 1: 'id_producer'}).to_sql('anime_producer', index=False,  if_exists='append', con=engine)
print('Table Animelist_producer updated')
reindexing(licens_animelist_list).rename(columns={0: 'id_anime', 1: 'id_licensor'}).to_sql('anime_licensor', index=False,  if_exists='append', con=engine)
print('Table Animelist_licensor updated')
reindexing(studs_animelist_list).rename(columns={0: 'id_anime', 1: 'id_studio'}).to_sql('anime_studio', index=False,  if_exists='append', con=engine)
print('Table Animelist_studio updated')
reindexing(genres_animelist_list).rename(columns={0: 'id_anime', 1: 'id_genre'}).to_sql('anime_genre', index=False,  if_exists='append', con=engine)
print('Table Animelist_genre updated')
print('Completed!')