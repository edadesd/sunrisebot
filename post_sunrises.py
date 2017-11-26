# post_sunrises.py
# Author: Daniel Edades
# Last Modified: 11/21/2017
# Description: Scans the database for rows with a timestamp earlier than the
# current time. Extracts the data from those rows and posts it to Twitter via
# the account designated through the authentication tokens. Archives the row
# in a different table after posting and cleans all posted rows out of the
# scheduled posts table. Intended usage: call once per minute via cronjob.

import tweepy
import sqlite3
import secret

# Twitter authentication
auth = tweepy.OAuthHandler(secret.CONSUMER_TOKEN, secret.CONSUMER_SECRET)
auth.set_access_token(secret.ACCESS_TOKEN, secret.ACCESS_SECRET)

api = tweepy.API(auth)

conn = sqlite3.connect('scheduled_posts.db')
c = conn.cursor()

command_string = "SELECT * FROM scheduled_posts WHERE posted = 0 AND post_time "
command_string += "<= datetime(\'now\')"
c.execute(command_string)
#c.execute("SELECT * FROM scheduled_posts")
scheduled_posts = []
# Post scheduled text to Twitter and prepare post for archiving in database.
for post in c.fetchall():

    # Extract text from database row. Current schema places text in the
    # second column.
    post_content = post[1]
    # api.update_status(post_content)

    # Copy contents of post for archiving in database.
    new_post = []
    for item in post:
        new_post.append(item)
    posted_id = (new_post[3],)
    # Update posted flag and copy to the database of past posts.
    c.execute("UPDATE scheduled_posts set posted = 1 WHERE id = ?", posted_id)
    post_args = (new_post[0], new_post[1], posted_id[0])
    c.execute("INSERT into posted VALUES(?, ?, ?)", post_args)

# Clean posts out of the scheduled_post database.
c.execute("DELETE FROM scheduled_posts WHERE posted = 1")
conn.commit()


