from flask import Flask, request
import requests
from staywell_api import StaywellExternalAPI
from edamam_api import EdamamAPI
from user import User
from db import DB
from Diet import Diet
from Fitness import Fitness
from Sleep import Sleep
from goals import Goals

app = Flask(__name__)
DB_OBJECT = DB()
USER = User(DB_OBJECT)
STAYWELL_API = StaywellExternalAPI()

@app.route('/')
def index():
    return 'Better You'

# params: weight - int, workout - str, minutes - int, token - str
@app.route('/enterWorkout')
def enterWorkout():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 400
    return STAYWELL_API.staywell(args, id, DB_OBJECT)

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
    food_dict, success = api.get_top_matches(item, barcode, 1)
    if not success:
        return "Unable to find the food item based on given info", 400
    else:
        return food_dict, 200

# params: item - str/int, barcode - optional boolean, nMatches -  optional int
@app.route('/getAvailableFoods')
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

# params: email - str, password - str
@app.route('/auth/login')
def login():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    if not 'email' in args:
        return "The 'email' is a required parameter", 400
    email = args['email']
    if not 'password' in args:
        return "The 'password' is a required parameter", 400
    password = args['password']
    id = USER.check_password_match(email, password)
    if id < 0:
        return "Incorrect login information.", 400
    return USER.encode_token(id)

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
    if USER.create_new_user(email, password):
        return "Succesfully Registered", 200
    else:
        return "Unable to register new user, they possibly already have an account", 400

# params: token - str, dateFrom - datetime timestamp, dateTo - datetime timestamp
@app.route('/getMeals')
def getMeals():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    dates_data = check_datetimes(args)
    if dates_data['status_code'] != 200:
        return dates_data['msg], dates_data['status_code']
    dateFrom = dates_data['dateFrom']
    dateTo = dates_data['dateTo']
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 400
    diet = Diet(DB_OBJECT, id)
    db_data, success = diet.get_columns_given_range(dateFrom, dateTo)
    if not success:
        return "Server Error", 500
    else:
        return db_data, 200

# params: user - int, selectedFood - dict (??), serving size - double
@app.route('/addMeal')
def addMeal():

# params: token - str, dateFrom - datetime timestamp, dateTo - datetime timestamp
@app.route('/getSleepData')
def getSleepData():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    dates_data = check_datetimes(args)
    if dates_data['status_code'] != 200:
        return dates_data['msg], dates_data['status_code']
    dateFrom = dates_data['dateFrom']
    dateTo = dates_data['dateTo']
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 400
    sleep = Sleep(DB_OBJECT, id)
    db_data, success = sleep.get_columns_given_range(dateFrom, dateTo)
    if not success:
        return "Server Error", 500
    else:
        return db_data, 200

@app.route('/insertSleepEntry')
def insertSleepEntry():

# params: token - str, dateFrom - datetime timestamp, dateTo - datetime timestamp
@app.route('/getFitnessData')
def getFitnessData():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    dates_data = check_datetimes(args)
    if dates_data['status_code'] != 200:
        return dates_data['msg], dates_data['status_code']
    dateFrom = dates_data['dateFrom']
    dateTo = dates_data['dateTo']
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 400
    fitness = Fitness(DB_OBJECT, id)
    db_data, success = fitness.get_columns_given_range(dateFrom, dateTo)
    if not success:
        return "Server Error", 500
    else:
        return db_data, 200

# params: token - str
@app.route('/getAllGoals')
def getAllGoals():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 400
    goals = Goals(DB_OBJECT, id)
    db_data, success = goals.get_all_goals()
    if not success:
        return "Server Error", 500
    else:
        return db_data, 200

# params: token - str, type - char(1) -> D, F, S
@app.route('/getTypeGoals')
def getTypeGoals():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    goal_data = check_goal_type(args)
    if goal_data['status_code'] != 200:
        return goal_type['msg', goal_type['status_code']
    goal_type = goal_data['type']
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 400
    goals = Goals(DB_OBJECT, id)
    db_data, success = goals.get_type_goals(goal_type)
    if not success:
        return "Server Error", 500
    else:
        return db_data, 200

#@app.route('/insertGoal')

#@app.route('/removeGoal')

def check_goal_type(data):
    if not 'type' in data:
        return {"msg": "Please provide goal type",
                "status_code": 400}
    goal_type = data['type']
    options = ["D", "F", "S"]
    if goal_type not in options:
        return {"msg": "Goal Type must be 'D', 'F', or 'S'",
                "status_code": 400}
    return {'type': goal_type, "status_code": 200}

def check_datetimes(data):
    # TODO: convert datetimes
    if not 'dateFrom' in data:
        return {"msg": "Please provide 'dateFrom' datetime parameter",
                "status_code": 400}
    if not 'dateTo' in data:
        return {"msg": "Please provide 'dateTo' datetime parameter",
                "status_code": 400}
    else:
        return {"dateFrom": data['dateFrom'], "dateTo": data['dateTo'],
                "status_code": 200}

def check_token(data):
    if 'token' in data:
        token = data['token']
        return {"status_code": 200, "token": token}
    else:
        return {"msg": "Please provide a token",
                "status_code": 400}

def getIdFromToken(token):
    msg, code = USER.decode_token(token)
    if code != 200:
        return -1
    return int(msg)


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=False)
