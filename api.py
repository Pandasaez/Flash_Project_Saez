# Import necessary libraries
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# Initialize the Flask app
app = Flask(__name__)

# Secret key for session management
app.secret_key = "many random bytes"

# Configuration for MySQL database connection
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "JasperSaez3489"
app.config['MYSQL_DB'] = 'information'

# Configuration for JWT
app.config['JWT_SECRET_KEY'] = 'IT'  
jwt = JWTManager(app)

# Initialize MySQL
mysql = MySQL(app)

# For login user and login
users = {
    'Jasper': 'Saez'
}

# Login route to generate JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if username and password are correct
    if username in users and users[username] == password:
        # Create access token
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        # Return error if credentials are invalid
        return jsonify({"error": "Invalid credentials"}), 401

# Protected route that requires JWT token
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    # Return the current user's identity
    return jsonify(logged_in_as=current_user), 200

# Route to insert a new student record (protected route)
@app.route("/insert", methods=['POST'])
@jwt_required()
def insert():
    try:
        data = request.get_json()
        id = data.get('ID')
        name = data.get('name')
        age = data.get('age')
        college = data.get('college')

        # Check if all required fields are provided
        if not id or not name or not age or not college:
            return jsonify({"error": "Missing data"}), 400

        cur = mysql.connection.cursor()
        # Insert new student record into the database
        cur.execute("INSERT INTO student (ID, `Student Name`, `Age`, `College`) VALUES (%s, %s, %s, %s)", (id, name, age, college))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Data Inserted Successfully"}), 201
    except Exception as e:
        # Return error if any exception occurs
        return jsonify({"error": str(e)}), 400

# Route to read all student records (protected route)
@app.route("/", methods=['GET'])
@jwt_required()
def index():
    try:
        cur = mysql.connection.cursor()
        # Select all student records from the database
        cur.execute("SELECT * FROM student")
        data = cur.fetchall()
        cur.close()

        students = []
        # Convert fetched data into a list of dictionaries
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
        # Return error if any exception occurs
        return jsonify({"error": str(e)}), 500

# Route to update an existing student record (protected route)
@app.route('/update/<int:id_data>', methods=['PUT'])
@jwt_required()
def update(id_data):
    try:
        data = request.get_json()
        new_id = data.get('ID')
        name = data.get('name')
        age = data.get('age')
        college = data.get('college')

        # Check if all required fields are provided
        if not name or not age or not college:
            return jsonify({"error": "Missing data"}), 400

        cur = mysql.connection.cursor()
        # Update the student record in the database
        cur.execute("""
        UPDATE student SET `ID`=%s, `Student Name`=%s, `Age`=%s, `College`=%s
        WHERE ID=%s
        """, (new_id, name, age, college, id_data))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Data Updated Successfully"}), 200
    except Exception as e:
        # Return error if any exception occurs
        return jsonify({"error": str(e)}), 400

# Route to delete a student record (protected route)
@app.route('/delete/<int:id_data>', methods=['DELETE'])
@jwt_required()
def delete(id_data):
    try:
        cur = mysql.connection.cursor()
        # Delete the student record from the database
        cur.execute("DELETE FROM student WHERE ID=%s", (id_data,))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Record Has Been Deleted Successfully"}), 200
    except Exception as e:
        # Return error if any exception occurs
        return jsonify({"error": str(e)}), 400

# Route to search for student records by name (protected route)
@app.route('/search', methods=['GET'])
@jwt_required()
def search_by_name():
    try:
        # Get search query (name) from query parameters
        search_name = request.args.get('name')
        
        if not search_name:
            return jsonify({"error": "Missing search query"}), 400

        cur = mysql.connection.cursor()
        # Search for student records based on the provided name query
        cur.execute("""
        SELECT * FROM student
        WHERE `Student Name` LIKE %s
        """, (f"%{search_name}%",))
        data = cur.fetchall()
        cur.close()

        students = []
        # Convert fetched data into a list of dictionaries
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
        # Return error if any exception occurs
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
