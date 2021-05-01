import sqlite3

from flask import session
from pony.orm import db_session, select

from models.create_freight import CreateFreight
from models.message import Message
from models.request_price import RequestPrice
from models.user import User


@db_session
def add_user(user):
    User(name=user["name"], last_name=user["last_name"], username=user["username"], email=user["email"],
         phone_number=user["phone_number"],
         password=user["password"])


@db_session
def get_user(username):
    return User.get(username=username)


@db_session
def add_message(message):
    Message(
        name_lastname=message["name_lastname"],
        email=message["email"],
        subject=message["subject"],
        message=message["message"]
    )


@db_session
def add_request_price(request):
    RequestPrice(
        name=request["name"],
        email=request["email"],
        phone=request["phone"],
        freight_type=request["freight_type"],
        departure_city=request["departure_city"],
        incoterms=request["incoterms"],
        weight=request["weight"],
        height=request["height"],
        width=request["width"],
        length=request["length"],
        radio_extra=request["radio_extra"]
    )


@db_session
def create_freight(freight):
    CreateFreight(
        user_id=freight["user_id"],
        freight_type=freight["freight_type"],
        departure_city=freight["departure_city"],
        incoterms=freight["incoterms"],
        weight=freight["weight"],
        height=freight["height"],
        width=freight["width"],
        length=freight["length"],
        radio_extra=freight["radio_extra"],
        freight_number=freight["freight_number"]
    )


@db_session
def get_freight(freight_number):
    user_id = get_user(session["username"])
    result = CreateFreight.select(lambda c: c.freight_number == freight_number and c.user_id == user_id.id).first()
    return result


@db_session
def get_my_freights():
    user = get_user(session["username"])
    result = list(CreateFreight.select(lambda f: f.user_id == user.id))
    return result


# Getting Admin Information
def get_admin(username, password):
    db = sqlite3.connect("db.sqlite")
    cursor = db.cursor()
    cursor.execute("select * from SuperUser")
    db.commit()

    result = cursor.fetchone()
    db.close()

    return True if username in result and password in result else False


@db_session
def get_all_users():
    return list(select(u for u in User))


@db_session
def get_all_freights():
    return list(select(f for f in CreateFreight))


@db_session
def get_request_freight():
    return list(select(r for r in RequestPrice))


@db_session
def get_all_messages():
    return list(select(m for m in Message))
