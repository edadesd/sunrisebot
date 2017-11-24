# sunrisebot
A Twitter bot written in Python 3 that posts places where the sun is rising or setting. Uses sqlite3 databases to store the following:

* Location names
* Latitudes and longitudes
* UTC offsets
* Sunrise and sunset times queried from https://sunrise-sunset.org/api based on latitudes and longitudes.

Schedules posts by executing sunrise.py once per day at 12:00AM UTC, which collects sunrise and sunset data from a sample of locations in each time zone. Formats them as database rows timestamped with the queried sunrise or sunset time. post_sunrises.py polls the database one per minute to find rows with a past timestamp, then extracts their text and posts them to Twitter. It then archives the post in a separate table and deletes it from the table of scheduled posts.

Still need to add:

* Sqlite3 Python script to create tables  
* Crontab to run daily sample/API queries and schedule sunrise/sunset posts  
* Crontab to check for timely posts every minute  
