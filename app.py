from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database: A list of students
students = [
    {"id": 1, "name": "Jane Doe", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "John Smith", "grade": 11, "section": "Genesis"}
]

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Welcome to the Student Portal API",
        "endpoints": ["/students (GET)", "/student/<id> (GET)", "/student (POST)"]
    })

# Feature 1: Get ALL students
@app.route('/students', methods=['GET'])
def get_all_students():
    return jsonify({"count": len(students), "students": students})

# Feature 2: Get a SPECIFIC student by ID (Dynamic Route)
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

# Feature 3: ADD a new student (POST request)
@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()
    
    # Basic validation
    if not data or "name" not in data:
        return jsonify({"error": "Missing required data"}), 400
    
    new_student = {
        "id": len(students) + 1,
        "name": data.get("name"),
        "grade": data.get("grade", "N/A"),
        "section": data.get("section", "General")
    }
    students.append(new_student)
    return jsonify({"message": "Student added successfully!", "student": new_student}), 201

if __name__ == '__main__':
    # Setting debug=True helps during development
    app.run(debug=True)
