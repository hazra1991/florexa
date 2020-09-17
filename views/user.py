from flask import Blueprint , request ,make_response ,url_for,abort
from controller.ctl_user import User , NoUserFound , InvalidPass
from lib.tokenlib import login_required,verify_and_geturldata_else_False

# TODO need to implement @app_loginrequired and secure the routes from front end access .CLIENTID and CLIENT_SECTERE

user = Blueprint('user',__name__)

# @user.before_app_request
# def run():
#     print("yes it ran")

@user.route("/login",methods=["POST"])
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
        

@user.route("/signup",methods=["POST"])
def signup():
    # TODO need to add a frontend access token to access this resource
    if request.method == "POST":
        print("entered")
        user_data =  request.get_json()
        if user_data is not None:
            dbresp = User.register_user(user_data)
            if dbresp is True:
                mail_id = user_data.get("email_id")
                b_url = url_for("user.userverification",mailid=mail_id,_external=True)
                User.send_verification_mail(b_url,mail_id)
                return make_response({"code":200,"status":"success","redirect_url":url_for('user.login')})
            else:
                return make_response({"code":dbresp[0],"status":"Failed","error":dbresp[1],"message":str(dbresp[2]),
                                    "redirect_url":url_for('user.login')},dbresp[0])
        else:
            abort(400)  


@user.route("/homepage")
@login_required
def homepage(user_info):
    return  user_info
    


@user.route("/logout")
def logout():
    pass

@user.route("/forgotpassword/")
def forgotpass():
    return "passs"
    pass
@user.route("/resendverification")
def resendverification():
    pass
@user.route("/verify/<mailid>")
def userverification(mailid):
    print(mailid)
    print(request.args.get("token"))
    if verify_and_geturldata_else_False(request.args["token"],exp_timedelta=30):
        return f"{mailid} verified"
    else:
        return "token expired"