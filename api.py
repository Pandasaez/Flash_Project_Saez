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

@app.route("/information", methods = ["GET"])
def get_information():
    cur = mysql.connection.cursor()
    query ="""
    select * from student
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    return make_response(jsonify(data), 200)
@app.route("/information/<int:id", methods=["GET"])
def get_student_by_ID(id):
    cur = mysql.connection.cursor()
    query ="""
    SELECT * FROM information.student WHERE ID = {}
    """.format(id)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    

if __name__ == "__main__":
    app.run(debug=True)
