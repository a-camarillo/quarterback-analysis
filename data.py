import qbscrape
import pandas as pd

a_urls = []
with open('./links/player_urls.txt') as a_f:
    a_urls = a_f.read().split(',')

r_urls = []
with open('./links/player_urls_retired.txt') as r_f:
    r_urls = r_f.read().split(',')

retired_dict = {}
for url in r_urls:
    qb_dict, columns, qb_name = qbscrape.scraper(url)
    retired_dict.update(qb_dict)

retired_df = []
for player, stats in retired_dict.items():
    df = qbscrape.player_df(stats,columns=columns,qb_name=player)
    retired_df.append(df)

active_dict = {}
for url in a_urls:
    qb_dict, columns, qb_name = qbscrape.scraper(url) 
    active_dict.update(qb_dict)

active_df = []
for player, stats in active_dict.items():
    df = qbscrape.player_df(stats,columns=columns,qb_name=player)
    active_df.append(df)

for df in active_df:
    df['retired'] = 'No'

for df in retired_df:
    df['retired'] = 'Yes'

total_df = active_df[0]
total_df = total_df.append(other=active_df[1::])
total_df = total_df.append(other=retired_df)

total_df.to_csv('./qb_stats.csv')

