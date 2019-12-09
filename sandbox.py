import pandas as pd
from sqlalchemy import create_engine

mysql_engine = 'mysql://root@localhost:3306/anime_norm_maria?charset=utf8'

engine = create_engine(mysql_engine)

anime_str = 'anime'
list_str = 'animelist'
usrs_str = 'users'

users_file = f'csv\\{usrs_str}_filtered.csv'
list_file = f'csv\\{list_str}_filtered.csv'


users_df = pd.read_csv(users_file)
list_df = pd.read_csv(list_file)

q = f'''
        SELECT *
        FROM anime_norm_maria.{anime_str}
    '''

anime_df = pd.read_sql(q, engine)

users_df.drop(columns=['user_id', 'my_tags', 'my_last_updated'], inplace=True)

print(f'In table {anime_str} is {anime_df[~anime_df.anime_id.isin(list_df.anime_id)].shape[0]} animes, which no in table {list_str}')
print(f'In table {usrs_str} is {users_df[~users_df.username.isin(list_df.username)].shape[0]} animes, which no in table {list_str}')


