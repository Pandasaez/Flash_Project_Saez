from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "many random bytes"

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "JasperSaez3489"
app.config['MYSQL_DB'] = 'information'

mysql = MySQL(app)

@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    data = cur.fetchall()
    cur.close()
    
    # Debugging: Print the data to check what is being returned
    print(data)
    
    return render_template("index.html", students=data)

if __name__ == "__main__":
    app.run(debug=True)
