import pandas as pd
import json

df = pd.read_csv('csv/initial csv/anime_filtered.csv')

a = []
outer = set()

# print(df.iloc[700].related.replace('\'', '\"'))

# json.dumps(json.loads(df.related.iloc[17].replace('\'', '\"')), open('test.js', 'w'))

ldfid = list(df.anime_id)

for ind, data in df.iterrows():
    if data.related != '[]':

        js_dic = json.loads(data.related.replace('\"', '+-=-+').replace('\'', '\"').replace('+-=-+', '\''))

        for i in js_dic:
            if i == 'Adaptation':
                continue
            for j in js_dic[i]:
                subid = j['mal_id']
                if subid in ldfid:
                    if subid != data.anime_id:
                        a.append((data.anime_id,  i, subid))
                    else:
                        outer.add(('Doubling', subid))
                else:
                    outer.add((i, data.anime_id, 'Without', j['title'], subid))

print(len(outer))


