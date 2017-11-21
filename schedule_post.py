# schedule_post.py
# Author: Daniel Edades
# Last Modified: 11/21/2017
# Description: Formats a database row intended to represent a post scheduled
# for a future time, then inserts that row into a database table for later
# retrieval and posting at that actual time.


import sqlite3


def schedule_post(table_name, time, content):

    conn = sqlite3.connect('scheduled_posts.db')
    c = conn.cursor()
    command_string = "INSERT INTO " + "\'" + table_name + "\'"
    command_string += "(\'post_time\', \'contents\', \'posted\')"
    command_string += " VALUES (?, ?, 0)"
    c.execute(command_string, (time, content))

    conn.commit()