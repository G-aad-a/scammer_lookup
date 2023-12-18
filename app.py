import flask
import flask_limiter
from flask_limiter.util import get_remote_address
import sqlite3


    
conn = sqlite3.connect("data.db")


conn.execute("""CREATE TABLE IF NOT EXISTS scammers (id INTEGER PRIMARY KEY AUTOINCREMENT, data VARCHAR(255), reason longtext);""")

with open("scammers.txt", "r") as f:
    for line in f.readlines():
        if line == "":
            break
        data = line.replace("\n", "").split(" - ")
        print(data[0], data[1])
        conn.execute("INSERT INTO `scammers` (`data`, `reason`) VALUES (?, ?)", (data[0], data[1]))
    
with open("scammers.txt", "w") as f:
    f.write("")



conn.commit()

app = flask.Flask(__name__)
limiter = flask_limiter.Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/lookup/<string:data>")
@limiter.limit("50 per hour")
def lookup(data):
    
    if "+45" in data:
        data = data.replace("+45", "")
    data = data.replace(" ", "")
    
    if len(data) > 50 or len(data) < 8:
        return "null"
    
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    
    result = c.execute("SELECT * FROM `scammers` WHERE `data` = ?", (data,)).fetchone()
    conn.close()
    
    if result:
        return result[2]
    else:
        return "Ikke fundet i scammer databasen"
    



app.run(host="0.0.0.0")