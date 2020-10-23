from flask import Blueprint,request
from controller.ctl_booking import Book

booking = Blueprint("booking",__name__)

@booking.route("/schedule",methods=["POST"])
def schedule():
    book_details = request.get_json()
    if book_details is not None:
        try:
            print(book_details)
            doc = Book(book_details)
            doc.schedule()
        except:
            pass
    print(book_details)
    return book_details
