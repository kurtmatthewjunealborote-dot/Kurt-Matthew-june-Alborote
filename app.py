from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# A simple list to store the data the user inputs
student_database = []

# HTML Template for a simple input form
HTML_FORM = '''
<!DOCTYPE html>
<html>
<body>
    <h2>Student Entry Form</h2>
    <form action="/add_student" method="post">
        Name: <input type="text" name="name" required><br><br>
        Grade: <input type="number" name="grade" required><br><br>
        Section: <input type="text" name="section" required><br><br>
        <input type="submit" value="Submit Student">
    </form>
    <br>
    <a href="/students">View All Students</a>
</body>
</html>
'''

@app.route('/')
def home():
    # This displays the input form when you visit the home page
    return render_template_string(HTML_FORM)

# FEATURE 1: Input via HTML Form
@app.route('/add_student', methods=['POST'])
def add_student_form():
    name = request.form.get('name')
    grade = request.form.get('grade')
    section = request.form.get('section')
    
    new_student = {"name": name, "grade": grade, "section": section}
    student_database.append(new_student)
    
    return f"<h3>Success! {name} has been added to {section}.</h3> <a href='/'>Go Back</a>"

# FEATURE 2: Input via JSON API (for mobile apps or other scripts)
@app.route('/api/student', methods=['POST'])
def add_student_api():
    data = request.get_json()
    
    if not data or not all(k in data for k in ("name", "grade", "section")):
        return jsonify({"error": "Please provide name, grade, and section"}), 400
    
    student_database.append(data)
    return jsonify({"message": "Student data received!", "student": data}), 201

# FEATURE 3: Display all inputs
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(student_database)

if __name__ == '__main__':
    app.run(debug=True)
