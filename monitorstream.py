# monitor Muddys music stream
import time
import requests
from requests.exceptions import RequestException
from datetime import datetime
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import mysql.connector
from mysql.connector import Error

def write_song_to_db(timestring, song_title):
    add_song = ("INSERT INTO song (time, title) values (%s, %s) ")
    cnx = mysql.connector.connect(user='stream', password='pickles', database='songs')
    cursor = cnx.cursor()

    data_song = (timestring, song_title)
    cursor.execute(add_song, data_song)
    
    # Make sure data is committed to the database
    cnx.commit()
    
    cursor.close()
    cnx.close()


def print_song_title():
    # api endpoint 20398
    URL = "http://muddys.digistream.info:20398/7.html"

    try:
        r = requests.get(url = URL, params = '')
    except RequestException as req_err:
        print("Request Exception {0}".format(req_err))
        return(song_title)
    except ConnectionError as conn_err:
        print("Connection Error {0}".format(conn_err))
        return(song_title)
    except ConnectTimeout as timeout_err:
        print("Connection Timeout {0}".format(timeout_err))
        return(song_title)

    soup = BeautifulSoup(r.text, 'html.parser')

    # could be commas in the title, check and re-assemble
    n = 6
    title = ""
    bodylist = soup.body.string.split(',')
    while n < len(bodylist):
        title = title + bodylist[n]
        n = n + 1
        if n < len(bodylist):
            title = title + ","

    m = re.search('http\S+(\s)(.*)', title)
    if m:
        return m.group(2)
    else:
        return(title)


song_title = ""
song_number = 0
output_file = open("songlist.txt", 'w')


while True:
    check_title = print_song_title()

    if song_title != check_title:
        song_number = song_number + 1
        song_title = check_title
        timestamp = datetime.now()
        timestring = timestamp.strftime("%b-%d-%Y (%H:%M:%S)")
        print(timestring, song_title)
        write_song_to_db(timestamp, song_title)
        print(timestring, song_title, sep=' ', end='\n', file=output_file, flush=True)


    time.sleep(10)



#<html><body>69,1,148,500,66,128,David Bowie, Mick Jagger - Dancing in the Street</body></html>
