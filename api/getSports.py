import requests
from api.parameters import client, api_key

# select database and collection
db = client["mdm"]
sportsCollection = db["sports"]

# URL um Sportarten abzuholen
sportsUrl = 'https://api.the-odds-api.com/v4/sports/?apiKey=' + api_key

def deleteAllSports():
    sportsCollection.delete_many({})
# Löscht alle Sportarten aus der Datenbank.
# Holt alle Sportarten bei der API ab.
# Anschliessend werden alle Sportsarten zurückgegeben.
def getSports():
    deleteAllSports()
    response = requests.get(url=sportsUrl)
    data = response.json()
    data = [sport for sport in data if not sport['has_outrights']]
    sportsCollection.insert_many(data)
    sports = [{'key': sport['key'], 'title': sport['title']} for sport in data]
    return sports