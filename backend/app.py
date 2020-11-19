from flask import Flask, request
import requests
from staywell_api import StaywellExternalAPI
from edamam_api import EdamamAPI

app = Flask(__name__)

@app.route('/')
def index():
    return 'Better You'

# params: weight - int, workout - str, minutes - int, user - int
# example: http://localhost:5000/staywell?weight=130&workout=Bowling&minutes=30&user=1
@app.route('/staywell')
def staywell():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    api = StaywellExternalAPI()
    return api.staywell(args)

# params: item - str/int, barcode - optional boolean
@app.route('/edamam')
def edamam():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    if not 'item' in args:
        return "The 'item' is a required parameter", 400
    item = args['item']
    barcode = False
    if 'barcode' in args and args['barcode'].upper() == "TRUE":
        barcode = True
    api = EdamamAPI()
    food_dict, success = api.get_nutrient_information(item, barcode)
    if not success:
        return "Unable to find the food item based on given info", 400
    else:
        return food_dict, 200

# params: item - str/int, barcode - optional boolean
@app.route('getFoodItemMatches')
def getFoodItemMatches():


@app.route('/auth/login')
def login():

@app.route('/register')
def register():

# params: user - int, dateFrom - datetime timestamp, dateTo - datetime timestamp
@app.route('/getMealsConsumed')
def getMealsConsumed():

if __name__ == '__main__':
	app.run(host="localhost", port=5000, debug=False)
