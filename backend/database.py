from peewee import *

db = SqliteDatabase('hostel.db')

class BaseModel(Model):
    class Meta:
        database = db

class Guest(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    phone = CharField()
    country = CharField()
    document_id = CharField(unique=True)
    total_stays = IntegerField(default=0)
    last_visit = DateField(null=True)

class Room(BaseModel):
    number = CharField(unique=True)
    type = CharField()
    capacity = IntegerField()
    price = FloatField()
    status = CharField(default='available')

class Booking(BaseModel):
    guest = ForeignKeyField(Guest, backref='bookings')
    room = ForeignKeyField(Room, backref='bookings')
    check_in = DateField()
    check_out = DateField()
    status = CharField(default='active')

def initialize_db():
    db.connect()
    db.create_tables([Guest, Room, Booking])
    db.close()