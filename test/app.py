from flask import Flask

ap = Flask(__name__)

@ap.route("/",methods=["GET"])
def fuN():
    return "hello"


if __name__ == "__main__":
    ap.run(debug=True)