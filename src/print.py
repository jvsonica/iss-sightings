def print_sightings(city, sightings):
    if len(sightings) == 0:
        print('No sightings registered for the near future for {}. Check back soon!'.format(city))
        return

    print('''
    ==========================================================================
        Next sighting in {city} will occur on {date} at {time}.
        This sighting will have a {duration} duration.
        The ISS will be visible at around {approach} and will disappear
        on {departure}, {duration} later.
        It should reach a maximum altitude of {maximum_elevation}.
    ==========================================================================
    '''
          .format(city=city,
                  date=sightings[0]["timestamp"].strftime('%A, %d %B'),
                  time=sightings[0]["timestamp"].strftime('%H:%M'),
                  duration=sightings[0]["duration"],
                  maximum_elevation=sightings[0]["maximum_elevation"],
                  approach=sightings[0]["approach"],
                  departure=sightings[0]["departure"]))

    print('If you can\'t catch the ISS at that time, check below future sightings in {}:'.format(city))

    for i in range(1, 4):
        print('- {date} at {time} with a {duration} duration. Appearing at {approach} and disappearing at {departure}'
              .format(city=city,
                      date=sightings[i]["timestamp"].strftime('%A, %d %B'),
                      time=sightings[i]["timestamp"].strftime('%H:%M'),
                      duration=sightings[i]["duration"],
                      approach=sightings[i]["approach"],
                      departure=sightings[i]["departure"]))

    print('\nFor more information on how to interpret these values, check this video! https://youtu.be/nqn8zT1VipA')
