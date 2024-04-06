from flask import Flask, request, jsonify
from flask.helpers import send_file
from api.getOdds import provideOdds
from api.getSports import getSports

app = Flask(__name__, static_url_path='/', static_folder='web')

@app.route("/")
def indexPage():
     return send_file("web/index.html")  

@app.route("/get_odds")
def get_odds():
    # fGet the arguments from the request
    sportsType = request.args.get('sports_type')
    region = request.args.get('region')
    result = provideOdds(sportsType, region)
    
    return jsonify(result)

@app.route('/sports', methods=['GET'])
def get_sports_types():
     return jsonify(getSports())