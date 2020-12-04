from flask import Flask, request
import requests
from datetime import datetime, timezone, timedelta
import json
import sys
from typing import Union, Any, List, Dict, Tuple
from backend.staywell_api import StaywellAPI
from backend.edamam_api import EdamamAPI
from backend.user import User
from backend.db import DB
from backend.Diet import Diet
from backend.Fitness import Fitness
from backend.Sleep import Sleep
from backend.goals import Goals

app = Flask(__name__)
DB_OBJECT = None
USER = None
STAYWELL_API = StaywellAPI()
EDAMAM_API = EdamamAPI()

@app.route('/')
def index():
    return 'Better You'

@app.route('/enterWorkout', methods=['POST'])
def enterWorkout():
    """
    Allows users to enter workout data. If successful, returns the number of
    calories burned and 200 code. Returns error otherwise.

    Parameters
    ----------
    weight : int
        Weight of the user.
    workout : str
        Workout type.
    minutes : float
        Duration the user did the workout for in minutes.
    token : str
        Unique token based on user ID.

    Returns
    -------
    result : Tuple[str, int]
        If successful, the first part of the Tuple corresponds to the calories burned
        by the user based on the Staywell API. Otherwise, it's the HTTP error message.
        The second part of the Tuple corresponds to the HTTP status code.
    """
    args = request.form
    if not args:
        return "Arguments needed.", 400
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 401
    return STAYWELL_API.staywell(args, id, DB_OBJECT)

@app.route('/getNutritionalData', methods=['GET'])
def getNutritionalData():
    """
    Search nutritional data for a certain food item given its name or barcode.
    If successful, returns the number of
    calories burned and 200 code. Returns error otherwise.

    Parameters
    ----------
    item : Union[str, int]
        Item name in string or barcode number if user scans a barcode.
    barcode : Optional[bool]
        True if user scans barcode, False otherwise.
    ServingSize : float
        Serving size of the item.

    Returns
    -------
    result : Tuple[Any, int]
        If successful, the first part of the tuple gives a dict containing the nutritional
        data of the given food item. Otherwise, it gives an error message.
        The second part of the tuple gives the HTTP status code.
    """
    args = request.args
    if not args:
        return "Arguments needed.", 400
    if not 'item' in args:
        return "The 'item' is a required parameter", 400
    item = args['item']
    barcode = False
    if 'barcode' in args and args['barcode'].upper() == "TRUE":
        barcode = True
    if not 'ServingSize' in args:
        return "The 'ServingSize' is a required parameter", 400
    serving_size = args['ServingSize']
    try:
        serving_size = float(serving_size)
    except ValueError:
        return "The 'ServingSize' must be a float or int", 400
    food_dict, success = EDAMAM_API.get_top_matches(item, barcode, 1, serving_size)
    if not success:
        return "Unable to find the food item based on given info", 400
    else:
        food_dict = json.dumps(food_dict)
        return food_dict, 200

@app.route('/getAvailableFoods', methods=['GET'])
def getAvailableFoods():
    """
    Uses the Edamam API to search available foods given item name or barcode.

    Parameters
    ----------
    item : Union[str, int]
        Item name in string or barcode number if user scans a barcode.
    barcode : Optional[bool]
        True if user scans barcode, False otherwise. Defaults to False.
    nMatches : Optional[int]
        Number of food matches from the API. Defaults to 5.
    ServingSize : float
        Serving size of the item.

    Returns
    -------
    result : Tuple[Any, int]
        If successful, the first part of the tuple gives a dict containing
        matches of the given food item. Otherwise, it gives an error message.
        The second part of the tuple gives the HTTP status code.
    """
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
    if not 'ServingSize' in args:
        return "The 'ServingSize' is a required parameter", 400
    serving_size = args['ServingSize']
    try:
        serving_size = float(serving_size)
    except ValueError:
        return "The 'ServingSize' must be a float or int", 400
    food_dict, success = EDAMAM_API.get_top_matches(item, barcode, n, serving_size)
    if not success:
        return "Unable to find the food item based on given info", 400
    else:
        food_dict = json.dumps(food_dict)
        return food_dict, 200

