from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.secret_key = "many random bytes"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "JasperSaez3489"
app.config['MYSQL_DB'] = 'information'

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'IT'  
jwt = JWTManager(app)

mysql = MySQL(app)

# Information for Password and Username
users = {
    'Jasper': 'Saez'
}

# Login route to generate JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Protected route that requires JWT token
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Create a new student using JSON data (protected route)
@app.route("/insert", methods=['POST'])
@jwt_required()
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

# Read all students (protected route)
@app.route("/", methods=['GET'])
@jwt_required()
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

# Update a student using JSON data (protected route)
@app.route('/update/<int:id_data>', methods=['PUT'])
@jwt_required()
def update(id_data):
    try:
        data = request.get_json()
        new_id = data.get('ID')
        name = data.get('name')
        age = data.get('age')
        college = data.get('college')

        if not name or not age or not college:
            return jsonify({"error": "Missing data"}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE student SET `ID`=%s, `Student Name`=%s, `Age`=%s, `College`=%s
        WHERE ID=%s
        """, (new_id, name, age, college, id_data))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Data Updated Successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Delete a student (protected route)
@app.route('/delete/<int:id_data>', methods=['DELETE'])
@jwt_required()
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
