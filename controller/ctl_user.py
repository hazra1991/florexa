from passlib.hash import pbkdf2_sha256
from lib.tokenlib import generate_jwt , generate_url_token
from lib.mongomodel import Errors
from model.user_model import UserSchema
from lib.mailserver import send_mail

class NoUserFound(Exception):
    pass

class InvalidPass(Exception):
    pass

class User:
    # client =  pymongo.MongoClient()
    @classmethod
    def verify_and_get_Token(cls,email_id,password):
        UserSchema.connect()
        document = UserSchema()
        u_info =  document.findone({"email_id":email_id})
        print(type(document),document)
        # print(userdocObj.email_id)
        # print(userdocObj)
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
            document = UserSchema(user_data)
            print(document)
            # temp = userdocObj.florexa.user_info.insert()
            document.insert()
            print(" MA HERERERE")
            return True
        except Errors.DuplicateKeyErr as e:
            return (409,"Email id already registered",e)
        except Errors.SchemaError as e:
            return (409,"Schema validation failed.Please check the data or re-define Schema",e)
        
    @classmethod
    def send_verification_mail(cls,baseurl,mail_id):
        # TODO meed to implement threading
        urltoken = generate_url_token(mail_id)
        subject="Florexa mail Verification"
        verification_url_msg = "Click the link below to verify\n\n{}?token={}".format(baseurl,str(urltoken))

        print(verification_url_msg)
        send_mail(subject=subject,body=verification_url_msg,sendto="florexa.dev@gmail.com")




    # @classmethod
    # def get_user_data(cls):
    #     pass