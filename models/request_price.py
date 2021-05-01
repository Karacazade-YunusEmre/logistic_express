from pony.orm import *

db = Database()
db.bind(provider="sqlite", filename="../db.sqlite", create_db=True)


class RequestPrice(db.Entity):
    _table_ = "RequestPrice"
    id = PrimaryKey(int, auto=True, column="ID")
    name = Optional(str, column="Name")
    email = Optional(str, column="Email")
    phone = Optional(str, column="PhoneNumber")
    freight_type = Optional(str, column="FreightType")
    departure_city = Optional(str, column="DepartureCity")
    incoterms = Optional(str, column="Incoterms")
    weight = Optional(str, column="Weight")
    height = Optional(str, column="Height")
    width = Optional(str, column="Width")
    length = Optional(str, column="Length")
    radio_extra = Required(str, column="RadioExtra")


db.generate_mapping(create_tables=True)
