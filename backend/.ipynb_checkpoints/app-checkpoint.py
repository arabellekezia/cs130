from flask import Flask, request
import requests

app = Flask(__name__)
staywellAPI = ("http://poc.select.kramesstaywell.com/Content/calculators-v1/"
               "calorie-burn-rate-calculator")

@app.route('/')
def index():
    return 'Better You'

@app.route('/staywell')
def staywell():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    weight_param = check_weight(args)
    if weight_param['status_code'] != 200:
        return weight_param['msg'], weight_param['status_code']
    else:
        weight = weight_param['weight']
    params = {'CalorieBurnCalc_Parameters': weight}
    # this API is stupid so I need to write a class to basically reimplement their code :(
    r  = requests.get(url=staywellAPI, params=params)
    if not r:
        return "Staywell API error", 500
    if int(r.status_code) != 200:
        return "Staywell API error", 500
    print(r.text)
    return "tbd"

def check_weight(data):
    if 'weight' in data:
        weight = data['weight']
        try:
            weight = int(weight)
            return {"status_code": 200, "weight": weight}
        except ValueError:
            return {"msg": "Please enter an integer for weight",
                    "status_code": 400}
    else:
        return {"msg": "Please enter a weight",
                "status_code": 400}

if __name__ == '__main__':
	app.run(host="localhost", port=5000, debug=False)
