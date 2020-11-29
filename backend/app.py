from flask import Flask, request
import requests
from datetime import datetime
import json
from backend.staywell_api import StaywellExternalAPI
from backend.edamam_api import EdamamAPI
from backend.user import User
from backend.db import DB
from backend.Diet import Diet
from backend.Fitness import Fitness
from backend.Sleep_aditya import Sleep
from backend.goals import Goals

app = Flask(__name__)
DB_OBJECT = DB(False)
USER = User(DB_OBJECT)
STAYWELL_API = StaywellExternalAPI()
EDAMAM_API = EdamamAPI()

@app.route('/')
def index():
    return 'Better You'

# params: weight - int, workout - str, minutes - int, token - str
@app.route('/enterWorkout', methods=['POST'])
def enterWorkout():
    args = request.form
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
@app.route('/getNutritionalData', methods=['GET'])
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
    food_dict, success = EDAMAM_API.get_top_matches(item, barcode, 1)
    if not success:
        return "Unable to find the food item based on given info", 400
    else:
        food_dict = json.dumps(food_dict)
        return food_dict, 200

# params: item - str/int, barcode - optional boolean, nMatches -  optional int
@app.route('/getAvailableFoods', methods=['GET'])
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
    food_dict, success = EDAMAM_API.get_top_matches(item, barcode, n)
    if not success:
        return "Unable to find the food item based on given info", 400
    else:
        food_dict = json.dumps(food_dict)
        return food_dict, 200

# params: email - str, password - str
@app.route('/auth/login', methods=['POST'])
def login():
    args = request.form
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
@app.route('/register', methods=['POST'])
def register():
    args = request.form
    if not args:
        return "Arguments needed.", 400
    if not 'email' in args:
        return "The 'email' is a required parameter", 400
    email = args['email']
    if not 'password' in args:
        return "The 'password' is a required parameter", 400
    password = args['password']
    if USER.create_new_user(email, password, fullname):
        id = USER.check_password_match(email, password)
        if id < 0:
            "Unable to find registered user.", 500
        goals = Goals(DB_OBJECT, id)
        diet_goal = {'Type': 'Calories', 'Value': 2000.0}
        fitness_goal = {'Type': 'FitnessMinutes', 'Value': 40.0}
        sleep_goal = {'Type': 'SleepHours', 'Value': 9.5}
        goals.set_goal(diet_goal)
        goals.set_goal(fitness_goal)
        goals.set_goal(sleep_goal)
        return "Succesfully Registered", 200
    else:
        return "Unable to register new user, they possibly already have an account", 400

# params: token - str, dateFrom - datetime timestamp, dateTo - datetime timestamp
@app.route('/getMeals', methods=['GET'])
def getMeals():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    dates_data = check_datetimes(args)
    if dates_data['status_code'] != 200:
        return dates_data['msg'], dates_data['status_code']
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
        db_data = json.dumps(db_data)
        return db_data, 200

# params: token - str, item - str, ServingSize - float, barcode - optional boolean
@app.route('/addMeal', methods=['POST'])
def addMeal():
    args = request.form
    if not args:
        return "Arguments needed.", 400
    if not 'item' in args:
        return "The 'item' is a required parameter", 400
    item = args['item']
    if not 'ServingSize' in args:
        return "The 'ServingSize' is a required parameter", 400
    serving_size = args['ServingSize']
    try:
        serving_size = float(serving_size)
    except ValueError:
        return "The 'ServingSize' must be a float or int", 400
    barcode = False
    if 'barcode' in args and args['barcode'].upper() == "TRUE":
        barcode = True
    food_dict, success = EDAMAM_API.get_top_matches(item, barcode, 1)
    if not success:
        return "Unable to find the food item based on given info", 400
    food_dict = food_dict[0]['Nutrients']
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 400
    insert_food_dict = {'Item': item, 'ServingSize': serving_size, 'Barcode': barcode}
    nutri_dict = {}
    for k, v in food_dict.items():
        nutri_dict[k] = v * serving_size
    insert_food_dict['nutri_dict'] = nutri_dict
    diet = Diet(DB_OBJECT, id)
    success = diet.insert_in_database(insert_food_dict)
    if not success:
        return "Server Error", 500
    else:
        return "Successful", 200

