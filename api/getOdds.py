import requests
import pandas as pd
from api.parameters import client, api_key
from model.findBestBookmaker import findBestBookmaker

# select database and collection
db = client["mdm"]
oddsCollection = db["odds"]

# Generiert eine API-URL, mit der Odds/Quoten abgeholt werden können.
# key = sports type // region = bookmakers region // markets = type of odds
def getOdds(key, region="eu", markets="h2h"):
    url = 'https://api.the-odds-api.com/v4/sports/'
    url += key + '/'
    url += 'odds'
    url += '?apiKey=' + api_key
    url += '&regions=' + region 
    url += '&markets=' + markets
    url += '&dateFormat=iso&oddsFormat=decimal'
    return url

# Speichert die Spiele + Quoten in der Datenbank.
def saveOdds(df):
    for id_value in df['id'].unique():
        document = {'id': id_value, 'games': []}
        filtered_df = df[df['id'] == id_value]
        for game, group in filtered_df.groupby(['home_team', 'away_team']):
            game_document = {'home_team': game[0], 'away_team': game[1], 'bookmakers': []}
            for bookmaker, group in group.groupby(['bookmakers.title']):
                quote_list = []
                for index, row in group.iterrows():
                    quote_list.append({'name': row['name'], 'price': row['price']})
                bookmaker_document = {'name': bookmaker, 'quotes': quote_list}
                game_document['bookmakers'].append(bookmaker_document)
            document['games'].append(game_document)
        oddsCollection.insert_one(document)

# Diese Funktion wird vom Frontend abgerufen
def provideOdds(key, region="eu", markets="h2h"):
    response = requests.get(url=getOdds(key, region, markets)) # getOdds holt die Odds/Quoten ab
    data = response.json()
    # Pandas DataFrame wird erstellt
    df = pd.json_normalize(data, record_path=['bookmakers', 'markets', 'outcomes'], 
                       meta=['id', 'sport_title', 'commence_time', 'home_team', 'away_team', ['bookmakers', 'title']])
    # Drop double values
    df = df.drop_duplicates(subset=['id', 'bookmakers.title', 'name'])
    saveOdds(df)
    return findBestBookmaker(df)

