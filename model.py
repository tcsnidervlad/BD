from peewee import *
from flask import *

app = Flask(__name__)
app.config.from_object(__name__)

db = PostgresqlDatabase(
    "Parcer",
    user="postgres",
    password="123",
    host="localhost",
    port="5432",
)

db.connect()


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = db


class BaseModel(Model):
    class Meta:
        database = db


class Client(BaseModel):
    client_id = AutoField()
    login = CharField()
    password = CharField()

    class Meta:
        table_name = 'client'


class SuperUser(BaseModel):
    user_id = AutoField()
    username = CharField()
    password = CharField()
    is_superuser = BooleanField(default=True)

    class Meta:
        table_name = 'superuser'


class Requests(BaseModel):
    requests_id = AutoField()
    username_id = CharField()
    name_request = CharField()

    class Requests:
        table_name = 'requests'
