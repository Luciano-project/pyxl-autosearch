from flask import Flask, request
from flask_cors import CORS
from flask import make_response


api = Flask(__name__)
CORS(api, supports_credentials=True)

@api.route('/pyxl/update', methods=['POST'])
def update():
    if request.method == 'POST' :
        print("POST")
        return 200
    
    else: make_response("Method not allowed", 405)

@api.route('/pyxl/read', methods=['POST'])
def read():
    if request.method == 'POST' :
        print("POST")
        return 200
    
    else: make_response("Method not allowed", 405)