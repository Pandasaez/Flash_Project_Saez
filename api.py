from flask import Flask,make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "JasperSaez3489"
app.config['MYSQL_DB'] = 'information'

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello Testing</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/information", methods = ["GET"])
def get_information():
    data = data_fetch("""select * from information """)
    return make_response(jsonify(data), 200)

@app.route("/information/student/<int:ID>", methods=["GET"])
def get_student_by_id(ID):
    data = data_fetch("""SELECT * FROM student WHERE ID = {}""".format(id))
    return make_response(jsonify(data), 200)
    

if __name__ == "__main__":
    app.run(debug=True)
