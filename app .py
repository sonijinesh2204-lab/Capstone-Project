from flask import Flask, render_template_string, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'capstone_event_secret_2024'

DB_PATH = 'registrations.db'

# ── Database Setup ─────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name     TEXT    NOT NULL,
            email         TEXT    NOT NULL,
            phone         TEXT    NOT NULL,
            college       TEXT    NOT NULL,
            year          TEXT    NOT NULL,
            event_name    TEXT    NOT NULL,
            t_shirt_size  TEXT    NOT NULL,
            expectations  TEXT,
            registered_at TEXT    NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ── HTML Templates ─────────────────────────────────────────────────────────

REGISTER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>College Event Registration</title>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
  <style>
    :root {
      --bg:      #f0f4ff;
      --white:   #ffffff;
      --navy:    #1a237e;
      --blue:    #1565c0;
      --accent:  #2979ff;
      --light:   #e3f2fd;
      --border:  #c5cae9;
      --text:    #1a237e;
      --muted:   #546e7a;
      --success: #00897b;
      --radius:  14px;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--bg);
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: var(--text);
      min-height: 100vh;
      background-image:
        radial-gradient(ellipse 70% 50% at 90% 10%, rgba(41,121,255,.10) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 10% 90%, rgba(26,35,126,.08) 0%, transparent 55%);
    }

    .wrapper { max-width: 780px; margin: 0 auto; padding: 40px 20px 70px; }

    /* ── Header ── */
    header { text-align: center; margin-bottom: 36px; }

    .event-badge {
      display: inline-flex; align-items: center; gap: 8px;
      background: var(--navy); color: #fff;
      border-radius: 999px; padding: 6px 20px;
      font-size: 11px; font-weight: 700; letter-spacing: .10em;
      text-transform: uppercase; margin-bottom: 18px;
    }
    .event-badge::before { content: '★'; color: #ffd740; }

    h1 {
      font-size: clamp(1.9rem, 5vw, 2.8rem); font-weight: 800;
      color: var(--navy); line-height: 1.15; margin-bottom: 10px;
    }
    h1 span { color: var(--accent); }
    .subtitle { color: var(--muted); font-size: 15px; font-weight: 400; }

    /* ── Flash ── */
    .flash {
      display: flex; align-items: center; gap: 10px;
      padding: 14px 20px; border-radius: var(--radius);
      font-size: 14px; font-weight: 600; margin-bottom: 24px;
    }
    .flash.success { background: #e0f2f1; border: 1.5px solid #80cbc4; color: var(--success); }
    .flash.error   { background: #fce4ec; border: 1.5px solid #f48fb1; color: #c62828; }

    /* ── Card ── */
    .card {
      background: var(--white); border-radius: 20px;
      padding: 40px 44px;
      box-shadow: 0 4px 6px rgba(26,35,126,.05), 0 20px 60px rgba(26,35,126,.10);
      border: 1px solid var(--border);
      position: relative; overflow: hidden;
    }
    .card::before {
      content: ''; position: absolute; top: 0; left: 0; right: 0;
      height: 4px;
      background: linear-gradient(90deg, var(--navy), var(--accent));
    }

    .section-label {
      font-size: 10.5px; font-weight: 800; letter-spacing: .12em;
      text-transform: uppercase; color: var(--accent);
      margin: 28px 0 16px;
      display: flex; align-items: center; gap: 10px;
    }
    .section-label:first-of-type { margin-top: 0; }
    .section-label::after { content: ''; flex: 1; height: 1.5px; background: var(--border); }

    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
    .full    { grid-column: 1 / -1; }
    @media(max-width:580px){ .grid-2 { grid-template-columns: 1fr; } }

    .field { display: flex; flex-direction: column; gap: 6px; }
    label  { font-size: 12px; font-weight: 600; color: var(--muted); letter-spacing: .03em; }

    input, select, textarea {
      background: var(--light); border: 1.5px solid var(--border);
      border-radius: 10px; padding: 11px 14px;
      color: var(--text); font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 14px; outline: none;
      transition: border-color .2s, box-shadow .2s, background .2s;
    }
    input:focus, select:focus, textarea:focus {
      border-color: var(--accent); background: #fff;
      box-shadow: 0 0 0 3px rgba(41,121,255,.15);
    }
    input::placeholder, textarea::placeholder { color: #b0bec5; }
    select { cursor: pointer; }
    textarea { resize: vertical; min-height: 80px; }

    /* ── Event cards ── */
    .event-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
    @media(max-width:580px){ .event-grid { grid-template-columns: 1fr; } }

    .event-option input[type="radio"] { display: none; }
    .event-option label {
      display: flex; flex-direction: column; align-items: center;
      gap: 6px; padding: 16px 10px;
      background: var(--light); border: 2px solid var(--border);
      border-radius: 12px; cursor: pointer;
      font-size: 12px; font-weight: 600; color: var(--muted);
      text-align: center; transition: all .2s;
      letter-spacing: 0;
    }
    .event-option label .ev-icon { font-size: 26px; }
    .event-option input[type="radio"]:checked + label {
      background: #e8eeff; border-color: var(--accent);
      color: var(--navy); box-shadow: 0 0 0 3px rgba(41,121,255,.12);
    }
    .event-option label:hover { border-color: var(--accent); }

    /* ── Submit ── */
    .btn-submit {
      margin-top: 32px; width: 100%; padding: 15px;
      background: linear-gradient(135deg, var(--navy), var(--accent));
      border: none; border-radius: 12px; color: #fff;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 15px; font-weight: 800; letter-spacing: .03em;
      cursor: pointer; position: relative; overflow: hidden;
      transition: transform .15s, box-shadow .2s;
      box-shadow: 0 4px 20px rgba(41,121,255,.35);
    }
    .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(41,121,255,.45); }
    .btn-submit:active { transform: translateY(0); }
    .btn-submit .ripple {
      position: absolute; border-radius: 50%;
      background: rgba(255,255,255,.3); transform: scale(0);
      animation: ripple .6s linear; pointer-events: none;
    }

    /* ── View link ── */
    .view-link {
      display: flex; align-items: center; justify-content: center; gap: 8px;
      margin-top: 22px; padding: 13px;
      background: var(--white); border: 1.5px solid var(--border);
      border-radius: 12px; color: var(--muted); text-decoration: none;
      font-size: 14px; font-weight: 500;
      transition: all .2s;
    }
    .view-link:hover { border-color: var(--accent); color: var(--accent); background: #e8eeff; }

    @keyframes ripple { to { transform: scale(4); opacity: 0; } }
  </style>
</head>
<body>
<div class="wrapper">
  <header>
    <div class="event-badge">University Event Portal</div>
    <h1>College Event<br/><span>Registration</span></h1>
    <p class="subtitle">Register for Tech Fest, Cultural Events & Workshops</p>
  </header>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
      <div class="flash {{ category }}">
        {% if category == 'success' %}✓{% else %}✕{% endif %} {{ message }}
      </div>
    {% endfor %}
  {% endwith %}

  <div class="card">
    <form method="POST" action="/register" id="regForm">

      <div class="section-label">Personal Details</div>
      <div class="grid-2">
        <div class="field full">
          <label>Full Name</label>
          <input type="text" name="full_name" placeholder="Enter your full name" required/>
        </div>
        <div class="field">
          <label>Email Address</label>
          <input type="email" name="email" placeholder="you@college.edu" required/>
        </div>
        <div class="field">
          <label>Phone Number</label>
          <input type="tel" name="phone" placeholder="+91 98765 43210" required/>
        </div>
        <div class="field">
          <label>College / Institute Name</label>
          <input type="text" name="college" placeholder="e.g. MIT College of Engineering" required/>
        </div>
        <div class="field">
          <label>Year of Study</label>
          <select name="year" required>
            <option value="" disabled selected>Select year</option>
            <option>1st Year</option>
            <option>2nd Year</option>
            <option>3rd Year</option>
            <option>4th Year</option>
          </select>
        </div>
        <div class="field">
          <label>T-Shirt Size</label>
          <select name="t_shirt_size" required>
            <option value="" disabled selected>Select size</option>
            <option>XS</option><option>S</option><option>M</option>
            <option>L</option><option>XL</option><option>XXL</option>
          </select>
        </div>
      </div>

      <div class="section-label">Select Event</div>
      <div class="event-grid">
        <div class="event-option">
          <input type="radio" name="event_name" id="techfest" value="Tech Fest" required/>
          <label for="techfest">
            <span class="ev-icon">💻</span>Tech Fest
          </label>
        </div>
        <div class="event-option">
          <input type="radio" name="event_name" id="cultural" value="Cultural Event"/>
          <label for="cultural">
            <span class="ev-icon">🎭</span>Cultural Event
          </label>
        </div>
        <div class="event-option">
          <input type="radio" name="event_name" id="workshop" value="Workshop"/>
          <label for="workshop">
            <span class="ev-icon">🛠</span>Workshop
          </label>
        </div>
        <div class="event-option">
          <input type="radio" name="event_name" id="sports" value="Sports Meet"/>
          <label for="sports">
            <span class="ev-icon">🏆</span>Sports Meet
          </label>
        </div>
        <div class="event-option">
          <input type="radio" name="event_name" id="hackathon" value="Hackathon"/>
          <label for="hackathon">
            <span class="ev-icon">⚡</span>Hackathon
          </label>
        </div>
        <div class="event-option">
          <input type="radio" name="event_name" id="seminar" value="Seminar"/>
          <label for="seminar">
            <span class="ev-icon">🎓</span>Seminar
          </label>
        </div>
      </div>

      <div class="section-label">Additional Info</div>
      <div class="field">
        <label>What do you expect from this event? (Optional)</label>
        <textarea name="expectations" placeholder="Write your expectations or any special requirements..."></textarea>
      </div>

      <button type="submit" class="btn-submit" id="submitBtn">
        Register for Event →
      </button>
    </form>
  </div>

  <a href="/registrations" class="view-link">
    📋 View All Registrations →
  </a>
</div>

<script>
  const btn = document.getElementById('submitBtn');
  btn.addEventListener('click', function(e) {
    const rect = btn.getBoundingClientRect();
    const r = document.createElement('span');
    r.className = 'ripple';
    const size = Math.max(rect.width, rect.height);
    r.style.cssText = `width:${size}px;height:${size}px;left:${e.clientX-rect.left-size/2}px;top:${e.clientY-rect.top-size/2}px`;
    btn.appendChild(r);
    setTimeout(() => r.remove(), 700);
  });
</script>
</body>
</html>
"""

REGISTRATIONS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>All Registrations</title>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
  <style>
    :root {
      --bg:     #f0f4ff; --white: #ffffff; --navy: #1a237e;
      --accent: #2979ff; --light: #e3f2fd; --border: #c5cae9;
      --text:   #1a237e; --muted: #546e7a;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: var(--bg); font-family: 'Plus Jakarta Sans', sans-serif; color: var(--text); min-height: 100vh; }

    .wrapper { max-width: 1150px; margin: 0 auto; padding: 40px 20px 60px; }

    header {
      display: flex; justify-content: space-between; align-items: flex-start;
      flex-wrap: wrap; gap: 16px; margin-bottom: 32px;
    }
    header h1 { font-size: 2rem; font-weight: 800; color: var(--navy); }
    header p  { color: var(--muted); font-size: 14px; margin-top: 4px; }

    .stat-badge {
      background: var(--navy); color: #fff;
      border-radius: 12px; padding: 12px 22px; text-align: center;
    }
    .stat-badge .num { font-size: 2rem; font-weight: 800; line-height: 1; }
    .stat-badge .lbl { font-size: 10px; text-transform: uppercase; letter-spacing: .08em; opacity: .7; }

    .search-bar {
      margin-bottom: 20px;
      position: relative;
    }
    .search-bar input {
      width: 100%; padding: 11px 16px 11px 42px;
      background: var(--white); border: 1.5px solid var(--border);
      border-radius: 10px; font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 14px; outline: none; color: var(--text);
      transition: border-color .2s;
    }
    .search-bar input:focus { border-color: var(--accent); }
    .search-bar svg { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--muted); }

    .table-card {
      background: var(--white); border-radius: 18px;
      border: 1px solid var(--border); overflow: hidden;
      box-shadow: 0 4px 6px rgba(26,35,126,.05), 0 20px 60px rgba(26,35,126,.08);
      position: relative;
    }
    .table-card::before {
      content: ''; position: absolute; top: 0; left: 0; right: 0;
      height: 4px; background: linear-gradient(90deg, var(--navy), var(--accent));
    }

    .table-scroll { overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    thead tr { background: #e8eeff; border-bottom: 1.5px solid var(--border); }
    th {
      padding: 13px 16px; text-align: left;
      font-size: 10.5px; font-weight: 800; letter-spacing: .10em;
      text-transform: uppercase; color: var(--navy); white-space: nowrap;
    }
    tbody tr { border-bottom: 1px solid #eef0f8; transition: background .15s; }
    tbody tr:last-child { border-bottom: none; }
    tbody tr:hover { background: #f5f7ff; }
    td { padding: 13px 16px; color: #37474f; white-space: nowrap; }

    .name-cell { display: flex; align-items: center; gap: 10px; font-weight: 600; color: var(--navy); }
    .avatar {
      width: 32px; height: 32px; border-radius: 8px;
      background: linear-gradient(135deg, var(--navy), var(--accent));
      display: flex; align-items: center; justify-content: center;
      font-size: 12px; font-weight: 800; color: #fff; flex-shrink: 0;
    }

    .badge {
      display: inline-block; padding: 3px 10px;
      border-radius: 999px; font-size: 11px; font-weight: 600;
    }
    .badge-event { background: #e8eeff; color: var(--accent); border: 1px solid #c5cae9; }
    .badge-year  { background: #e0f2f1; color: #00897b; border: 1px solid #b2dfdb; }

    .empty { padding: 60px; text-align: center; color: var(--muted); }
    .empty .icon { font-size: 3rem; margin-bottom: 12px; }

    .back-link {
      display: inline-flex; align-items: center; gap: 8px;
      margin-top: 22px; padding: 12px 22px;
      background: var(--white); border: 1.5px solid var(--border);
      border-radius: 12px; color: var(--muted); text-decoration: none;
      font-size: 14px; font-weight: 500; transition: all .2s;
    }
    .back-link:hover { border-color: var(--accent); color: var(--accent); }
  </style>
</head>
<body>
<div class="wrapper">
  <header>
    <div>
      <h1>Event Registrations</h1>
      <p>All registered participants</p>
    </div>
    <div class="stat-badge">
      <div class="num">{{ registrations|length }}</div>
      <div class="lbl">Registered</div>
    </div>
  </header>

  <div class="search-bar">
    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
      <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
    </svg>
    <input type="text" id="searchInput" placeholder="Search by name, email or event..."/>
  </div>

  <div class="table-card">
    {% if registrations %}
    <div class="table-scroll">
      <table id="regTable">
        <thead>
          <tr>
            <th>#</th><th>Name</th><th>Email</th><th>Phone</th>
            <th>College</th><th>Year</th><th>Event</th>
            <th>T-Shirt</th><th>Registered On</th>
          </tr>
        </thead>
        <tbody>
          {% for r in registrations %}
          <tr>
            <td style="color:#90a4ae">{{ r.id }}</td>
            <td><div class="name-cell">
              <div class="avatar">{{ r.full_name[0].upper() }}</div>{{ r.full_name }}
            </div></td>
            <td style="color:#78909c">{{ r.email }}</td>
            <td>{{ r.phone }}</td>
            <td>{{ r.college }}</td>
            <td><span class="badge badge-year">{{ r.year }}</span></td>
            <td><span class="badge badge-event">{{ r.event_name }}</span></td>
            <td>{{ r.t_shirt_size }}</td>
            <td style="color:#90a4ae">{{ r.registered_at }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
    {% else %}
    <div class="empty">
      <div class="icon">📋</div>
      <p>No registrations yet. Be the first to register!</p>
    </div>
    {% endif %}
  </div>

  <a href="/" class="back-link">← Back to Registration Form</a>
</div>

<script>
  const search = document.getElementById('searchInput');
  const rows = document.querySelectorAll('#regTable tbody tr');
  search && search.addEventListener('input', () => {
    const q = search.value.toLowerCase();
    rows.forEach(r => { r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none'; });
  });
</script>
</body>
</html>
"""

# ── Routes ─────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template_string(REGISTER_HTML)

@app.route('/register', methods=['POST'])
def register():
    data = {
        'full_name':    request.form.get('full_name', '').strip(),
        'email':        request.form.get('email', '').strip(),
        'phone':        request.form.get('phone', '').strip(),
        'college':      request.form.get('college', '').strip(),
        'year':         request.form.get('year', '').strip(),
        'event_name':   request.form.get('event_name', '').strip(),
        't_shirt_size': request.form.get('t_shirt_size', '').strip(),
        'expectations': request.form.get('expectations', '').strip(),
        'registered_at': datetime.now().strftime('%d %b %Y, %I:%M %p')
    }

    required = ['full_name','email','phone','college','year','event_name','t_shirt_size']
    if not all(data[k] for k in required):
        flash('Please fill all required fields and select an event.', 'error')
        return redirect(url_for('index'))

    conn = get_db()
    conn.execute('''
        INSERT INTO registrations
        (full_name, email, phone, college, year, event_name, t_shirt_size, expectations, registered_at)
        VALUES
        (:full_name, :email, :phone, :college, :year, :event_name, :t_shirt_size, :expectations, :registered_at)
    ''', data)
    conn.commit()
    conn.close()
    flash(f'Registration successful! Welcome, {data["full_name"]}. See you at {data["event_name"]}!', 'success')
    return redirect(url_for('index'))

@app.route('/registrations')
def registrations():
    conn = get_db()
    rows = conn.execute('SELECT * FROM registrations ORDER BY id DESC').fetchall()
    conn.close()
    return render_template_string(REGISTRATIONS_HTML, registrations=rows)

# ── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    print("\n" + "="*55)
    print("  🎓 College Event Registration Portal")
    print("="*55)
    print("  ➜  Form     : http://127.0.0.1:5000")
    print("  ➜  All Data : http://127.0.0.1:5000/registrations")
    print("="*55 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
