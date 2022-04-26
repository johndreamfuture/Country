from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model


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


db.drop_tables([Country])
db.create_tables([Country])

country1 = Country(name='United States of America',
                   capital='Washington, DC', population=329500000)
country1.save()
country2 = Country(name='Afghanistan',
                   capital='Kabul', population=38930000)
country2.save()
country3 = Country(name='Barbados',
                   capital='Bridgetown', population=287371)
country3.save()
country4 = Country(name='Bhutan',
                   capital='Thimphu', population=771612)
country4.save()
country5 = Country(name='Canada',
                   capital='Ottawa', population=37742154)
country5.save()
country6 = Country(name='Cuba',
                   capital='Havana', population=11326616)
country6.save()
country7 = Country(name='Egypt',
                   capital='Cairo', population=102334404)
country7.save()

app = Flask(__name__)


@app.route('/')
def index():
    return f"Hello, welcome to the country api!there are {Country.select().count()} countries"


@app.route('/country/', methods=['GET', 'POST'])
@app.route('/country/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Country.get(Country.id == id)))
        else:
            countryList = []
            for country in Country.select():
                countryList.append(model_to_dict(country))
            return jsonify(countryList)

    if request.method == 'PUT':
        Country.update(request.get_json()).where(Country.id == id)
        Country.execute()
        return jsonify({'updated': True})

    if request.method == 'POST':
        addcountry = dict_to_model(Country, request.get_json())
        addcountry.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        deleted = Country.delete().where(Country.id == id)
        deleted.execute()
        return jsonify({'deleted': True})


app.run(port=5000, debug=True)
