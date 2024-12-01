from flask import Flask, request, render_template
from flask_cors import CORS
from flask import make_response
from .views import *


api = Flask(__name__)
CORS(api, supports_credentials=True)

@api.route('/pyxl/write', methods=['PATCH'])
def update():
    if request.method == 'PATCH' :
        data = write_file(request.json)
        return make_response(data, 200)
    else: make_response("Not found", 404)

@api.route('/pyxl/read', methods=['POST'])
def read():
    if request.method == 'POST':
        data = read_file(request.json)
        return make_response(data, 200)
    else: make_response("Not found", 404)

@api.route('/api')
def index():
    return render_template('options.html')

@api.route('/api/read')
def read_front():
    return render_template('read.html')

@api.route('/api/write')
def write_front():
    return render_template('write.html')