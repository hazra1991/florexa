from passlib.hash import pbkdf2_sha256
from lib.token import generate_jwt
import pymongo

class NoUserFound(Exception):
    pass

class InvalidPass(Exception):
    pass

class User:
    client =  pymongo.MongoClient()
    @classmethod
    def verify_and_get_Token(cls,email_id,password):
        db = cls.client.florexa
        collection = db.user_info
        u_info =  collection.find_one({"email_id":email_id})
        if u_info is not None:
            u_info['_id'] = str(u_info["_id"])
            if pbkdf2_sha256.verify(password,u_info["password"]):
                u_info.pop('password')
                return (generate_jwt(u_info),u_info)
            else:
                raise InvalidPass ("password incorrect")
        else:
            raise NoUserFound

    @classmethod
    def register_user(cls,user_data):
        try:
            db = cls.client.florexa
            db.user_info.create_index([("email_id",pymongo.ASCENDING)],unique=True)
            user_data["password"] = pbkdf2_sha256.hash(user_data["password"])
            db.user_info.insert_one(user_data)
            return True
        except pymongo.errors.DuplicateKeyError:
            return False

    # @classmethod
    # def get_user_data(cls):
    #     pass