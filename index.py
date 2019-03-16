import argparse
from src.print import print_sightings
from src.find import get_sightings, find_location_by_city_name, find_location_by_gps_coordinates

parser = argparse.ArgumentParser(description='Get next International Space Station sightings in your city.')
parser.add_argument('--city', '-c', metavar='Braga', type=str, help='city')
parser.add_argument('--coordinates', '-g', metavar='42.5,-8.4', type=str, help='comma-separated gps coordinates. \'latitude,longitude\'')
args = parser.parse_args()
location = None

print('Gathering information...\n')

if args.city is not None:
    location = find_location_by_city_name(args.city)

if args.coordinates is not None:
    [latitude, longitude] = [float(c) for c in args.coordinates.split(',')]
    location = find_location_by_gps_coordinates(latitude, longitude)
    print('The closest location to {latitude},{longitude} found was {city}'
          .format(latitude=latitude, longitude=longitude, city=location['full_location']))

sighting_list = get_sightings(location.country, location.region, location.city)
print_sightings(location.city, sighting_list)
