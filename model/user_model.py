# can use pymodm 0.4.3 for modeling latter
# https://gist.github.com/fatiherikli/4350345

from lib.token import generate_jwt
from lib.mongomodel import DocumentModel ,PrimaryKey ,Optional

class UserSchema(DocumentModel):
    
    __schema__ = {
        "email_id":[str,PrimaryKey],
        "first_name":[str],
        "middle_name":[str,None],
        "last_name":[str],
        "password":[str],
        "phone":[int],
        "location":[str,Optional],
        "verifyed":[bool],
        "verified_on":[str,None],
        "DOB":[str]
    }

document =  UserSchema({"email_id":"12",
        "first_name":"abhisehk",
        "middle_name":None,
        "last_name":"str",
        "password":"str",
        "phone":9999999999,
        "location":"str",
        "verifyed":False,
        "verified_on":"None",
        "DOB":"str"
        })

document.save()