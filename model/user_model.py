# can use mongoengine for modeling latter
# https://gist.github.com/fatiherikli/4350345

from lib.mongomodel.models import DocumentModel
from lib.mongomodel.datatypes import Email ,StringField,Date ,EmbeddedDocumentList

from datetime import datetime

class UserSchema(DocumentModel):
    __database__ ="user"
    __collection__="user_info"
    __schema__ ={
        "email_id":Email(unique=True),
        "first_name":DocumentModel.fieldtype(str,bool),
        "middle_name":DocumentModel.fieldtype(str,canbenull=True),
        "last_name":DocumentModel.fieldtype(str),
        "password":DocumentModel.fieldtype(str),
        "phone":DocumentModel.fieldtype(int),
        "location":DocumentModel.fieldtype(str,optional=True),
        "verified":DocumentModel.fieldtype(bool),
        "verified_on":DocumentModel.fieldtype(str,canbenull=True),
        "DOB":{
            "year":StringField(default=datetime.now,canbenull=True),
            "month":DocumentModel.fieldtype(int,canbenull=True),
            "day":DocumentModel.fieldtype(int)
        }
    }
    

