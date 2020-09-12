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
        abort(401)
        

@user.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        print("entered")
        user_data =  request.get_json()
        if user_data is not None:
            dbresp = User.register_user(user_data)
            if dbresp is True:
                return make_response({"code":200,"status":"success","redirect_url":url_for('user.login')})
            else:
                return make_response({"code":dbresp[0],"status":"Failed","error":dbresp[1],
                                    "redirect_url":url_for('user.login')},dbresp[0])
        else:
            abort(422)

    elif request.method == "GET": 
        response =  make_response({
            "email_id":"<string>",
            "first_name":"<string>",
            "last_name":"<string>",
            "password":"<string",
            "phone":"<int>",
            "location":"<string>",
            "verifyed":"bool",
            "verified_on":"<string/null>",
            "DOB":"<string>"
            })
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

# @user.route("/verify/<str:token>")
# def userverification():
#     pass
