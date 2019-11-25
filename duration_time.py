import pandas as pd
import sqlalchemy

mysql_engine = 'mysql://root@localhost:3306/anime_norm_maria?charset=utf8'
engine = sqlalchemy.create_engine(mysql_engine)

st_csv_filename = 'csv\\initial csv\\anime_filtered.csv'


in_df = pd.read_csv(st_csv_filename)

in_df['url_mal'] = 'https://myanimelist.net/anime/' + in_df.anime_id.apply(str)
in_df['url_shiki'] = 'https://shikimori.one/animes/' + in_df.anime_id.apply(str)


dur = list()
id = list()

# for k, v in in_df.iterrows():
#     dur.append(v.duration)
#     id.append(v.anime_id)
#     if 'per ep' in dur[k]:
#         dur[k] = dur[k][:-8]
#
#     if 'min' in dur[k]:
#         dur[k] = dur[k][:-5]
#
#     if 'hr' in dur[k] and len(dur[k]) > 5:
#         dur[k] = int(60 * int(dur[k][0])) + int(dur[k][6:])
#     elif 'hr' in dur[k]:
#         dur[k] = int(60 * int(dur[k][0]))
#
#     if type(dur[k]) != int and 'sec' in dur[k]:
#         dur[k] = '1'
#     if type(dur[k]) != int and 'Unknown' in dur[k]:
#         dur[k] = 0


def change_dur(x):

    # dur.append(v.duration)
    # id.append(v.anime_id)

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


in_df.duration = in_df.duration.apply(change_dur)

# for i in range(len(id)):
#     in_df.loc[in_df['anime_id'] == id[i], 'duration'] = dur[i]




