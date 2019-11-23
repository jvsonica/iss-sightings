import datetime
import re
import math
import pandas as pd
import requests
import hashlib
from bs4 import BeautifulSoup
from .error import InvalidUsage

from src.possible_addresses import locations

df_locations = pd.DataFrame(locations, columns=['full_location', 'latitude', 'longitude', 'region', 'country', 'city'])


def get_sightings(country, region, city):
    # Fetch rss feed of the location given
    rss = 'https://spotthestation.nasa.gov/sightings/xml_files/{}_{}_{}.xml'.format(
        country, region, city
    )
    r = requests.get(rss)

    # Create hashing interface to be used to calculate an identifier of all sightings
    m = hashlib.md5()

    # Parse the information from the received feed
    xml = BeautifulSoup(r.text, features='html.parser')
    items = xml.find_all('item')
    sightings = []
    for item in items:
        # Discarding any sighting events that aren't of ISS
        title = item.find('title').contents[0][11:]
        if title != 'ISS Sighting':
            continue

        # Parse information of the sighting
        info = item.find('description').contents[0]
        date = re.search(r'Date:\s(.*)<br/>', info).groups()[0]
        time = re.search(r'Time:\s(.*?)\s<br/>', info).groups()[0]
        duration = re.search(r'Duration:\s(.*)\s<br/>', info).groups()[0]
        maximum_elevation = re.search(r'Maximum Elevation:\s(.*)\s<br/>', info).groups()[0]
        approach = re.search(r'Approach:\s(.*)\s<br/>', info).groups()[0]
        departure = re.search(r'Departure:\s(.*)\s<br/>', info).groups()[0]

        m.update(country.encode())
        m.update(city.encode())
        m.update(date.encode())
        hash_content = m.hexdigest()[:16]

        sightings.append({
            'sighting': item.find('title').contents[0][11:],
            'timestamp': datetime.datetime.strptime(date + time, '%A %b %d, %Y %I:%M %p'),
            'duration': duration,
            'maximum_elevation': maximum_elevation,
            'approach': approach,
            'departure': departure,
            'identifier': hash_content
        })

    # Remove sightings that have already occurred
    sightings = [s for s in sightings if s['timestamp'] > datetime.datetime.now()]
    sightings = sorted(sightings, key=lambda s: s['timestamp'])[:5]
    return sightings


def find_location_by_city_name(city=None):
    matching_locations = df_locations[df_locations['full_location'].str.lower().str.contains(city.lower())]

    if matching_locations.empty:
        raise InvalidUsage('City not found.')

    return matching_locations.iloc[0]


def find_location_by_gps_coordinates(latitude, longitude):
    if latitude is None or longitude is None:
        raise BaseException('No location source given as parameter')

    # Filter the locations that are at least 1 lat/lon decimal degree away so we only
    # calculate the haversine distance of the relevant locations
    matching_locations = df_locations.drop(df_locations[~(
        (df_locations.latitude < latitude + 1) &
        (df_locations.latitude > latitude - 1) &
        (df_locations.longitude < longitude + 1) &
        (df_locations.longitude > longitude - 1)
    )].index)

    def haversine_distance(row, lat, lon):
        earth_radius = 6371e3
        [lat1, lon1] = [math.radians(x) for x in (lat, lon)]
        [lat2, lon2] = [math.radians(x) for x in (row['latitude'], row['longitude'])]
        [dlat, dlon] = [lat2 - lat1, lon2 - lon1]

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return earth_radius * c

    matching_locations['distance'] = matching_locations.apply(haversine_distance, args=(latitude, longitude), axis=1)
    return matching_locations.sort_values(by='distance').iloc[0]
