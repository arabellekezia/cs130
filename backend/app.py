from flask import Flask, request
import requests
from staywell_api import StaywellExternalAPI
from edamam_api import EdamamAPI
from user import User

app = Flask(__name__)

@app.route('/')
def index():
    return 'Better You'

# params: weight - int, workout - str, minutes - int, user - int
# example: http://localhost:5000/staywell?weight=130&workout=Bowling&minutes=30&user=1
@app.route('/enterWorkout')
def enterWorkout():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    api = StaywellExternalAPI()
    return api.staywell(args)

# params: item - str/int, barcode - optional boolean
@app.route('/getNutritionalData')
def getNutritionalData():
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

# params: item - str/int, barcode - optional boolean, nMatches - int
@app.route('getAvailableFoods')
def getAvailableFoods():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    if not 'item' in args:
        return "The 'item' is a required parameter", 400
    item = args['item']
    barcode = False
    if 'barcode' in args and args['barcode'].upper() == "TRUE":
        barcode = True
    n = 5
    if 'nMatches' in args:
        try:
            n = int(args['nMatches'])
        except:
            return "Parameter 'nMatches' must be an integer", 400
    api = EdamamAPI()
    food_dict, success = api.get_top_matches(item, barcode, n)
    if not success:
        return "Unable to find the food item based on given info", 400
    else:
        return food_dict, 200

@app.route('/auth/login')
def login():

# params: email - str, password - str
@app.route('/register')
def register():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    if not 'email' in args:
        return "The 'email' is a required parameter", 400
    email = args['email']
    if not 'password' in args:
        return "The 'password' is a required parameter", 400
    password = args['password']
    usr = User()
    if usr.create_new_user(email, password):
        return "Succesfully Registered", 200
    else:
        return "Unable to register new user, they possibly already have an account", 400

# params: user - int, dateFrom - datetime timestamp, dateTo - datetime timestamp
@app.route('/getMeals')
def getMeals():

# params: user - int, selectedFood - dict (??), serving size - double
@app.route('/addMeal')

# params: user - int, dateFrom - datetime timestamp, dateTo - datetime timestamp
@app.route('/getSleepData')

@app.route('/insertSleepEntry')

# params: user - int, dateFrom - datetime timestamp, dateTo - datetime timestamp
@app.route('/getFitnessData')

# TODO: goals stuff (?)
# params: user - int
@app.route('/getAllGoals')

# params: user - int, type - char(1) -> D, F, S
@app.route('/getTypeGoals')

@app.route('/insertGoal')

@app.route('/removeGoal')


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=False)
