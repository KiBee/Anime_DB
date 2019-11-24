import pandas as pd
import sqlalchemy

mysql_engine = 'mysql://root@localhost:3306/anime_norm_maria?charset=utf8'

engine = sqlalchemy.create_engine(mysql_engine)


q = """
    SELECT *
    from test_anime
    """

dur = list()
id = list()
a = pd.read_sql(q, engine)

for k, v in a.iterrows():
    dur.append(v.duration)
    id.append(v.anime_id)
    if 'per ep' in dur[k]:
        dur[k] = dur[k][:-8]

    if 'min' in dur[k]:
        dur[k] = dur[k][:-5]

    if 'hr' in dur[k] and len(dur[k]) > 5:
        dur[k] = int(60 * int(dur[k][0])) + int(dur[k][6:])
    elif 'hr' in dur[k]:
        dur[k] = int(60 * int(dur[k][0]))

    if type(dur[k]) != int and 'sec' in dur[k]:
        dur[k] = '1'
    if type(dur[k]) != int and 'Unknown' in dur[k]:
        dur[k] = 0


for i in range(len(id)):
    a.loc[a['anime_id'] == id[i], 'duration'] = dur[i]




