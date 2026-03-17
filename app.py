from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Simulated Database with nested Participants
event_database = [
    {from flask import Flask, request, render_template_string, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Simulated Database with more detailed participant objects
event_database = [
    {
        "id": 1, 
        "name": "Tech Conference 2026", 
        "date": "2026-05-15", 
        "location": "Manila Convention Center", 
        "status": "Open",
        "participants": [
            {"name": "Alice Robertson", "email": "alice@example.com", "time": "2026-01-10"},
        ]
    },
    {
        "id": 2, 
        "name": "Music Festival", 
        "date": "2026-07-20", 
        "location": "BGC Amphitheater", 
        "status": "Open",
        "participants": []
    },
]

COMMON_STYLE = '''
<style>
    :root { --primary: #0f172a; --secondary: #1e293b; --accent: #38bdf8; --glass: rgba(255, 255, 255, 0.05); }
    body {
        font-family: 'Inter', sans-serif;
        background: radial-gradient(circle at top right, var(--secondary), var(--primary));
        min-height: 100vh; margin: 0; color: #f1f5f9; display: flex; justify-content: center; padding: 40px 20px;
    }
    .container {
        background: var(--glass); backdrop-filter: blur(12px); padding: 2.5rem;
        border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);
        width: 100%; max-width: 900px; height: fit-content;
    }
    .event-card {
        background: rgba(255,255,255,0.03); border-radius: 15px; padding: 20px;
        margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .btn {
        padding: 12px 24px; border: none; border-radius: 8px;
        background: var(--accent); color: #0f172a; font-weight: 600;
        cursor: pointer; transition: 0.2s; text-decoration: none;
    }
    .btn:hover { opacity: 0.9; transform: scale(1.02); }
    .btn-outline { background: transparent; border: 1px solid var(--accent); color: var(--accent); }
    input {
        width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; 
        border: 1px solid rgba(255,255,255,0.2); background: rgba(0,0,0,0.2); color: white;
    }
    .badge { font-size: 0.75rem; padding: 4px 12px; border-radius: 99px; background: #22c55e; color: white; }
</style>
'''

# --- TEMPLATES ---

MAIN_PAGE = COMMON_STYLE + '''
<div class="container">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
        <h2>🚀 Available Events</h2>
        <span style="opacity: 0.6;">Select an event to register your attendance</span>
    </div>

    {% for event in events %}
    <div class="event-card">
        <div>
            <span class="badge">{{ event.status }}</span>
            <h3 style="margin: 10px 0 5px 0;">{{ event.name }}</h3>
            <p style="margin: 0; opacity: 0.7; font-size: 0.9rem;">📍 {{ event.location }} | 📅 {{ event.date }}</p>
        </div>
        <div>
            <a href="/register/{{ event.id }}" class="btn">Register Attendance</a>
        </div>
    </div>
    {% endfor %}
</div>
'''

REGISTRATION_PAGE = COMMON_STYLE + '''
<div class="container" style="max-width: 500px;">
    <a href="/" style="color: var(--accent); text-decoration: none; font-size: 0.9rem;">← Back to Events</a>
    <h2 style="margin-top: 20px;">Register for Attendance</h2>
    <p style="opacity: 0.8;">Event: <strong>{{ event.name }}</strong></p>
    
    <form action="/submit_registration/{{ event.id }}" method="POST" style="margin-top: 20px;">
        <label>Full Name</label>
        <input type="text" name="full_name" placeholder="John Doe" required>
        
        <label>Email Address</label>
        <input type="email" name="email" placeholder="john@example.com" required>
        
        <button type="submit" class="btn" style="width: 100%; margin-top: 15px;">Confirm Registration</button>
    </form>
</div>
'''

SUCCESS_PAGE = COMMON_STYLE + '''
<div class="container" style="max-width: 500px; text-align: center;">
    <h1 style="font-size: 4rem; margin: 0;">✅</h1>
    <h2>Registration Confirmed!</h2>
    <p>You have been added to the guest list for <strong>{{ event_name }}</strong>.</p>
    <br>
    <a href="/" class="btn btn-outline">Return Home</a>
</div>
'''

# --- ROUTES ---

@app.route('/')
def home():
    return render_template_string(MAIN_PAGE, events=event_database)

@app.route('/register/<int:event_id>')
def register_view(event_id):
    event = next((e for e in event_database if e['id'] == event_id), None)
    if event:
        return render_template_string(REGISTRATION_PAGE, event=event)
    return "Event not found", 404

@app.route('/submit_registration/<int:event_id>', methods=['POST'])
def submit_registration(event_id):
    event = next((e for e in event_database if e['id'] == event_id), None)
    if event:
        name = request.form.get('full_name')
        email = request.form.get('email')
        
        # Add participant with timestamp
        new_participant = {
            "name": name,
            "email": email,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        event['participants'].append(new_participant)
        
        return render_template_string(SUCCESS_PAGE, event_name=event['name'])
    return "Error processing registration", 400

if __name__ == '__main__':
    app.run(debug=True)
        "id": 1, 
        "name": "Tech Conference 2026", 
        "date": "2026-05-15", 
        "location": "Manila Convention Center", 
        "status": "Upcoming",
        "participants": ["Alice Robertson", "Bob Marlow", "Charlie Day"]
    },
    {
        "id": 2, 
        "name": "Music Festival", 
        "date": "2026-07-20", 
        "location": "BGC Amphitheater", 
        "status": "Planning",
        "participants": ["David Guetta", "Eve Online"]
    },
]

# --- SHARED CSS ---
COMMON_STYLE = '''
<style>
    :root { --primary: #1a1a2e; --secondary: #16213e; --accent: #e94560; --glass: rgba(255, 255, 255, 0.1); }
    body {
        font-family: 'Segoe UI', sans-serif;
        background: radial-gradient(circle at top left, var(--primary), var(--secondary));
        min-height: 100vh; display: flex; justify-content: center; align-items: center; margin: 0; color: #eee;
    }
    .container {
        background: var(--glass); backdrop-filter: blur(20px); padding: 2rem;
        border-radius: 24px; box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        width: 90%; max-width: 800px; border: 1px solid rgba(255,255,255,0.1);
    }
    .btn {
        padding: 10px 20px; border: none; border-radius: 12px;
        background: var(--accent); color: white; font-weight: bold;
        cursor: pointer; transition: 0.3s; text-decoration: none; display: inline-block;
    }
    .btn:hover { filter: brightness(1.2); transform: translateY(-2px); }
    .btn-secondary { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); }
    table { width: 100%; border-collapse: separate; border-spacing: 0 10px; margin-top: 20px; }
    td { padding: 15px; background: rgba(255,255,255,0.05); }
    td:first-child { border-radius: 12px 0 0 12px; }
    td:last-child { border-radius: 0 12px 12px 0; }
    .status-badge { padding: 4px 10px; border-radius: 20px; font-size: 11px; background: rgba(233, 69, 96, 0.2); color: var(--accent); border: 1px solid var(--accent); }
</style>
'''

# --- TEMPLATES ---
MAIN_PAGE = COMMON_STYLE + '''
<div class="container">
    <h2>📅 Event Organizer</h2>
    <form action="/add_event" method="post" style="display: grid; gap: 10px;">
        <input type="text" name="name" placeholder="Event Name" required style="padding:12px; border-radius:10px; border:none;">
        <div style="display: flex; gap: 10px;">
            <input type="date" name="date" required style="flex:1; padding:12px; border-radius:10px; border:none;">
            <input type="text" name="location" placeholder="Location" required style="flex:1; padding:12px; border-radius:10px; border:none;">
        </div>
        <button type="submit" class="btn">Schedule New Event</button>
    </form>

    <table>
        <thead>
            <tr>
                <th>Event Name</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for event in events %}
            <tr>
                <td><strong>{{ event.name }}</strong><br><small>{{ event.date }}</small></td>
                <td><span class="status-badge">{{ event.status }}</span></td>
                <td>
                    <a href="/event/{{ event.id }}" class="btn" style="font-size: 12px;">View Guests</a>
                    <form action="/delete/{{ event.id }}" method="POST" style="display:inline;">
                        <button class="btn btn-secondary" style="font-size: 12px; color: #ff4b2b;">Cancel</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
'''

EVENT_DETAILS_PAGE = COMMON_STYLE + '''
<div class="container">
    <a href="/" class="btn btn-secondary" style="margin-bottom: 20px;">← Back to Schedule</a>
    <h2>👥 {{ event.name }}</h2>
    <p><strong>Location:</strong> {{ event.location }} | <strong>Date:</strong> {{ event.date }}</p>
    
    <hr style="opacity: 0.1; margin: 20px 0;">
    
    <h3>Add Participant</h3>
    <form action="/add_participant/{{ event.id }}" method="post" style="display: flex; gap: 10px;">
        <input type="text" name="guest_name" placeholder="Guest Full Name" required style="flex:1; padding:12px; border-radius:10px; border:none;">
        <button type="submit" class="btn">Add Guest</button>
    </form>

    <h3 style="margin-top: 30px;">Guest List ({{ event.participants|length }})</h3>
    <ul>
        {% for person in event.participants %}
            <li style="background: rgba(255,255,255,0.05); margin: 5px 0; padding: 10px; border-radius: 8px; list-style: none;">
                👤 {{ person }}
            </li>
        {% else %}
            <p style="color: #888;">No participants added yet.</p>
        {% endfor %}
    </ul>
</div>
'''

# --- ROUTES ---

@app.route('/')
def home():
    return render_template_string(MAIN_PAGE, events=event_database)

@app.route('/event/<int:event_id>')
def view_event(event_id):
    # Find the event by ID
    event = next((e for e in event_database if e['id'] == event_id), None)
    if event:
        return render_template_string(EVENT_DETAILS_PAGE, event=event)
    return "Event not found", 404

@app.route('/add_event', methods=['POST'])
def add_event_form():
    new_event = {
        "id": len(event_database) + 1,
        "name": request.form.get('name'), 
        "date": request.form.get('date'), 
        "location": request.form.get('location'),
        "status": "Upcoming",
        "participants": []
    }
    event_database.append(new_event)
    return redirect(url_for('home'))

@app.route('/add_participant/<int:event_id>', methods=['POST'])
def add_participant(event_id):
    event = next((e for e in event_database if e['id'] == event_id), None)
    if event:
        guest_name = request.form.get('guest_name')
        if guest_name:
            event['participants'].append(guest_name)
    return redirect(url_for('view_event', event_id=event_id))

@app.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    global event_database
    event_database = [e for e in event_database if e['id'] != event_id]
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
