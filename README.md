# 🚀 Alumni Management System

A modern full-stack web application designed to **connect students and alumni**, enabling mentorship, networking, and event participation within an institution.

---

## 📌 Overview

The **Alumni Management System** provides a centralized platform where students can interact with alumni, seek mentorship, and stay updated with institutional activities.

It helps in:

* Strengthening alumni engagement
* Building professional networks
* Facilitating career guidance

---

## ✨ Key Features

### 👤 Role-Based Access

* **Student**

  * Request mentorship
  * Explore alumni directory
* **Alumni**

  * Accept/reject mentorship requests
  * Update professional profile
* **Admin**

  * Manage announcements
  * Create and manage events

---

### 🤝 Mentorship System

* Students can send mentorship requests
* Alumni can accept or reject requests
* Once accepted:

  * 📧 Direct email communication
  * 🔗 LinkedIn profile access

---

### 📊 Dashboard Analytics

* Personalized dashboard for each user
* Displays:

  * Mentorship request count
  * Total alumni
  * Total events
* Shows latest announcements & upcoming events

---

### 📅 Event Management

* Admin can create events
* Users can register for events
* Displays attendee count
* Organized event listings

---

### 📢 Announcements

* Admin can post announcements
* Users can view recent updates in dashboard

---

## 🛠️ Tech Stack

| Layer       | Technology Used         |
| ----------- | ----------------------- |
| Frontend    | HTML, CSS, Bootstrap    |
| Backend     | Flask (Python)          |
| Database    | SQLite (SQLAlchemy ORM) |
| Auth System | Flask-Login             |

---

## 📂 Project Structure

```
Alumni-Management-System/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── alumni_routes.py
│   │   ├── mentorship_routes.py
│   │   ├── events_routes.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── mentorship.html
│   │   ├── events.html
│   │   └── ...
│   │
│   ├── static/
│       ├── css/
│       ├── js/
│
├── instance/
│   └── site.db
│
├── run.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/alumni-management.git
cd alumni-management
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Environment

```bash
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Application

```bash
flask run
```

---

## 🔐 Authentication

* Secure login & registration
* Role-based access control
* Session management using Flask-Login

---

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Mentorship System
![Mentorship](screenshots/mentorship.png)

### Events Page
![Events](screenshots/events.png)

---

## 🚀 Future Enhancements

* 💬 Real-time chat system
* 🔔 Notification system
* 📊 Advanced analytics dashboard (charts)
* 🌙 Dark mode
* 📱 Fully responsive mobile UI

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 📜 License

This project is developed for educational and academic purposes.

---

## 👨‍💻 Author

**Satyam Sharma**
B.Tech CSE — SRM AP

---

## ⭐ Support

If you found this project helpful, consider giving it a **star ⭐** on GitHub!

---
