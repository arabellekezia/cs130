from typing import Any, Dict, Tuple
from backend.db import DB
from backend.Fitness import Fitness

# source: http://poc.select.kramesstaywell.com/Content/calculators-v1/calorie-burn-rate-calculator
# code/values/workout types come from this website however they only provided HTML and not JSON data
# so I made this script to do the same functionality as the website linked

class StaywellExternalAPI:
    def __init__(self) -> None:
        self._workout_list = ['Aerobics, step: high impact',
                              'Aerobics, step: low impact',
                              'Aerobics: high impact',
                              'Aerobics: low impact',
                              'Aerobics: water',
                              'Basketball: game',
                              'Basketball: wheelchair',
                              'Bicycling, stationary: moderate',
                              'Bicycling, stationary: vigorous',
                              'Bicycling: 20 mph',
                              'Bicycling: 12-13.9 mph',
                              'Bicycling: 14-15.9 mph',
                              'Bicycling: 16-19 mph',
                              'Bicycling: BMX/mountain',
                              'Bowling',
                              'Boxing: sparring',
                              'Calisthenics: moderate',
                              'Calisthenics: vigorous',
                              'Chopping/splitting wood',
                              'Circuit training',
                              'Dancing: disco, ballroom, square',
                              'Dancing: fast, ballet, twist',
                              'Dancing: slow, waltz, foxtrot',
                              'Elliptical',
                              'Football: competitive',
                              'Football: touch, flag',
                              'Gardening',
                              'Golf: carrying clubs',
                              'Golf: using cart',
                              'Gymnastics',
                              'Handball',
                              'Health rider',
                              'Heavy cleaning: car, windows',
                              'Hiking: cross country',
                              'Hockey: field and ice',
                              'Ice skating',
                              'Kayaking',
                              'Martial arts: karate, kickboxing',
                              'Moving: carrying boxes',
                              'Mowing lawn: push, hand',
                              'Mowing lawn: push, power',
                              'Operate snow blower: walking',
                              'Racquetball: casual',
                              'Racquetball: competitive',
                              'Raking lawn',
                              'Rollerblade: skating',
                              'Rope jumping',
                              'Rowing, stationary: moderate',
                              'Rowing, stationary: vigorous',
                              'Running: 6 min/mile',
                              'Running: 8 min/mile',
                              'Running: 10 min/mile',
                              'Running: 12 min/mile',
                              'Scuba or skin diving',
                              'Shoveling snow: by hand',
                              'Sitting: reading, watching TV',
                              'Skateboarding',
                              'Skiing: downhill',
                              'Ski machine',
                              'Sleeping',
                              'Snow shoeing',
                              'Soccer',
                              'Softball',
                              'Stair-step machine',
                              'Stretching, yoga',
                              'Swimming: general',
                              'Swimming: laps, vigorous',
                              'Tai chi',
                              'Tennis',
                              'Walk/Jog: jog<10 min.',
                              'Walk: 15 min/mile',
                              'Water polo',
                              'Water skiing',
                              'Water volleyball',
                              'Weightlifting: general',
                              'Weightlifting: vigorous',
                              'Whitewater: rafting, kayaking',
                              'Wrestling',
                              'Volleyball: beach',
                              'Volleyball general play']

    def staywell(self, args: Dict[str, Any], userID: int, db: DB) -> Tuple[str, int]:
        if not args:
            return "Arguments needed.", 400
        weight_param = self._check_weight(args)
        if weight_param['status_code'] != 200:
            return weight_param['msg'], weight_param['status_code']
        else:
            weight = weight_param['weight']
        workout_param = self._check_workout_type(args)
        if workout_param['status_code'] != 200:
            return workout_param['msg'], workout_param['status_code']
        else:
            workout = workout_param['workout']
        mins_param = self._check_minutes(args)
        if mins_param['status_code'] != 200:
            return mins_param['msg'], mins_param['status_code']
        else:
            mins = mins_param['minutes']

        calories = self._get_exact_calories(weight, workout, mins)
        fitness_dict = {'WorkoutType': workout, 'Minutes': mins, 'CaloriesBurned': calories}

        fitness = Fitness(db, userID)
        success = fitness.insert_in_database(fitness_dict)
        if not success:
            return "Server Error", 500
        return str(calories), 200

    def _get_calories_list_per_hour(self, weight: int) -> int:
        calories_for_exercise = []
        if weight < 113:
            calories_for_exercise = [480, 336, 336, 264, 192, 384, 312, 336, 504, 792, 384, 480,
                                     576, 408, 144, 432, 216, 384, 288, 384, 264, 288, 144, 432,
                                     432, 384, 216, 264, 168, 192, 576, 240, 216, 288, 384, 336,
                                     240, 480, 336, 264, 216, 216, 336, 480, 192, 336, 480, 336,
                                     408, 792, 600, 480, 384, 336, 288, 54, 240, 288, 456, 30,
                                     384, 336, 240, 288, 192, 288, 480, 192, 336, 288, 216, 480,
                                     288, 144, 144, 288, 240, 288, 384, 144]
        elif weight > 112 and weight < 138:
            calories_for_exercise = [600, 420, 420, 330, 240, 480, 390, 420, 630, 990, 480, 600,
                                     720, 510, 180, 540, 270, 480, 360, 480, 330, 360, 180, 540,
                                     540, 480, 270, 330, 210, 240, 720, 300, 270, 360, 480, 420,
                                     300, 600, 420, 330, 270, 270, 420, 600, 240, 420, 600, 420,
                                     510, 990, 750, 600, 480, 420, 360, 68, 300, 360, 570, 38,
                                     480, 420, 300, 360, 240, 360, 600, 240, 420, 360, 270, 600,
                                     360, 180, 180, 360, 300, 360, 480, 180]
        elif weight > 137 and weight < 163:
            calories_for_exercise = [720, 504, 504, 396, 288, 576, 468, 504, 756, 1188, 576, 720,
                                     864, 612, 216, 648, 324, 576, 432, 576, 396, 432, 216, 648,
                                     648, 576, 324, 396, 252, 288, 864, 360, 324, 432, 576, 504,
                                     360, 720, 504, 396, 324, 324, 504, 720, 288, 504, 720, 504,
                                     612, 1188, 900, 720, 576, 504, 432, 81, 360, 432, 684, 45,
                                     576, 504, 360, 432, 288, 432, 720, 288, 504, 432, 324, 720,
                                     432, 216, 216, 432, 360, 432, 576, 216]
        elif weight > 162 and weight < 188:
            calories_for_exercise = [840, 588, 588, 462, 336, 672, 546, 588, 882, 1386, 672, 840,
                                     1008, 714, 252, 756, 378, 672, 504, 672, 462, 504, 252, 756,
                                     756, 672, 378, 462, 294, 336, 1008, 420, 378, 504, 672, 588,
                                     420, 840, 588, 462, 378, 378, 88, 840, 336, 588, 840, 588,
                                     714, 1386, 1050, 840, 672, 588, 504, 95, 420, 504, 798, 53,
                                     672, 588, 420, 504, 336, 504, 840, 336, 588, 504, 378, 840,
                                     504, 252, 252, 504, 420, 504, 672, 252]
        else:
            calories_for_exercise = [960, 672, 672, 528, 384, 768, 624, 672, 1008, 1584, 768, 960,
                                     1152, 816, 288, 864, 432, 768, 576, 768, 528, 576, 288, 864,
                                     864, 768, 432, 528, 336, 384, 1152, 480, 432, 576, 768, 672,
                                     480, 960, 672, 528, 432, 432, 672, 960, 384, 672, 960, 672,
                                     816, 1584, 1200, 960, 768, 672, 576, 108, 480, 576, 912, 60,
                                     768, 672, 480, 576, 384, 576, 960, 384, 672, 576, 432, 960,
                                     576, 288, 288, 576, 480, 576, 768, 288]
        return calories_for_exercise

    def _get_exact_calories(self, weight: int, workout: str, minutes: float) -> float:
        calories_for_exercise = self._get_calories_list_per_hour(weight)
        index = self._workout_list.index(workout)
        calories_per_min = calories_for_exercise[index] / 60
        return (minutes*calories_per_min)

    def _check_weight(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if 'weight' in data:
            weight = data['weight']
            try:
                weight = int(weight)
            except ValueError:
                return {"msg": "Please enter an integer for weight",
                        "status_code": 400}
            if weight < 0:
                return {"msg": "Please enter an positive integer for weight",
                        "status_code": 400}
            else:
                return {"status_code": 200, "weight": weight}
        else:
            return {"msg": "Please enter a weight",
                    "status_code": 400}

    def _check_workout_type(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if 'workout' in data:
            workout = data['workout']
            if workout in self._workout_list:
                return {"status_code": 200, "workout": workout}
            else:
                return {"msg": "Please enter a valid workout",
                        "status_code": 400}
        else:
            return {"msg": "Please enter a workout",
                    "status_code": 400}

    def _check_minutes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if 'minutes' in data:
            mins = data['minutes']
            try:
                mins = float(mins)
            except ValueError:
                return {"msg": "Please enter an integer for minutes of the workout duration.",
                        "status_code": 400}
            if mins < 0:
                return {"msg": "Please enter a positive integer for minutes of the workout duration.",
                        "status_code": 400}
            else:
                return {"status_code": 200, "minutes": mins}
        else:
            return {"msg": "Please enter a workout duration in minutes",
                    "status_code": 400}

