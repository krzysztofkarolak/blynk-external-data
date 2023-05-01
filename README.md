# Blynk Api External Weather Data

A Python app for weather data deployment to [Blynk](https://blynk.cc) Projects, using:

- [Airly](https://airly.eu) for temperature and air pollution data,
- [Yahoo Weather](https://weather.yahoo.com) for temperature, wind speed/direction, weather conditions data,
- [Open Weather Map](https://openweathermap.org) for temperature, humidity, pressure, wind speed/direction, weather conditions data,
- [Blynk Server](https://github.com/blynkkk/blynk-server) Api for data deployment to Blynk projects.

This application works with default or custom instance of Blynk server.

If your Blynk Project provides a temperature sensor with a fan mounted outside, the app can send the information to the sensor if weather conditions are favourable to start the fan.

## Configuration

Python 3.11 or newer is recommended. Make sure you have installed Python depedencies:

```sh
PyYAML>=4.2b1
certifi>=2018.4.16
chardet>=3.0.4
idna>=2.6
pytz>=2018.4
requests>=2.20.0
urllib3>=1.24.2
```

Create config.yml file and enter your API keys:

```sh
server:
    name: "My Data Server"
    timezone: "Europe/Berlin"
    lang: "pl" # en or pl are supported for weather data
    units: "metric" # metric or imperial
location:
    latitude: "52.526400"
    longitude: "13.397261"
    owmCityId: "2950159" # OpenWeatherMap City Id
    yahooCityWOEID: "638242"
apiKeys:
    airlyKey: "yourapikey" # You can request your API Key on airly.eu
    owmKey: "yourapikey" # You can request your API Key on openweathermap.org
    blynkKey: "yourapikey" # Blynk Project Api Key
blynkServer:
    hostname: "blynk-cloud.com" # Your Blynk Server URL
    port: "9443" # Default HTTPS Api port
devices:
    fan: true # If there is a fan in your temperature sensor, leave this option true
```

## Deploying to Heroku

This app was intended to work in Heroku or GCP CloudFunction. You can easily deploy it to Heroku instance:

```sh
$ heroku create
$ git add .
$ git commit -am "First commit"
$ git push heroku master

```
or in GCP Cloud Functions:

```sh
$ gcloud functions deploy function-name --runtime python311 --entry-point=BlynkExternalData

```

## Blynk Project Configuration

Default Virtual Pins are listed below:

- V36: Air Quality Color
- V37: Air Quality Description
- V38: Humidity
- V39: PM 1
- V40: PM 2.5
- V41: PM 10
- V42: Air Pollution Level
- V43: Temperature
- V44: Air Quality Index - CAQI
- V45: Temperature Sensor's Fan favourable conditions (based on weather conditions) [0 or 1]
- V46: Date and time of data update
- V47: Wind Speed
- V48: Wind Direction
- V49: Pressure
- V70: OWM Weather Conditions
- V71: Server Name
- V72: Yahoo Weather Conditions
