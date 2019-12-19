from bd import Db

kek = Db('test_interface')
# print(pd.DataFrame(kek.show()))
# print(pd.DataFrame(kek.show_table('anime')))
# left = pd.DataFrame(
#     kek.left_join(l_table='anime', r_table='anime_genre',
#                   l_col='anime_id', r_col='id_anime',
#                   l_show='title', r_show='id_genre'))

# test = kek.join(l_table='genre', r_table='anime_genre', type_join='left',
#                 l_col='id_genre', r_col='id_genre',
#                 l_show='title_genre', r_show='id_anime')
kek.show_table('user')

# kek.clear_table('user')

# print(test)

# print(kek.show_all())
# print(kek.show_all().iloc[0, 0])

# print(kek.show_table(kek.show_all().iloc[0, 0]))

# print(test)

# st_test = pd.DataFrame(
#     kek.staging_left_join(l_table='anime', r_table='genre', st_table='anime_genre',
#                           l_col='id_anime', r_col='id_genre',
#                           l_show='title', r_show='title_genre'))


# kek.join(test, st_test)
# print(test.head())
# left.to_csv('test_left.csv', index=False, header=False)
# print(pd.DataFrame(kek.describe('anime')))
# test.to_csv('test_test.csv', index=False, header=False)
# st_test.to_csv('st_test.csv', index=False, header=False)
# def get_mf_name(t):
#     return 'csv\\' + t + '.csv'
#
#
# # import data from animelist to tables:
# #           producer, licensor, studio, genres, relation
# #           animelist_producer, animelist_licensor, animelist_studio, animelist_genres
# #  and create .csv files to */csv/
#
# # ссылка на начальную таблицу, откуда берутся все данные
# st_csv_filename = 'csv\\initial csv\\anime_filtered.csv'
# user_filename = 'csv\\initial csv\\user_filtered.csv'
#
# user_table = 'user'
#
# mysql_engine = 'mysql://root@localhost:3306/anime_norm_maria?charset=utf8'
# engine = sqlalchemy.create_engine(mysql_engine)
#
# anime = pd.read_csv(st_csv_filename)
# users = pd.read_csv(user_filename)
# users = users.drop(columns=['location',
#                             'user_id', 'user_watching', 'user_completed', 'user_onhold', 'user_dropped',
#                             'user_plantowatch',
#                             'user_days_spent_watching', 'access_rank', 'last_online', 'stats_mean_score',
#                             'stats_rewatched', 'stats_episodes'])
#
# print(users.columns)
# # список с id anime (для заполнения таблицы relation)
# anime_id_list = list(anime.anime_id)
# # users = users.replace(to_replace='"', value="|", regex=True).replace(to_replace=r',', value="+_-_-+", regex=True)
# pass
# users['username'] = users.username.where(~users.username.isna(), 'null')
# users.to_csv(get_mf_name(user_table), index=False)
# # users.dty
# users.to_sql(user_table, index=False, if_exists='append', con=engine)
#
# # to_sql(col, index=f'id_{col}', if_exists='append', con=engine)
#
# # названия таблиц
# anime_table = 'anime'
