from peewee import *


db = PostgresqlDatabase('country', user='guangjianbao', password='12345',
                        host='localhost', port=5432)

db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Country(BaseModel):
    name = CharField()
    capital = CharField()
    population = IntegerField()


db.create_tables([Country])


country1 = Country(name='United States of America',
                   capital='Washington, DC', population=329500000)
country1.save()
