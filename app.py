from flask import Flask
import requests
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

@app.route('/')
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=b7d6a69e341e91ca31cefbd99139d193'

    city = 'Las Vegas'

    #fetching the dat from the apii if going here
    #first passing the city name to the api call 
    r = requests.get(url.format(city)).json()
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
        'city' : city,
        'temperature' : r['main']['temp'],
        'description' : r["weather"][0]['description'],
        'icon' : r['weather'][0]['icon'],
        'country' : r['sys']['country'],
        'humidity' :r['main']['humidity'],
        'pressure' :r['main']['pressure']
    }
    print(weather)




    return render_template('template.html',weather=weather)
if __name__=='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=5000) 

