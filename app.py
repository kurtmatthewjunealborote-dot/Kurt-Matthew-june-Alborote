from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Simulated Database for Events
event_database = [
    {"id": 1, "name": "Tech Conference 2026", "date": "2026-05-15", "location": "Manila Convention Center", "status": "Upcoming"},
]

# Refactored UI for Event Management
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Event Planner Pro</title>
    <style>
        :root {
            --primary: #1a1a2e;
            --secondary: #16213e;
            --accent: #e94560;
            --glass: rgba(255, 255, 255, 0.1);
        }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: radial-gradient(circle at top left, var(--primary), var(--secondary));
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            color: #eee;
        }
        .container {
            background: var(--glass);
            backdrop-filter: blur(20px);
            padding: 2.5rem;
            border-radius: 24px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            width: 90%;
            max-width: 900px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        h2 { text-align: center; margin-bottom: 2rem; font-weight: 300; letter-spacing: 2px; }
        .form-group { margin-bottom: 15px; }
        input, select {
            width: 100%;
            padding: 12px;
            border-radius: 12px;
            border: none;
            background: rgba(255,255,255,0.08);
            margin-top: 5px;
            box-sizing: border-box;
            color: white;
            outline: none;
        }
        input::placeholder { color: #bbb; }
        .btn {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 12px;
            background: var(--accent);
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
            text-transform: uppercase;
        }
        .btn:hover { filter: brightness(1.2); transform: translateY(-3px); }
        .btn-delete { background: #ff4b2b; width: auto; padding: 6px 12px; font-size: 11px; }
        
        table {
            width: 100%;
            margin-top: 25px;
            border-collapse: separate;
            border-spacing: 0 10px;
        }
        th { text-align: left; padding: 15px; color: #888; font-size: 13px; text-transform: uppercase; }
        td { padding: 15px; background: rgba(255,255,255,0.05); }
        td:first-child { border-radius: 12px 0 0 12px; }
        td:last-child { border-radius: 0 12px 12px 0; }
        
        .status-badge {
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            background: rgba(233, 69, 96, 0.2);
            color: var(--accent);
            border: 1px solid var(--accent);
        }
        .search-box { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>📅 Event Organizer</h2>
        
        <form action="/add_event" method="post">
            <div class="form-group">
                <input type="text" name="name" placeholder="Event Name" required>
            </div>
            <div style="display: flex; gap: 10px;">
                <input type="date" name="date" required>
                <input type="text" name="location" placeholder="Location" required>
            </div>
            <button type="submit" class="btn">Schedule New Event</button>
        </form>

        <hr style="margin: 2rem 0; opacity: 0.1;">

        <div class="search-box">
             <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search events or locations...">
        </div>

        <table id="eventTable">
            <thead>
                <tr>
                    <th>Event Details</th>
                    <th>Date</th>
                    <th>Location</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for event in events %}
                <tr>
                    <td><strong>{{ event.name }}</strong></td>
                    <td>{{ event.date }}</td>
                    <td>{{ event.location }}</td>
                    <td><span class="status-badge">{{ event.status }}</span></td>
                    <td>
                        <form action="/delete/{{ event.id }}" method="POST" style="display:inline;">
                            <button class="btn btn-delete">Cancel</button>
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
            let table = document.getElementById("eventTable");
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
    return render_template_string(HTML_TEMPLATE, events=event_database)

@app.route('/add_event', methods=['POST'])
def add_event_form():
    name = request.form.get('name')
    date = request.form.get('date')
    location = request.form.get('location')
    
    new_event = {
        "id": len(event_database) + 1,
        "name": name, 
        "date": date, 
        "location": location,
        "status": "Upcoming"
    }
    event_database.append(new_event)
    return redirect(url_for('home'))

@app.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    global event_database
    event_database = [e for e in event_database if e['id'] != event_id]
    return redirect(url_for('home'))

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(event_database)

if __name__ == '__main__':
    app.run(debug=True)
