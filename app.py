import os
from flask import Flask, request, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "event_system_secret"

# --- DATABASE CONFIGURATION ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    # This connects the Event to all its Participants
    participants = db.relationship('Participant', backref='event', lazy=True)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    reg_time = db.Column(db.DateTime, default=datetime.utcnow)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()
    if not Event.query.first():
        e1 = Event(name="Tech Summit 2026", date="2026-05-15", location="Manila")
        e2 = Event(name="Web Dev Workshop", date="2026-06-20", location="Cebu")
        db.session.add_all([e1, e2])
        db.session.commit()

# --- STYLES ---
CSS = '''
<style>
    :root { --bg: #0f172a; --card: #1e293b; --accent: #38bdf8; --text: #f1f5f9; }
    body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 40px 20px; }
    .container { max-width: 900px; margin: auto; }
    .card { background: var(--card); padding: 25px; border-radius: 15px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1); }
    .btn { background: var(--accent); color: var(--bg); padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; border: none; cursor: pointer; display: inline-block; transition: 0.3s; }
    .btn-outline { background: transparent; border: 1px solid var(--accent); color: var(--accent); margin-left: 10px; }
    .btn:hover { opacity: 0.8; transform: translateY(-2px); }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { text-align: left; padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); }
    input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box; }
    .nav { margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }
</style>
'''

# --- ROUTES ---

@app.route('/')
def home():
    events = Event.query.all()
    content = f'''
    <div class="nav">
        <h1>📅 Event Registration</h1>
        <a href="/dashboard" class="btn btn-outline">View Attendance Dashboard</a>
    </div>
    '''
    for e in events:
        content += f'''
        <div class="card">
            <h2>{e.name}</h2>
            <p>📍 {e.location} | 📅 {e.date}</p>
            <p><small>{len(e.participants)} registered attendees</small></p>
            <a href="/register/{e.id}" class="btn">Register My Attendance</a>
        </div>
        '''
    return render_template_string(CSS + f'<div class="container">{content}</div>')

@app.route('/register/<int:event_id>')
def register_page(event_id):
    event = Event.query.get_or_404(event_id)
    form = f'''
    <div class="card" style="max-width: 450px; margin: auto;">
        <a href="/" style="color: var(--accent); text-decoration: none;">← Back to Events</a>
        <h2 style="margin-top:20px;">Join {event.name}</h2>
        <form action="/submit/{event.id}" method="POST">
            <input type="text" name="name" placeholder="Full Name" required>
            <input type="email" name="email" placeholder="Email Address" required>
            <button type="submit" class="btn" style="width:100%">Confirm Registration</button>
        </form>
    </div>
    '''
    return render_template_string(CSS + f'<div class="container">{form}</div>')

@app.route('/submit/<int:event_id>', methods=['POST'])
def submit(event_id):
    name = request.form.get('name')
    email = request.form.get('email')
    
    new_attendee = Participant(name=name, email=email, event_id=event_id)
    db.session.add(new_attendee)
    db.session.commit()
    
    return render_template_string(CSS + f'''
    <div class="container" style="text-align:center; padding-top: 50px;">
        <div class="card">
            <h1 style="font-size: 50px;">🎉</h1>
            <h1>Registration Confirmed!</h1>
            <p>Thank you <strong>{name}</strong>. We've added you to the guest list.</p>
            <a href="/" class="btn">Back to Home</a>
            <a href="/dashboard" class="btn btn-outline">View Guest List</a>
        </div>
    </div>
    ''')

# --- NEW: ATTENDANCE DATABASE VIEW ---
@app.route('/dashboard')
def dashboard():
    events = Event.query.all()
    content = '<a href="/" style="color: var(--accent); text-decoration: none;">← Back to Home</a>'
    content += '<h1>📊 Attendance Dashboard</h1>'
    
    for e in events:
        content += f'''
        <div class="card">
            <h3>{e.name} - Guest List</h3>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Date Registered</th>
                </tr>
        '''
        if not e.participants:
            content += '<tr><td colspan="3" style="text-align:center; opacity:0.5;">No registrations yet.</td></tr>'
        else:
            for p in e.participants:
                content += f'''
                <tr>
                    <td>{p.name}</td>
                    <td>{p.email}</td>
                    <td>{p.reg_time.strftime('%Y-%m-%d %H:%M')}</td>
                </tr>
                '''
        content += '</table></div>'
        
    return render_template_string(CSS + f'<div class="container">{content}</div>')

if __name__ == '__main__':
    app.run(debug=True)
