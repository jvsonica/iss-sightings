from flask import Flask, request
from src.find import get_sightings, find_location_by_city_name, find_location_by_gps_coordinates
from src.error import InvalidUsage
import json
app = Flask(__name__)


@app.route('/find-by-city', methods=['GET'])
def find_by_city():
    location = find_location_by_city_name(request.args.get('city'))
    return json.dumps({
        'location': {
            'city': location.city,
            'country': location.country,
            'full_location': location.full_location
        },
        'sightings': get_sightings(location.country, location.region, location.city)
    }, cls=Flask.json_encoder)


@app.route('/find-by-gps', methods=['GET'])
def find_by_gps():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    location = find_location_by_gps_coordinates(latitude, longitude)
    return json.dumps({
        'location': {
            'city': location.city,
            'country': location.country,
            'full_location': location.full_location
        },
        'sightings': get_sightings(location.country, location.region, location.city)
    }, cls=Flask.json_encoder)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = error.to_dict()
    response['status_code'] = error.status_code
    return json.dumps(response)

app.run('0.0.0.0', 5000)
