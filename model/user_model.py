# can use pymodm 0.4.3 for modeling latter
# https://gist.github.com/fatiherikli/4350345

from lib.mongomodel import DocumentModel ,Email

class UserSchema(DocumentModel):
    __database__ ="florexa"
    __collection__="user_info"
    __schema__ = {
        "email_id":DocumentModel.fieldtype(Email,str,unique=True),
        "first_name":DocumentModel.fieldtype(str),
        "middle_name":DocumentModel.fieldtype(str,None,optional=True),
        "last_name":DocumentModel.fieldtype(str),
        "password":DocumentModel.fieldtype(str),
        "phone":DocumentModel.fieldtype(int),
        "location":DocumentModel.fieldtype(str,optional=True),
        "verifyed":DocumentModel.fieldtype(bool),
        "verified_on":DocumentModel.fieldtype(str,int,None),
        "DOB":DocumentModel.fieldtype(str,int)
    }

# print(type(UserSchema),UserSchema.__mro__)
