from flask import Flask
import requests
from flask import render_template,redirect,url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 #database 
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&appid=b7d6a69e341e91ca31cefbd99139d193'
    r = requests.get(url).json()
    return r 
         



@app.route('/',methods=['GET'])
def index_get():
    cities = City.query.all()
    cities = reversed(cities)

    
    #creating a blank list to hold all the cities
    weather_data = []

    for city in cities:
        r = get_weather_data(city.name)
        print(r)


        #fetching the dat from the apii if going here
        #first passing the city name to the api call 
       
        #now we are getting the data in the nested dict and lsit
        # output data 
        # {'coord': {'lon': -115.14, 'lat': 36.17}, 
        # 'weather': [{'id': 800, 'main': 'Clear',
        # 'description': 'clear sky', 'icon': '01n'}], 
        # 'base': 'stations', 
        # 'main': {'temp': 46.69, 'feels_like': 38.82, 'temp_min': 44.01, 
        # 'temp_max': 48.99, 'pressure': 1018, 'humidity': 70}, 
        # 'visibility': 16093, 'wind': {'speed': 9.17, 'deg': 90}, 
        # 'clouds': {'all': 1}, 'dt': 1586436500, 
        # 'sys': {'type': 1, 'id': 6171, 
        # 'country': 'US', 'sunrise': 1586438062, 'sunset': 1586484546}, 
        # 'timezone': -25200, 'id': 5506956, 'name': 'Las Vegas', 'cod': 200}

        #there are lot of info is coming so we only stor the usefull one 
        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r["weather"][0]['description'],
            'icon' : r['weather'][0]['icon'],
            'country' : r['sys']['country'],
            'humidity' :r['main']['humidity'],
            'pressure' :r['main']['pressure']
        }
        print(weather)
        weather_data.append(weather)



    return render_template('template.html', weather_data=weather_data)

@app.route('/',methods=['POST'])
def index_post():
    err_msg = ''
    # db.session.query(City).delete()
    # db.session.commit()
    # if request.method == 'POST':
    new_city = request.form.get('city')
    if new_city :
        existing_city = City.query.filter_by(name=new_city).first()
           
        if not existing_city:
            new_city_data = get_weather_data(new_city)
            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city)
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = 'City does not Exit in the world!'
        else:
            err_msg = 'City not exist in database!'

    return redirect(url_for('index_get'))

if __name__=='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=3000) 

