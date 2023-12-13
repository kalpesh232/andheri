import mysql.connector
import json
from flask import make_response,request
import jwt
from datetime import datetime, timedelta
import re
from config.config import db_confog

class auth_model:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host=db_confog['host'], user=db_confog['user'], password = db_confog['password'], database=db_confog['database'])
            self.conn.autocommit = True
            self.cur =  self.conn.cursor(dictionary=True)
        except:
            print('some error')

    def token_authorization(self,endpoint = ''):
        def inner1(fun):
            def inner2(*args):
                endpoint = request.url_rule
                print('*' * 153)
                print('args', endpoint)
                authorization =  request.headers.get('authorization')
                
                # if re.match(r'^Bearer\s(.+)$', authorization, flags=0):
                token = authorization.split(' ')[1]
                # print(token)
                # decode the token start
                try:
                    decoded_token =  jwt.decode(token,'secret',algorithms="HS256")
                    print('decoded_token :', decoded_token)
                except jwt.ExpiredSignatureError:
                    return make_response({"EOOR":"TOKEN_EXPIRED"}, 401)
                # decode the token end
                decoded_roles =  decoded_token['payload']['roles']
                self.cur.execute(f"select roles from auth_view where emdpoint_names = '{endpoint}' ")
                result =  self.cur.fetchall()
                if len(result) >0 :
                    allowed_roles =  json.loads(result[0]['roles'])
                    print(decoded_roles)
                    print(allowed_roles)
                    if decoded_roles in allowed_roles:
                        return fun(*args)
                    else:
                        return make_response({"ERROR" : "INVALID_ROLE"}, 404)
                else:
                    return make_response({"ERROR" : "UNKNOW_ENDPOIT"}, 404)
                # else:
                #     return make_response({"ERROR" :"INVALID_TOKEN"},401)
            return inner2
        return inner1
        