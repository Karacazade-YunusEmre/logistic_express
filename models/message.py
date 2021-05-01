from pony.orm import *

db = Database()
db.bind(provider="sqlite", filename="../db.sqlite", create_db=True)


class Message(db.Entity):
    _table_ = "Message"
    id = PrimaryKey(int, auto=True, column="ID")
    name_lastname = Required(str, column="Name")
    email = Required(str, column="Email")
    subject = Required(str, column="Subject")
    message = Required(str, column="Message")


db.generate_mapping(create_tables=True)
