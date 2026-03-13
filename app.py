from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Simulated Database with nested Participants
event_database = [
    {
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
