# can use pymodm 0.4.3 for modeling latter
# https://gist.github.com/fatiherikli/4350345

from lib.mongomodel import DocumentModel ,Email

class UserSchema(DocumentModel):
    __database__ ="florexa"
    __collection__="user_info"
    __schema__ ={
        "email_id":DocumentModel.fieldtype(str),
        "first_name":DocumentModel.fieldtype(str),
        "middle_name":DocumentModel.fieldtype(str,None,optional=True),
        "last_name":DocumentModel.fieldtype(str),
        "password":DocumentModel.fieldtype(str),
        "phone":DocumentModel.fieldtype(int),
        "location":DocumentModel.fieldtype(str,optional=True),
        "verified":DocumentModel.fieldtype(bool),
        "verified_on":DocumentModel.fieldtype(None),
        "DOB":{
            "year":DocumentModel.fieldtype(int),
            "month":DocumentModel.fieldtype(int),
            "day":DocumentModel.fieldtype(int)
    }
    }

