# iss-sightings

Finds the next ISS Sighting near your area and helps you localize it.

This projects simply reads and gathers data from the ISS sightings RSS feeds supplied by
[NASA's Spot the Station](https://spotthestation.nasa.gov/sightings/).

Although the results can be obtained through quick command examples below, a simple Flask
example webservice can also be run with the same available requests.

When a search by city is issued, the available locations on NASA's RSS feed are checked. If the city is not found, an
error message is presented. If a search by gps coordinates is issued, the haversine distance to the most likely cities
is calculated. The results are taken from the smallest distance. In both situations, the inferred city is returned in
the response message.

### CLI

Search by city name with:
```
python cli.py -c Braga
```

Or with gps coordinates:
```
python cli.py -g 41.55,-8.45
```

### Server
Alternatively, run as a flask server with
```
python server.py
```

The server's default port is `5000`. Then, the following routes will be available:

- To find the next 5 sightings in a city:
```
GET /find-by-city?city=<City Name>`
```

- To find the next 5 sightings by GPS coordinates
```
GET /find-by-gps?latitude=<latitude>&longitude=<longitude>`
```

Example output for both requests:
```json
{
    "location": {
        "city": "Oporto-Porto",
        "country": "Portugal",
        "full_location": "Oporto-Porto, Portugal"
    },
    "sightings": [{
        "sighting: "ISS Sighting",
        "departure": "11° above SE",
        "approach": "20° above SE",
        "maximum_elevation": "20°",
        "duration": "1 minute",
        "timestamp": "Sun, 17 Mar 2019 04:35:00 GMT"
    }, {
        "sighting": "ISS Sighting",
        "departure": "10° above SW",
        "approach": "10° above WSW",
        "maximum_elevation": "10°",
        "duration": "1 minute",
        "timestamp": "Sun, 17 Mar 2019 06:09:00 GMT"
    }, {
        "sighting": "ISS Sighting",
        "departure": "10° above S",
        "approach": "14° above S",
        "maximum_elevation": "14°",
        "duration": "less than 1 minute",
        "timestamp": "Mon, 18 Mar 2019 05:20:00 GMT"
    }, {
        "sighting": "ISS Sighting",
        "departure": "29° above S",
        "approach": "10° above SSW",
        "maximum_elevation": "29°",
        "duration": "2 minutes",
        "timestamp": "Wed, 20 Mar 2019 20:14:00 GMT"
    }, {
        "sighting": "ISS Sighting",
        "departure": "13° above E",
        "approach": "10° above S",
        "maximum_elevation": "19°",
        "duration": "4 minutes",
        "timestamp": "Thu, 21 Mar 2019 19:24:00 GMT"
    }]
}
```
