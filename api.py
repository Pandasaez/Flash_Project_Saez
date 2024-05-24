from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "many random bytes"

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "JasperSaez3489"
app.config['MYSQL_DB'] = 'information'

mysql = MySQL(app)

# Create a new student using JSON data
@app.route("/insert", methods=['POST'])
def insert():
    try:
        data = request.get_json()
        id = data.get('ID')
        name = data.get('name')
        age = data.get('age')
        college = data.get('college')

        if not id or not name or not age or not college:
            return jsonify({"error": "Missing data"}), 400

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student (ID, `Student Name`, `Age`, `College`) VALUES (%s, %s, %s, %s)", (id, name, age, college))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Data Inserted Successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Read all students
@app.route("/", methods=['GET'])
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student")
        data = cur.fetchall()
        cur.close()

        students = []
        for row in data:
            student = {
                "ID": row[0],
                "Student Name": row[1],
                "Age": row[2],
                "College": row[3]
            }
            students.append(student)

        return jsonify({"students": students}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update a student using JSON data
@app.route('/update/<int:id_data>', methods=['PUT'])
def update(id_data):
    try:
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        college = data.get('college')

        if not name or not age or not college:
            return jsonify({"error": "Missing data"}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE student SET `Student Name`=%s, `Age`=%s, `College`=%s
        WHERE ID=%s
        """, (name, age, college, id_data))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Data Updated Successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a student
@app.route('/delete/<int:id_data>', methods=['DELETE'])
def delete(id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM student WHERE ID=%s", (id_data,))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Record Has Been Deleted Successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
