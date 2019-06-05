from flask import Flask, request, abort, Blueprint
import psycopg2 as psy
import datetime
import os
import random
import sys
import json


con = psy.connect(
        host=os.environ.get("DBHOST", "db"),
        database=os.environ.get("DBNAME","app"),
        user=os.environ.get("DBUSER", "postgres"),
        password=os.environ.get("DBPASSWORD", "secret")
)

def create_table(connection):
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS anagrams (id serial PRIMARY KEY, anagram varchar, origin varchar);")
    connection.commit()
    cur.close()

def check_existing(connection, word, anagram):
    cur = connection.cursor()
    cur.execute("SELECT * FROM anagrams WHERE origin = '" + word + "' and anagram = '" + anagram + "';")
    result = cur.fetchone() is None
    cur.close()
    return result
    
def scramble_word(word):
    return "".join(random.sample(word, len(word)))

def check_anagram(connection, anagram, word):
    cur = connection.cursor()
    cur.execute("SELECT origin FROM anagrams WHERE anagram = '" + anagram  +"';")
    result = cur.fetchone()
    cur.close()
    return result is not None and result[0] == word

def write_db(connection, anagram, origin):
    cur = connection.cursor()
    try:
        cur.execute("INSERT INTO anagrams (anagram, origin) VALUES ('" + anagram + "','" + origin +"' );")
    except:
        connection.rollback()
    connection.commit()
    cur.close()

def get_random_anagram(connection):
    cur = connection.cursor()
    cur.execute("SELECT anagram FROM anagrams;")
    result = cur.fetchall()
    cur.close
    return random.choice(result)[0]


bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/check')
def check_anagram_call():
    anagram = request.args.get('anagram', default = "", type = str)
    word = request.args.get('word', default = "", type = str)
    if anagram is "" or word is "":
        return abort(400)
    return json.dumps(check_anagram(con, anagram, word))

@bp.route('/create')
def create_anagram_call():
    word = request.args.get('word').lower()
    anagram = scramble_word(word) 
    if check_existing(con, word, anagram):
        write_db(con, anagram, word)
    return anagram

@bp.route('/get')
def get_anagram_call():
    return get_random_anagram(con)

app = Flask(__name__)
app.register_blueprint(bp)
if __name__ == '__main__':
    create_table(con)
    app.run(debug=True, host='0.0.0.0')
