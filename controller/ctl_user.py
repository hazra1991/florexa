from passlib.hash import pbkdf2_sha256
from lib.token import generate_jwt
from lib.mongomodel import Errors
from model.user_model import UserSchema

class NoUserFound(Exception):
    pass

class InvalidPass(Exception):
    pass

class User:
    # client =  pymongo.MongoClient()
    @classmethod
    def verify_and_get_Token(cls,email_id,password):
        UserSchema.connect()
        userdocObj = UserSchema()
        u_info =  userdocObj.florexa.user_info.findone({"email_id":email_id})
        if u_info is not None:
            u_info['_id'] = str(u_info["_id"])
            if pbkdf2_sha256.verify(password,u_info["password"]):
                u_info.pop('password')
                return (generate_jwt(u_info),u_info)
            else:
                raise InvalidPass("password incorrect")
        else:
            raise NoUserFound

    @classmethod
    def register_user(cls,user_data):
        UserSchema.connect()
        try:
            user_data["password"] = pbkdf2_sha256.hash(user_data["password"])
            userdocObj = UserSchema(user_data)
            print(userdocObj)
            temp = userdocObj.florexa.user_info.insert()
            print(" MA HERERERE")
            return True
        except Errors.DuplicateKeyErr as e:
            return (409,"Email id already registered,Please login",e)
        except Errors.SchemaError as e:
            return (409,"Schema validation failed.Please check the data or re-define Schema",e)

    # @classmethod
    # def get_user_data(cls):
    #     pass