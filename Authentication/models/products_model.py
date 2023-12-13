import mysql.connector
import json
from flask import make_response
import jwt
from datetime import datetime, timedelta
from config.config import db_confog

class user_model:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host=db_confog['host'], user=db_confog['user'], password = db_confog['password'], database=db_confog['database'])
            self.conn.autocommit = True
            self.cur =  self.conn.cursor(dictionary=True)
        except:
            print('some error')
    def user_signup_model(self):
        self.cur.execute("select * from users ")
        result1 = self.cur.fetchall()
        if len(result1) > 0 :
            # result = json.dumps(result1)
            result = result1
            # print('Len :', len(result))
            # print('Type :', type(result))
            # print('result :', result)
          
            # return  result
            res = make_response({"payload" : result}, 200)
            # print('res :', res)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return  res
        else:
            return  make_response({"message" :  "No Data Found"}, 204)
        
    def user_addone_model(self, mydata):
        # self.cur.execute("select * from users")
        print('request.form : ',  mydata)
        self.cur.execute(f"insert into users (name,email,phone,roles,password) values ('{mydata['name']}','{mydata['email']}','{mydata['phone']}','{mydata['roles']}','{mydata['password']}')")
        # print('request.form : ',  query)
        return make_response( {"message" : "User created successfully"}, 200)
    
        
    def user_login_model(self,user_info):
        self.cur.execute(f"select id,name,email, roles, phone from users where email = '{user_info['email']}' and password =  '{user_info['passsword']}' ")
        result1 = self.cur.fetchall()
        if len(result1) > 0 :
            user_date = result1[0]
            exp_time =  datetime.now() + timedelta( minutes= 15)
            exp_epoch_time = exp_time.timestamp()
            payload = {
                "payload" : user_date,
                "exp" : exp_epoch_time
            }
            jwt_token = jwt.encode(payload,'secret',algorithm="HS256")
            print(int(exp_epoch_time))
            # return  result1
            # return  str(result1)
            return  make_response({'payload' : jwt_token}, 200)
        else:
            return  make_response({"message" :  "No Data Found"}, 204)
        
   