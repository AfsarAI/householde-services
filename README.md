# 🏠 A-Z Household Services - A Flask Web Application

**A comprehensive multi-user platform connecting customers with skilled professionals for various household needs. This project was developed as part of the Modern Application Development (MAD-1) course.**

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Flask-red.svg" alt="Flask Framework">
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey.svg" alt="SQLite Database">
  <img src="https://img.shields.io/badge/Frontend-Bootstrap-purple.svg" alt="Bootstrap">
</p>

## 🎥 Project Demo Video

A full video explanation and demo of the project is available here:

**[📺 Watch the Project Explanation Video Here]** *(<- Paste your YouTube video link here)*

---

## ✨ Key Features

This application is packed with features designed to provide a seamless experience for all user types:

* [cite_start]**👤 Multi-User Authentication System:** Separate registration and login portals for **Customers**, **Professionals**, and an **Admin** with secure session management[cite: 5, 153].
* [cite_start]**🛠️ Service Management:** Enables customers to browse and book services, and track their status from request to completion[cite: 4, 5, 154].
* [cite_start]**📂 File Upload Support:** Professionals can upload their resumes and certifications to showcase their qualifications[cite: 26, 157].
* [cite_start]**📱 Responsive & Modern UI:** Built with **Bootstrap** for a fully responsive, mobile-friendly design[cite: 8, 16, 155]. [cite_start]The UI is enhanced with gradient backgrounds and star animations for a better user experience[cite: 15, 17, 156].
* [cite_start]**⚙️ Dynamic & Robust Backend:** Built with the **Flask** framework and **SQLAlchemy** to handle all business logic and database management[cite: 8, 13, 16].

---

## 💻 Tech Stack & Architecture

The application follows a standard web architecture using the following technologies:

* [cite_start]**Backend:** Python, Flask, SQLAlchemy [cite: 8, 13]
* [cite_start]**Database:** SQLite [cite: 8, 14]
* [cite_start]**Frontend:** HTML, CSS, JavaScript, Jinja2, Bootstrap [cite: 8, 13, 15]
* [cite_start]**Architecture:** The code is organized into folders for backend logic (`controllers`, `models`), static assets (`css`, `js`, `images`), and UI templates, with a central `app.py` file to run the application[cite: 143, 144, 146, 147, 148]. [cite_start]The SQLite database is stored in the `instance` folder[cite: 150].

---

## 🗂️ Database Design

[cite_start]The database schema is normalized to minimize redundancy and ensure data integrity[cite: 32]. It consists of the following core tables:

* [cite_start]**Admin Table:** Stores admin credentials and information[cite: 20, 21].
* [cite_start]**Users Table:** Stores customer details and credentials[cite: 22, 23].
* [cite_start]**Professionals Table:** Stores service professional details, including experience and resume filenames[cite: 24, 25, 26].
* [cite_start]**Services Table:** Contains all available services, their descriptions, and base prices[cite: 27, 28].
* [cite_start]**Service Requests Table:** Manages the relationships between customers, professionals, and the services they book[cite: 29, 30].

*An ER Diagram is available in the project report for a visual representation of table relationships.*

---

## 🚀 Getting Started (Installation & Setup)

To get this application running on your local machine, follow these steps:

### 1. Prerequisites
Ensure you have **Python** and **pip** installed on your system.

### 2. Clone the Repository
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

### 6. Admin Access
Use the default admin credentials for testing and initial setup.

## 📜 Acknowledgement
This project is an academic submission created to apply the theoretical concepts learned in the Modern Application Development (MAD-1) course.

⭐ *Developed by [Mohd Afsar]*  
