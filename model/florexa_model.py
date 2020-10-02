# can use mongoengine for modeling latter
# https://gist.github.com/fatiherikli/4350345

from lib.mongomodel.models import DocumentModel
from lib.mongomodel.datatypes import Email,StringField,EmbeddedDocumentList,NumberField,DateTime,Boolean
from datetime import datetime

class UserSchema(DocumentModel):
    __database__ ="florexa"
    __collection__="user_info"
    __schema__ ={
        "email_id":Email(unique=True),
        "first_name":StringField(),
        "middle_name":StringField(canbenull=True),
        "last_name":StringField(),
        "password":StringField(),
        "phone":NumberField(minimum=10,maximum=12),
        "location":StringField(optional=True),
        "verified":Boolean(default=False),
        "verified_on":DateTime(_format="%Y/%m/%d"),
        "DOB":{
            "year":NumberField(),
            "month":NumberField(),
            "day":NumberField()
        }
    }

class Appointments(DocumentModel):
    __database__="florexa"
    __collection__="appointments"
    __schema__= {
        "received_on":DateTime(default=datetime.now),
        "email_id":Email(),
        "first_name":StringField(),
        "middle_name":StringField(canbenull=True),
        "last_name":StringField(),
        "phone":NumberField(minimum=10,maximum=12),
        "confirmed":Boolean(default=False),
        "booking_date":DateTime(_format="%Y/%m/%d"),
        "time_slot":DocumentModel.fieldtype(float),
        "sevices":EmbeddedDocumentList({
                                        "id":DocumentModel.fieldtype(float),
                                        "name":StringField()
                                    })
    }

class Services(DocumentModel):
    __database__ = "florexa"
    __collection__ = "service_info"
    __schema__ = {
        "id":DocumentModel.fieldtype(float,unique=True),
        "name":StringField(),
        "price":DocumentModel.fieldtype(float)
    }


class TimeSlot(DocumentModel):
    __database__ = "florexa"
    __collection__ = "timeslot"
    __schema__= {
        "id":DocumentModel.fieldtype(float,unique=True),
        "time_slot":StringField(),
        "max_booking":NumberField(default=4)
    }
