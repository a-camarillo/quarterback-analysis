import requests
from bs4 import BeautifulSoup as soup 
import pandas as pd


def scraper(url):
    '''
    This function will pass a url(nfl.com/players/) and scrape the webpage for the passing statistics of the player.
    Only for quarterback statistics since other positions may give different results
    '''

    r = requests.get(url)
    c = r.content

    page = soup(c,'html.parser')

    #get the name of the quarterback
    qb_name = page.find("div",{"class":"nfl-c-player-header__title"}).text

    #initialize quarterback dictionary
    qb_dict = {qb_name:{}}

    #grab the table of passing statistics
    passing =  page.find("table",{"class":"d3-o-table d3-o-standings--detailed d3-o-table--sortable {sortlist: [[0,1]], debug: true}"})  
    
    #grabs headers from table, will use for column labels
    headers = passing.find("thead")
    columns = [th.text for th in headers.findAll("th")]

    #get al of the table rows and remove first(columns) and last(total) columns
    trows = passing.findAll("tr")
    trows.pop()
    trows.pop(0)
    
    #update dict with the year as the key and an empty dict as the value
    for row in trows:
        qb_dict[qb_name].update({row.find("td").text.strip():[]})
    
    #update each year key with a list of the corresponding stats for that year
    for row in trows:
        tds = row.findAll("td")
        for key in qb_dict[qb_name].keys():
            if tds[0].text.strip() == key:
                qb_dict[qb_name].update({key:[td.text.strip() for td in tds]})

    return qb_dict, columns, qb_name

def player_df(dictionary,columns=None,qb_name=None):
    '''This function will take in the values returned from scraper
       and create a dataframe from those values
    '''
    df = pd.DataFrame.from_dict(data=dictionary,columns=columns,orient='index')
    
    #create a column to label the player
    df['qb_name'] = [qb_name]*len(df)
    
    #reset index to integer based
    df.reset_index(drop=True,inplace=True)
    
    #create a column for their year in the league
    df['year_played'] = [i+1 for i in range(0,len(df))]
    return df