@app.route('/auth/login', methods=['POST'])
def login():
    """
    Login method using user's email and password.

    Parameters
    ----------
    email : str
        User's email.
    password : str
        User's password.

    Returns
    -------
    result : Tuple[str, int]
        If successful, the first part of the tuple is the User's payload encoding.
        Otherwise, it gives HTTP error message. The second part of the tuple is the
        HTTP status code.
    """
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

@app.route('/register', methods=['POST'])
def register():
    """
    Register new user.

    Parameters
    ----------
    email : str
        User's email.
    password : str
        User's password.
    fullname : str
        User's full name.

    Returns
    -------
    result : Tuple[str, int]
        The first part gives HTTP error message. The second part of the tuple is the
        HTTP status code.
    """
    args = request.form
    if not args:
        return "Arguments needed.", 400
    if not 'email' in args:
        return "The 'email' is a required parameter", 400
    email = args['email']
    if not 'password' in args:
        return "The 'password' is a required parameter", 400
    password = args['password']
    if not 'fullname' in args:
        return "The 'fullname' is a required parameter", 400
    fullname = args['fullname']
    if USER.create_new_user(email, password, fullname):
        id = USER.check_password_match(email, password)
        if id < 0:
            "Unable to find registered user.", 500
        goals = Goals(DB_OBJECT, id)
        diet_goal = {'Type': 'Calories', 'Value': 2000.0}
        fitness_goal = {'Type': 'FitnessMinutes', 'Value': 30.0}
        sleep_goal = {'Type': 'SleepHours', 'Value': 7.0}
        goals.set_goal(diet_goal)
        goals.set_goal(fitness_goal)
        goals.set_goal(sleep_goal)
        return "Succesfully Registered", 200
    else:
        return "Unable to register new user, they possibly already have an account", 400

@app.route('/getMeals', methods=['GET'])
def getMeals():
    """
    Fetch all logged meals from database given a time period.

    Parameters
    ----------
    token : str
        Unique token based on user ID.
    dateFrom : timestamp
        Start date of the data that wants to be fetched.
    dateTo : timestamp
        End date of the data that wants to be fetched.

    Returns
    -------
    result : Tuple[Any, int]
        If successful, the first part of the tuple gives a dict containing the meal data
        for the given time period. Otherwise, it gives an error message.
        The second part of the tuple gives the HTTP status code.
    """
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
        return "Invalid Token", 401
    diet = Diet(DB_OBJECT, id)
    db_data, success = diet.get_columns_given_range(dateFrom, dateTo)
    if not success:
        if db_data == -1:
            return "Server Error", 500
        else:
            return json.dumps([]), 200
    else:
        db_data = json.dumps(db_data)
        return db_data, 200

@app.route('/addMeal', methods=['POST'])
def addMeal():
    """
    Log meal and add it to database.

    Parameters
    ----------
    token : str
        Unique token based on user ID.
    item : Union[str, int]
        Food item name or barcode.
    ServingSize : float
        Serving size of the food consumed.
    barcode : Optional[bool]
        True if user scans barcode, False otherwise.

    Returns
    -------
    result : Tuple[str, int]
        The first part gives HTTP error message. The second part of the tuple is the
        HTTP status code.
    """
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
    food_dict, success = EDAMAM_API.get_top_matches(item, barcode, 1, serving_size)
    if not success:
        return "Unable to find the food item based on given info", 400
    label = food_dict[0]['Label']
    food_dict = food_dict[0]['Nutrients']
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 401
    insert_food_dict = {'Item': label, 'ServingSize': serving_size, 'Barcode': barcode}
    nutri_dict = {}
    for k, v in food_dict.items():
        nutri_dict[k] = v
    insert_food_dict['nutri_dict'] = nutri_dict
    diet = Diet(DB_OBJECT, id)
    success = diet.insert_in_database(insert_food_dict)
    if not success:
        return "Server Error", 500
    else:
        return "Successful", 200

@app.route('/getSleepData', methods=['GET'])
def getSleepData():
    """
    Fetch all logged sleep periods from database given a time period.

    Parameters
    ----------
    token : str
        Unique token based on user ID.
    dateFrom : timestamp
        Start date of the data that wants to be fetched.
    dateTo : timestamp
        End date of the data that wants to be fetched.

    Returns
    -------
    result : Tuple[Any, int]
        If successful, the first part of the tuple gives a dict containing the sleep data
        for the given time period. Otherwise, it gives an error message.
        The second part of the tuple gives the HTTP status code.
    """
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
        return "Invalid Token", 401
    sleep = Sleep(DB_OBJECT, id)
    db_data, success = sleep.get_columns_given_range(dateFrom, dateTo)
    if not success:
        if db_data == -1:
            return "Server Error", 500
        else:
            return json.dumps([]), 200
    else:
        db_data = json.dumps(db_data)
        return db_data, 200

