from pony.orm import *

db = Database()
db.bind(provider="sqlite", filename="../db.sqlite", create_db=True)


class CreateFreight(db.Entity):
    _table_ = "CreateFreight"
    id = PrimaryKey(int, auto=True, column="ID")
    user_id = Required(int, column="UserID")
    freight_type = Optional(str, column="FreightType")
    departure_city = Optional(str, column="DepartureCity")
    incoterms = Optional(str, column="Incoterms")
    weight = Optional(str, column="Weight")
    height = Optional(str, column="Height")
    width = Optional(str, column="Width")
    length = Optional(str, column="Length")
    radio_extra = Required(str, column="RadioExtra")
    freight_number = Required(str, column="FreightNumber")


db.generate_mapping(create_tables=True)
