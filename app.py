import os
from flask import Flask, request, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "event_system_secret"

# --- DATABASE CONFIGURATION ---
# This setup works both locally and on Render
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
    participants = db.relationship('Participant', backref='event', lazy=True)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    reg_time = db.Column(db.DateTime, default=datetime.utcnow)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

# Initialize database tables
with app.app_context():
    db.create_all()
    # Add seed data if the database is empty
    if not Event.query.first():
        sample_event = Event(name="Tech Summit 2026", date="2026-05-15", location="Manila")
        db.session.add(sample_event)
        db.session.commit()

# --- STYLES ---
CSS = '''
<style>
    :root { --bg: #0f172a; --card: #1e293b; --accent: #38bdf8; --text: #f1f5f9; }
    body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 40px 20px; }
    .container { max-width: 800px; margin: auto; }
    .card { background: var(--card); padding: 25px; border-radius: 15px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1); }
    .btn { background: var(--accent); color: var(--bg); padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; border: none; cursor: pointer; display: inline-block; }
    input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box; }
</style>
'''

# --- ROUTES ---

@app.route('/')
def home():
    events = Event.query.all()
    content = f"<h1>📅 Event Registration</h1>"
    for e in events:
        content += f'''
        <div class="card">
            <h2>{e.name}</h2>
            <p>📍 {e.location} | 📅 {e.date}</p>
            <p><small>{len(e.participants)} registered so far</small></p>
            <a href="/register/{e.id}" class="btn">Register My Attendance</a>
        </div>
        '''
    return render_template_string(CSS + f'<div class="container">{content}</div>')

@app.route('/register/<int:event_id>')
def register_page(event_id):
    event = Event.query.get_or_404(event_id)
    form = f'''
    <div class="card" style="max-width: 400px; margin: auto;">
        <h2>Register for {event.name}</h2>
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
    <div class="container" style="text-align:center;">
        <div class="card">
            <h1>✅ Success!</h1>
            <p>Thank you {name}, your attendance for event #{event_id} is recorded.</p>
            <a href="/" class="btn">Return to Events</a>
        </div>
    </div>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
