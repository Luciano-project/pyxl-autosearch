from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
from flask import make_response
from flask_swagger_ui import get_swaggerui_blueprint
from .views import *


api = Flask(__name__)
CORS(api, supports_credentials=True)

# Swagger UI setup
SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI
API_SPEC_URL = '/static/swagger.yaml'  # Path to your Swagger YAML file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_SPEC_URL,
    config={'app_name': "PYXL - API"}
)
api.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
#

@api.route('/pyxl/write', methods=['PATCH'])
def write():
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


# Frontend routes
@api.route('/')
def home():
    return redirect('/api')

@api.route('/api')
def index():
    return render_template('options.html')

@api.route('/api/read')
def read_front():
    return render_template('read.html')

@api.route('/api/write')
def write_front():
    return render_template('write.html')