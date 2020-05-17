import qbscrape
import pandas as pd

urls = []
with open('player_urls.txt') as f:
    urls = f.read().split(',')

total_dict = {}
for url in urls:
    qb_dict, columns, qb_name = qbscrape.scraper(url) 
    total_dict.update(qb_dict)

total_df = []
for player, stats in total_dict.items():
    df = qbscrape.player_df(stats,columns=columns,qb_name=player)
    total_df.append(df)
    
print(total_df)