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
    "location":{
        "city":"Braga",
        "full_location":"Braga, Portugal",
        "country":"Portugal"
    },
    "sightings":[
        {
            "identifier":"d98c2449644fd612",
            "approach":"13° above WNW",
            "departure":"13° above WNW",
            "timestamp":"Sat, 23 Nov 2019 19:49:00 GMT",
            "duration":"less than  1 minute",
            "sighting":"ISS Sighting",
            "maximum_elevation":"13°"
        },
        {
            "identifier":"ee38d3548f2cc1bd",
            "approach":"23° above W",
            "departure":"37° above NW",
            "timestamp":"Sun, 24 Nov 2019 19:01:00 GMT",
            "duration":"1 minute",
            "sighting":"ISS Sighting",
            "maximum_elevation":"37°"
        },
        {
            "identifier":"51c4707a566cf03c",
            "approach":"33° above W",
            "departure":"20° above NE",
            "timestamp":"Mon, 25 Nov 2019 18:13:00 GMT",
            "duration":"3 minutes",
            "sighting":"ISS Sighting",
            "maximum_elevation":"59°"
        },
        {
            "identifier":"ad703005aad5e75c",
            "approach":"10° above WNW",
            "departure":"10° above WNW",
            "timestamp":"Mon, 25 Nov 2019 19:49:00 GMT",
            "duration":"less than  1 minute",
            "sighting":"ISS Sighting",
            "maximum_elevation":"10°"
        },
        {
            "identifier":"59b1c093080a7309",
            "approach":"12° above WNW",
            "departure":"21° above NNW",
            "timestamp":"Tue, 26 Nov 2019 19:01:00 GMT",
            "duration":"2 minutes",
            "sighting":"ISS Sighting",
            "maximum_elevation":"21°"
        }
    ]
}
```