@app.route('/insertSleepEntry', methods=['POST'])
def insertSleepEntry():
    """
    Log meal and add it to database.

    Parameters
    ----------
    token : str
        Unique token based on user ID.
    dateFrom : timestamp
        User's sleep time.
    dateTo : timestamp
        User's wake up time.
    nap : Optional[bool]
        If this entry is a nap, defaults to False for not a nap.

    Returns
    -------
    result : Tuple[str, int]
        The first part gives HTTP error message. The second part of the tuple is the
        HTTP status code.
    """
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
        return "Invalid Token", 401
    Nap = False
    if 'nap' in args and args['nap'].upper() == 'TRUE':
        Nap = True
    sleep = Sleep(DB_OBJECT, id)
    success = sleep.insert_in_database({'SleepTime': SleepTime, 'WakeupTime': WakeupTime, 'Nap': Nap})
    if not success:
        return "Server Error", 500
    else:
        return 'Successful', 200

@app.route('/getFitnessData', methods=['GET'])
def getFitnessData():
    """
    Fetch all logged fitness data from database given a time period.

    Parameters
    ----------
    token : str
        Unique token based on user ID.
    dateFrom : timestamp
        Start date of the data that wants to be fetched.
    dateTo : timestamp
        End date of the data that wants to be fetched.

    Returns
    -------
    result : Tuple[Any, int]
        If successful, the first part of the tuple gives a dict containing the fitness data
        for the given time period. Otherwise, it gives an error message.
        The second part of the tuple gives the HTTP status code.
    """
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
        return "Invalid Token", 401
    fitness = Fitness(DB_OBJECT, id)
    db_data, success = fitness.get_columns_given_range(dateFrom, dateTo)
    if not success:
        if db_data == -1:
            return "Server Error", 500
        else:
            return json.dumps([]), 200
    else:
        db_data = json.dumps(db_data)
        return db_data, 200

@app.route('/getAllGoals', methods=['GET'])
def getAllGoals():
    """
    Fetch all of the user's set goals.

    Parameters
    ----------
    token : str
        Unique token based on user ID.

    Returns
    -------
    result : Tuple[Any, int]
        If successful, the first part of the tuple gives a dict containing
        all of the user's goals. Otherwise, it gives an error message.
        The second part of the tuple gives the HTTP status code.
    """
    args = request.args
    if not args:
        return "Arguments needed.", 400
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 401
    goals = Goals(DB_OBJECT, id)
    db_data, success = goals.get_all_goals()
    if not success:
        if db_data == -1:
            return "Server Error", 500
        else:
            return json.dumps([]), 200
    else:
        db_data = json.dumps(db_data)
        return db_data, 200

@app.route('/getTypeGoals', methods=['GET'])
def getTypeGoals():
    """
    Fetch a certain goal given the type.

    Parameters
    ----------
    token : str
        Unique token based on user ID.
    type : str
        Type of goal we want to fetch.
        Available options are: 'FitnessMinutes', 'Calories', 'SleepHours'

    Returns
    -------
    result : Tuple[Any, int]
        If successful, the first part of the tuple gives a dict containing
        all of the user's goals. Otherwise, it gives an error message.
        The second part of the tuple gives the HTTP status code.
    """
    args = request.args
    if not args:
        return "Arguments needed.", 400
    goal_data = check_goal_type(args)
    if goal_data['status_code'] != 200:
        return goal_data['msg'], goal_data['status_code']
    goal_type = goal_data['type']
    token = check_token(args)
    if token['status_code'] != 200:
        return token['msg'], token['status_code']
    token = token['token']
    id = getIdFromToken(token)
    if id < 0:
        return "Invalid Token", 401
    goals = Goals(DB_OBJECT, id)
    db_data, success = goals.get_type_goals(goal_type)
    if not success:
        if db_data == -1:
            return "Server Error", 500
        else:
            return json.dumps([]), 200
    else:
        db_data = json.dumps(db_data)
        return db_data, 200

