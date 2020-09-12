from flask import Flask ,url_for
from views.user import user

################
#### config ####
################

app = Flask(__name__)
# app.config 

####################
#### blueprints ####
####################

app.register_blueprint(user,url_prefix="/user")

########################
#### error handlers ####
########################

@app.errorhandler(404)
def not_found(error):
    return ({"code":404,"error":"url not found","message":str(error)},404)

@app.errorhandler(403)
def forbidden_page(error):
    return ({"code":403,"error":"permission denied.Resource forbidden or token expired ","message":str(error)},403)

@app.errorhandler(500)
def server_error(error):
    return ({"code":500,"error":"server crashed","message":str(error)},500)

@app.errorhandler(400)
def token_expired(error):
    return ({"code":400,"error":"Bad Request/ Data format incorrect / Invalid Token ","redirect_url":url_for("user.login")},400)

@app.errorhandler(422)
def Invalid_data(error):
    return ({"code":422,"error":"Invalid or Unprocessable data"},422)

@app.errorhandler(401)
def unauthorized(error):
    return ({"code":401,"status":"failed","error":"Authorization failed,password incorrect","message":str(error)},401)

if __name__ == "__main__":
    #TODO sett the env variables including the secrect_key,and other config params 
    app.run(debug=True)

