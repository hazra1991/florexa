from functools import wraps
from datetime import datetime ,timedelta 
import jwt,os,copy
from flask import abort,request

SECRET =  "need to take this string to the env var latter "

def generate_jwt(u_info):
    temp =  copy.deepcopy(u_info)
    temp["exp"] = datetime.utcnow() + timedelta(seconds=120)
    return jwt.encode(temp,SECRET,algorithm='HS256')


def verify_jwt(fun):
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