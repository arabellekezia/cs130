from flask import Flask, request
import requests
from staywell_api import StaywellExternalAPI

app = Flask(__name__)

@app.route('/')
def index():
    return 'Better You'

# example: http://localhost:5000/staywell?weight=130&workout=Bowling&minutes=30&user=1
@app.route('/staywell')
def staywell():
    args = request.args
    if not args:
        return "Arguments needed.", 400
    api = StaywellExternalAPI()
    return api.staywell(args)


if __name__ == '__main__':
	app.run(host="localhost", port=5000, debug=False)