@app.route('/changeGoal', methods=['POST'])
def changeGoal():
    """
    Change a specific goal.

    Parameters
    ----------
    token : str
        Unique token based on user ID.
    type : str
        Type of goal we want to change.
        Available options are: 'FitnessMinutes', 'Calories', 'SleepHours'
    value : float
        Value of the user's new goal.

    Returns
    -------
    result : Tuple[str, int]
        The first part gives HTTP error message. The second part of the tuple is the
        HTTP status code.
    """
    args = request.form
    if not args:
        return "Arguments needed.", 400
    goal_data = check_goal_type(args)
    if goal_data['status_code'] != 200:
        return goal_data['msg'], goal_data['status_code']
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
        return "Invalid Token", 401
    goals = Goals(DB_OBJECT, id)
    success = goals.alter_goal(goal_type, goal_value)
    if not success:
        return "Server Error", 500
    else:
        return 'Successful', 200

def check_goal_value(data):
    """
    Helper function for changeGoal method. Checks current goal given type.

    Parameters
    ----------
    data : Dict[Any]
        Type of goal we want to check.
        Available options are: 'FitnessMinutes', 'Calories', 'SleepHours'

    Returns
    -------
    result : Tuple[str, int]
        If successful, the first part gives the type of goal we are checking.
        Otherwise, it gives an eror message. The second part of the tuple is the
        HTTP status code.
    """
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
    """
    Helper function that checks validity of the goal type passed in.

    Parameters
    ----------
    data : Dict[Any]
        Data dictionary containing the type of goal passed in.
        Available options are: 'FitnessMinutes', 'Calories', 'SleepHours'

    Returns
    -------
    result : Tuple[str, int]
        If successful, the first part gives the type of goal we are checking.
        Otherwise, it gives an eror message. The second part of the tuple is the
        HTTP status code.
    """
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
    """
    Helper function that checks datetime formatting.

    Parameters
    ----------
    data : Dict[Any]
        Dictionary containing dateFrom and dateTo dates.

    Returns
    -------
    result : Union[Dict[datetime, datetime, int], Dict[str, int]]
        If successful, returns a dict containing the converted datetime values
        for dateTo and dateFrom, and HTTP status code. Otherwise, returns dict
        containing HTTP error message and status code.
    """
    if not 'dateFrom' in data:
        return {"msg": "Please provide 'dateFrom' datetime parameter",
                "status_code": 400}
    if not 'dateTo' in data:
        return {"msg": "Please provide 'dateTo' datetime parameter",
                "status_code": 400}
    try:
        timestamp_from = float(data['dateFrom'])
        timestamp_to = float(data['dateTo'])
        dateFrom = datetime.fromtimestamp(timestamp_from) + timedelta(hours=8);
        dateTo = datetime.fromtimestamp(timestamp_to) + timedelta(hours=8);
    except:
        return {'msg': "Please format the dateFrom and dateTo as timestamp objects",
                "status_code": 400}

    return {"dateFrom": dateFrom, "dateTo": dateTo,
            "status_code": 200}

def check_token(data):
    """
    Helper function that checks user's token.

    Parameters
    ----------
    data : Dict[Any]
        Dictionary containing user's token that needs to be checked.

    Returns
    -------
    result : Union[Dict[int, int], Dict[str, int]]
        If successful, returns dictionary of the HTTP status code and user token.
        Otherwise, returns dictionary of HTTP error message and status code.
    """
    if 'token' in data:
        token = data['token']
        return {"status_code": 200, "token": token}
    else:
        return {"msg": "Please provide a token",
                "status_code": 400}

def getIdFromToken(token):
    """
    Helper function that gets user's ID given token.

    Parameters
    ----------
    token : str
        Unique user token.

    Returns
    -------
    result : int
        If successful, returns user ID. Otherwise, returns -1.
    """
    msg, code = USER.decode_token(token)
    if code != 200:
        return -1
    return int(msg)


if __name__ == '__main__':
    test = False
    try:
        test = sys.argv[1]
        test = bool(test)
    except:
        test = False

    print(test)
    DB_OBJECT = DB(test)
    USER = User(DB_OBJECT)

    app.run(host="0.0.0.0", port=5000, debug=False)
