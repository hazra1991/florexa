from flask import Blueprint , request ,make_response ,url_for,abort
from controller.ctl_user import User , NoUserFound , InvalidPass
from lib.token import verify_jwt

user = Blueprint('user',__name__)

# @user.before_app_request
# def run():
#     print("yes it ran")

@user.route("/login",methods=["GET"])
def login():
    try:
        data = request.get_json()
        TOKEN ,u_info = User.verify_and_get_Token(data.get("email_id"),data.get("password"))
        response = make_response({"code":200,"user_info":u_info,"status":"success","redirect_url":url_for('user.homepage'),
                                 "x-access-token":TOKEN.decode('utf-8')})
        return response

    except NoUserFound:
        return make_response({"code":404,"status":"failed","error":"user not found",
                "redirect_url":url_for('user.signup')},404)
    except InvalidPass:
        return make_response({"code":401,"status":"failed","error":"authorization failed"},401)
        

@user.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        print("entered")
        user_data =  request.get_json()
        if user_data is not None:
            if User.register_user(user_data):
                return make_response({"code":200,"status":"success","redirect_url":url_for('user.login')})
            else:
                return make_response({"code":409,"status":"Failed","error":"user exists",
                                    "redirect_url":url_for('user.login')},409)

    elif request.method == "GET":
        #TODO the defined module scema can be put in future  
        response =  make_response({
            "Http_method":"POST",
            "email_id":"example@example.com",
            "first_name":"<string>",
            "last_name":"<string>",
            "password":"<string",
            "phone":"<int>",
            "location":"<string>",
            "verifyed":False,
            "verified_on":"<date/Null>",
            "DOB":{
                "year":"<int>",
                "month":"<int>",
                "date": "<int>"
            }})
        response.headers["Content-Type"] = "application/json"
        return response




@user.route("/homepage")
@verify_jwt
def homepage(user_info):
    return  user_info
    


@user.route("/logout")
def logout():
    pass

@user.route("/forgotpassword/")
def forgotpass():
    pass

# # @user.route("/verify/<token>")
