from typing import Tuple
from flask import Flask, make_response, request
import dbhelpers as dh
import apihelper as a
import json
import dbcreds as d

app = Flask(__name__)

@app.post('/api/painting')

def add_painting():
    artist = request.json.get('artist')
    date_painted = request.json.get('date_painted')
    name = request.json.get('name')
    img_url = request.json.get('img_url')
    valid_check = a.check_endpoint_info(request.json, ['artist', 'date_painted', 'name', 'img_url'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)
    result = dh.run_statement('CALL add_new_painting(?,?,?,?)', [artist, date_painted, name, img_url])
    if(type(result) == list):
        # using make response to make it easier for me to debug
        # http response 200 = success, 400 = connection problem
        return make_response(json.dumps(result, default=str), 200)
      
    else:
        return make_response(json.dumps(result, default=str), 400)

@app.get('/api/painting')

def all_painting_by_artist():
    artist = request.args.get('artist')
    valid_check = a.check_endpoint_info(request.args, ['artist'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result = dh.run_statement('CALL show_all_painting_by_artist(?)', [artist])
    if(type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)



if(d.production_mode == True):
    print("Running in Production Mode")
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)