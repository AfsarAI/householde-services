# 🏠 A-Z Household Services  
### A Flask-Based Multi-User Household Services Platform

A comprehensive **web application** connecting customers with skilled professionals for various household needs — developed as part of the **Modern Application Development (MAD-1)** course at **IIT Madras**.

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Flask-red.svg" alt="Flask Framework">
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey.svg" alt="SQLite Database">
  <img src="https://img.shields.io/badge/Frontend-Bootstrap-purple.svg" alt="Bootstrap">
</p>

---

## 🎥 Project Demo Video

A full video explanation and demo of the project is available here:  
👉 **[📺 Watch the Project Demo Video](<Your YouTube Video Link>)**

---

## ✨ Key Features

This application provides a seamless experience for all user types:

- **👤 Multi-User Authentication System**  
  Separate registration and login portals for **Customers**, **Professionals**, and **Admin**, with secure session management.

- **🛠️ Service Management**  
  Customers can browse and book services and track their status from request to completion.

- **📂 File Upload Support**  
  Professionals can upload resumes and certifications to showcase their qualifications.

- **📱 Responsive & Modern UI**  
  Built with **Bootstrap** for a fully responsive, mobile-friendly design. The UI is enhanced with gradient backgrounds and subtle animations for a better user experience.

- **⚙️ Dynamic & Robust Backend**  
  Developed using **Flask** and **SQLAlchemy** to handle all business logic and database operations.

---

## 💻 Tech Stack & Architecture

| Layer | Technology Used |
|-------|----------------|
| **Backend** | Python, Flask, SQLAlchemy |
| **Frontend** | HTML, CSS, JavaScript, Jinja2, Bootstrap |
| **Database** | SQLite |
| **Architecture** | MVC-style structure with `controllers`, `models`, `templates`, and `static` assets; main app entry via `app.py` |

---

## 🗂️ Database Design

The database is designed to minimize redundancy and maintain data integrity. Core tables include:

| Table | Purpose |
|-------|---------|
| **Admin** | Stores admin credentials and information |
| **Users** | Stores customer details and credentials |
| **Professionals** | Stores professional details, experience, and uploaded documents |
| **Services** | Contains available services, descriptions, and pricing |
| **Service Requests** | Tracks bookings and relationships between customers, professionals, and services |

*An ER diagram is included in the project report for a visual representation of table relationships.*

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1️⃣ Prerequisites
- Python 3.10+
- pip

### 2️⃣ Clone the Repository
```bash
git clone <your-repository-link>
cd household-services-application
```

### 3. Create and Activate a Virtual Environment
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
### 5. Run the Application
```bash
python app.py
```
---

### 6. Admin Access
Use the default admin credentials for testing and initial setup.
| Field    | Value               |
|----------|---------------------|
| Email    | Admin@xyz.com       |
| Password | Admin@123           |

---

## 💬 Future Enhancements

- Integration with more services and sub-categories
- Email or SMS notifications for service updates
- Option for customer reviews and ratings
- Migrate to a more scalable database like PostgreSQL or MySQL

---

## 🏆 Credits

| Role | Name |
|------|------|
| **Developer** | Mohd Afsar |
| **Institution** | IIT Madras |
| **Course** | Modern Application Development – 1 |

---

## 🧾 Acknowledgement

This project is an academic submission created to apply the theoretical concepts learned in the **MAD-1** course.

⭐ Developed with ❤️ by [Mohd Afsar]
