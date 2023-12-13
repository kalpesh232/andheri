
from app import app
from models.products_model import user_model
from models.auth_model import auth_model
from flask import request, send_file
from datetime import datetime
import os

obj = user_model()
auth = auth_model()

@app.route('/get_all')
@auth.token_authorization()
def product():
    # return "product"
    return obj.user_signup_model()

@app.route('/addone', methods=['POST'])
def addone():
    # return "product"
    print('-------->', request.form)
    return obj.user_addone_model(request.form)

@app.route('/login', methods=['POST'])
def user_login_controller():
    return obj.user_login_model(request.form)

