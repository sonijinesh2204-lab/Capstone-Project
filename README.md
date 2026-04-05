# 🎓 Cloud-Based College Event Registration System
### Google Cloud Digital Leader — Capstone Project

A full-stack web application for college event registrations, built as a local prototype using Flask + SQLite, with a proposed Google Cloud architecture for production deployment.

---

## 📌 Project Overview

Students can register for college events (Tech Fest, Cultural Events, Workshops, etc.) through a web form. All registration data is stored in a database. The local prototype uses Flask + SQLite; the cloud version uses Google Cloud Run + Firestore.

---

## 🖥️ Local Prototype — How to Run

### Prerequisites
- Python 3.8 or above installed
- pip package manager

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/capstone-project.git
cd capstone-project
```

### Step 2 — Install Dependencies
```bash
pip install flask
```

### Step 3 — Run the Application
```bash
python app.py
```

### Step 4 — Open in Browser
```
Registration Form  : http://127.0.0.1:5000
View Registrations : http://127.0.0.1:5000/registrations
```

> Keep the terminal/CMD window open while using the app.

---

## 📁 Project Structure

```
capstone-project/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── registrations.db    # SQLite database (auto-created on first run)
```

---

## 🗄️ Database Schema

**Table: `registrations`**

| Column         | Type    | Description                  |
|----------------|---------|------------------------------|
| id             | INTEGER | Auto-increment primary key   |
| full_name      | TEXT    | Student's full name          |
| email          | TEXT    | Email address                |
| phone          | TEXT    | Phone number                 |
| college        | TEXT    | College/Institute name       |
| year           | TEXT    | Year of study                |
| event_name     | TEXT    | Selected event               |
| t_shirt_size   | TEXT    | T-shirt size                 |
| expectations   | TEXT    | Optional expectations        |
| registered_at  | TEXT    | Registration timestamp       |

---

## ☁️ Google Cloud Architecture (Proposed)

| Component         | Local (Prototype)  | Google Cloud (Production)     |
|-------------------|--------------------|-------------------------------|
| Web Hosting       | Flask (localhost)  | Cloud Run (serverless)        |
| Database          | SQLite (.db file)  | Firestore (NoSQL)             |
| Public Access     | localhost:5000     | Cloud Run public URL (HTTPS)  |
| Loose Coupling    | Direct DB calls    | Pub/Sub messaging             |
| Container         | None               | Docker + Artifact Registry    |

### Migration Steps (Local → Cloud)
1. Replace SQLite with **Google Firestore** SDK
2. Containerize app using **Docker**
3. Push image to **Artifact Registry**
4. Deploy container to **Cloud Run**
5. Pub/Sub topic for future integrations

---

## 🔧 Google Cloud Services Used

- **Cloud Run** — Serverless hosting, auto-scales, no server management
- **Firestore** — Scalable NoSQL cloud database
- **Pub/Sub** — For loose coupling with future services
- **Artifact Registry** — Stores Docker container image
- **Cloud Build** — CI/CD pipeline for deployment

---

## ✅ Features

- Interactive event registration form
- 6 event types: Tech Fest, Cultural Event, Workshop, Sports Meet, Hackathon, Seminar
- Real-time form validation
- Success/error flash messages
- Live searchable registrations table
- Colour-coded event badges
- Responsive design (mobile-friendly)
- Ripple button animation

---

## 👩‍💻 Author
**Purvi** — Google Cloud Digital Leader, Semester 2 Capstone Project