# params: token - str, dateFrom - datetime timestamp, dateTo - datetime timestamp
@app.route('/getSleepData', methods=['GET'])
def getSleepData():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    dates_data = check_datetimes(args)
    if dates_data['status_code'] != 200:
        return dates_data['msg'], dates_data['status_code']
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
        db_data = json.dumps(db_data)
        return db_data, 200

# params: token - str, dateFrom - datetime timestamp, dateTo - datetime timestamp, nap - optional bool
@app.route('/insertSleepEntry', methods=['POST'])
def insertSleepEntry():
    args = request.form
    if not args:
        return "Arguments needed.", 400
    dates_data = check_datetimes(args)
    if dates_data['status_code'] != 200:
        return dates_data['msg'], dates_data['status_code']
    SleepTime = dates_data['dateFrom']
    WakeupTime = dates_data['dateTo']
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 400
    Nap = False
    if 'nap' in args and args['nap'].upper() == 'TRUE':
        Nap = True
    sleep = Sleep(DB_OBJECT, id)
    success = sleep.insert_in_database({'SleepTime': SleepTime, 'WakeupTime': WakeupTime, 'Nap': Nap})
    if not success:
        return "Server Error", 500
    else:
        return 'Successful', 200

# params: token - str, dateFrom - datetime timestamp, dateTo - datetime timestamp
@app.route('/getFitnessData', methods=['GET'])
def getFitnessData():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    dates_data = check_datetimes(args)
    if dates_data['status_code'] != 200:
        return dates_data['msg'], dates_data['status_code']
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
        db_data = json.dumps(db_data)
        return db_data, 200

# params: token - str
@app.route('/getAllGoals', methods=['GET'])
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
        db_data = json.dumps(db_data)
        return db_data, 200

# params: token - str, type - str
@app.route('/getTypeGoals', methods=['GET'])
def getTypeGoals():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    goal_data = check_goal_type(args)
    if goal_data['status_code'] != 200:
        return goal_type['msg'], goal_type['status_code']
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
        db_data = json.dumps(db_data)
        return db_data, 200

# params: token - str, type - str, value - float
@app.route('/changeGoal', methods=['POST'])
def changeGoal():
    args = request.form
    if not args:
        return "Arguments needed.", 400
    goal_data = check_goal_type(args)
    if goal_data['status_code'] != 200:
        return goal_type['msg'], goal_type['status_code']
    goal_type = goal_data['type']
    goal_val_data = check_goal_value(args)
    if goal_val_data['status_code'] != 200:
        return goal_val_type['msg'], goal_val_type['status_code']
    goal_value = goal_val_data['value']
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 400
    goals = Goals(DB_OBJECT, id)
    success = goals.alter_goal(type, value)
    if not success:
        return "Server Error", 500
    else:
        return 'Successful', 200

def check_goal_value(data):
    if not 'value' in data:
        return {"msg": "Please provide goal value",
                "status_code": 400}
    goal_value = data['value']
    try:
        goal_value = float(goal_value)
    except ValueError:
        return {"msg": "Goal value must be a decimal or integer number",
                "status_code": 400}
    if goal_value < 0:
        return {"msg": "Goal value must be a positive number",
                "status_code": 400}
    return {'value': goal_value, 'status_code': 200}

def check_goal_type(data):
    if not 'type' in data:
        return {"msg": "Please provide goal type",
                "status_code": 400}
    goal_type = data['type']
    options = ["Calories", "FitnessMinutes", "SleepHours"]
    if goal_type not in options:
        return {"msg": f"Goal Type must be one of {options}",
                "status_code": 400}
    return {'type': goal_type, "status_code": 200}

def check_datetimes(data):
    if not 'dateFrom' in data:
        return {"msg": "Please provide 'dateFrom' datetime parameter",
                "status_code": 400}
    if not 'dateTo' in data:
        return {"msg": "Please provide 'dateTo' datetime parameter",
                "status_code": 400}
    try:
        timestamp_from = int(data['dateFrom'])
        timestamp_to = int(data['dateTo'])
        dateFrom = datetime.fromtimestamp(timestamp_from)
        dateTo = datetime.fromtimestamp(timestamp_to)
    except:
        return {'msg': "Please format the dateFrom and dateTo as timestamp objects",
                "status_code": 400}
       
    return {"dateFrom": dateFrom, "dateTo": dateTo,
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
    app.run(host="0.0.0.0", port=5000, debug=False)
