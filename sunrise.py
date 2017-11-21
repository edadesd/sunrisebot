# sunrise.py
# Author: Daniel Edades
# Last Modified: 11/21/2017
# Description: Chooses a sample of locations from different timezones, taken
# out of a database of names with latitudes and longitudes. Queries a sunrise
# and sunset time API and extracts times for the chosen cities. Then formats
# the data as the text of a post for Twitter. Stores the text in a database
# of scheduled posts.

import sqlite3
import schedule_post    # Stores a timestamp + string in a database table
import requests
import random
import datetime

CITIES_PER_ZONE = 3
API_ENDPOINT = "https://api.sunrise-sunset.org/json?"
SUNRISE_TEXT = "The sun is rising over "
SUNSET_TEXT = "The sun is setting over "
random.seed()

conn = sqlite3.connect("timezones.db")
c = conn.cursor()

c.execute("select * from timezones")
zones = []
for row in c.fetchall():
    zones.append(row)

# Create the table of cities by time zone. This will be a list of tuples
# where the first entry is the UTC offset and the second entry is the
# list of city entries from the database.
cities = []
for row in zones:
    cities_in_zone = []
    c.execute("select * from cities where offset=?", (row[0],))
    for city in c.fetchall():
        cities_in_zone.append(city)
    cities.append((row[0], cities_in_zone))

sunrise_cities = []
sunset_cities = []

# Take a sample of locations from each timezone. Sample size depends on
# the number of locations.
for row in cities:
    if len(row[1]) == 1:
        sunrise_sample = row[1]
        sunset_sample = row[1]
    elif len(row[1]) == 2 or row[1] == 3:
        sunrise_sample = random.sample(row[1], 2)
        sunset_sample = random.sample(row[1], 2)
    else:
        sunrise_sample = random.sample(row[1], CITIES_PER_ZONE)
        sunset_sample = random.sample(row[1], CITIES_PER_ZONE)
    for city in sunrise_sample:
        sunrise_cities.append(city)
    for city in sunset_sample:
        sunset_cities.append(city)

for city in sunrise_cities:
    # Query API for data from each location chosen.
    # API requires two arguments: lat= and long=
    request_string = API_ENDPOINT + "lat=" + str(city[1])
    request_string += "&lng=" + str(city[2])
    r = requests.get(request_string)
    retrieved = r.json()
    sunrise = retrieved['results']['sunrise']

    # Build the text of the Twitter post.
    # e.g. "The sun is rising over Mexicali."
    post_text = SUNRISE_TEXT + city[0] + "."

    # Convert sunrise time into SQLite datetime string format.
    # Run this at 12:00 AM UTC to ensure date is correct for all posts
    # added at time of execution.
    utc_day = datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y-%m-%d ")
    converted_time = datetime.datetime.strptime(sunrise, "%I:%M:%S %p")
    converted_time = datetime.datetime.strftime(converted_time, "%H:%M")
    date_and_time = utc_day + converted_time

    # Schedule the sunrise for later posting by inserting it into the
    # table of scheduled posts as a database row
    schedule_post.schedule_post("scheduled_posts", date_and_time, post_text)

# Same procedure as above for sunrise_cities
for city in sunset_cities:
    request_string = API_ENDPOINT + "lat=" + str(city[1])
    request_string += "&lng=" + str(city[2])
    r = requests.get(request_string)
    retrieved = r.json()
    sunset = retrieved['results']['sunset']

    post_text = SUNSET_TEXT + city[0] + "."

    # Convert sunset time into SQLite datetime string format.
    utc_day = datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y-%m-%d ")
    converted_time = datetime.datetime.strptime(sunset, "%I:%M:%S %p")
    converted_time = datetime.datetime.strftime(converted_time, "%H:%M")
    date_and_time = utc_day + converted_time

    # Schedule the sunset for later posting by inserting it into the table of
    # scheduled posts as a database row.
    schedule_post.schedule_post("scheduled_posts", date_and_time, post_text)