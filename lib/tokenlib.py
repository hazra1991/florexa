import jwt,os
import itsdangerous
from functools import wraps
from datetime import datetime ,timedelta 
from flask import abort,request

SECRET =  "need to take this string to the env var latter "
SECURITY_SALT = "need a salt value to config"

def generate_jwt(u_info):
    print(type(u_info),"    ",u_info)
    try:
        temp =  dict(u_info)
        temp["exp"] = datetime.utcnow() + timedelta(seconds=120)
        return jwt.encode(temp,SECRET,algorithm='HS256')
    except Exception as e:
        print("idisusbdsjdbakjdbakjdbajsdbajsdbakkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        print(e)


def login_required(fun):
    @wraps(fun)
    def wrapper(*args,**kwargs):
        token = request.headers.get('x-access-token')
        try:
            if token is not None:
                info = jwt.decode(token,SECRET,algorithm='HS256')
                return fun(info,*args,**kwargs)
            else:
                abort(403)
        except jwt.exceptions.ExpiredSignatureError:
            abort(403)
        except jwt.exceptions.DecodeError:
            abort(400)
    return wrapper

def generate_url_token(data):
    serializer =  itsdangerous.URLSafeTimedSerializer(SECRET)
    web_token =  serializer.dumps(data,salt=SECURITY_SALT)
    return web_token

def verify_and_geturldata_else_False(url_token,exp_timedelta:"in seconds" = 10):
    try:
        deserializer = itsdangerous.URLSafeTimedSerializer(SECRET)
        data = deserializer.loads(url_token,salt=SECURITY_SALT,max_age=exp_timedelta)
    except (itsdangerous.exc.SignatureExpired,itsdangerous.exc.BadTimeSignature):
        return False
    return data

