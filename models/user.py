from pony.orm import *

db = Database()
db.bind(provider="sqlite", filename="../db.sqlite", create_db=True)


class User(db.Entity):
    _table_ = "User"
    id = PrimaryKey(int, auto=True, column="ID")
    name = Required(str, column="Name")
    last_name = Required(str, column="LastName")
    username = Required(str, column="UserName")
    email = Required(str, column="Email")
    phone_number = Required(str, column="PhoneNumber")
    password = Required(str, column="Password")


db.generate_mapping(create_tables=True)
