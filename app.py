from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Simulated Database
student_database = [
    {"id": 1, "name": "Juan Dela Cruz", "grade": 10, "section": "Zechariah"},
]

# Modern UI with CSS (Glassmorphism + Gradients)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Management System</title>
    <style>
        :root {
            --primary: #6a11cb;
            --secondary: #2575fc;
            --glass: rgba(255, 255, 255, 0.2);
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            color: white;
        }
        .container {
            background: var(--glass);
            backdrop-filter: blur(15px);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            width: 90%;
            max-width: 800px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        h2 { text-align: center; margin-bottom: 1.5rem; }
        .form-group { margin-bottom: 15px; }
        input {
            width: 100%;
            padding: 10px;
            border-radius: 10px;
            border: none;
            background: rgba(255,255,255,0.9);
            margin-top: 5px;
            box-sizing: border-box;
        }
        .btn {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 10px;
            background: #00d2ff;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
            margin-top: 10px;
        }
        .btn:hover { background: #3a7bd5; transform: translateY(-2px); }
        .btn-delete { background: #ff4b2b; width: auto; padding: 5px 10px; font-size: 12px; }
        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
            background: rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }
        th { background: rgba(0,0,0,0.2); }
        .search-box { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🎓 Student Registry</h2>
        
        <form action="/add_student" method="post">
            <div class="form-group">
                <input type="text" name="name" placeholder="Full Name" required>
            </div>
            <div style="display: flex; gap: 10px;">
                <input type="number" name="grade" placeholder="Grade Level" required>
                <input type="text" name="section" placeholder="Section" required>
            </div>
            <button type="submit" class="btn">Add Student Record</button>
        </form>

        <hr style="margin: 2rem 0; opacity: 0.2;">

        <div class="search-box">
             <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search names or sections...">
        </div>

        <table id="studentTable">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Grade</th>
                    <th>Section</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for student in students %}
                <tr>
                    <td>{{ student.name }}</td>
                    <td>{{ student.grade }}</td>
                    <td>{{ student.section }}</td>
                    <td>
                        <form action="/delete/{{ student.id }}" method="POST" style="display:inline;">
                            <button class="btn btn-delete">Delete</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <script>
        function searchTable() {
            let input = document.getElementById("searchInput").value.toUpperCase();
            let table = document.getElementById("studentTable");
            let tr = table.getElementsByTagName("tr");

            for (let i = 1; i < tr.length; i++) {
                let text = tr[i].textContent || tr[i].innerText;
                tr[i].style.display = text.toUpperCase().indexOf(input) > -1 ? "" : "none";
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    # Pass the student database to the HTML template
    return render_template_string(HTML_TEMPLATE, students=student_database)

@app.route('/add_student', methods=['POST'])
def add_student_form():
    name = request.form.get('name')
    grade = request.form.get('grade')
    section = request.form.get('section')
    
    new_student = {
        "id": len(student_database) + 1,
        "name": name, 
        "grade": grade, 
        "section": section
    }
    student_database.append(new_student)
    return redirect(url_for('home'))

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    global student_database
    student_database = [s for s in student_database if s['id'] != student_id]
    return redirect(url_for('home'))

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(student_database)

if __name__ == '__main__':
    app.run(debug=True)
