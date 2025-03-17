# 📝 Attendance Management System

A **Django-based** Attendance Management System where employees can check in, check out, update their profiles, and request leave.

---

## 🚀 Features
- Employee Profile Management  
- Daily Check-in & Check-out  
- Leave Request System  
- Admin Panel for Managing Attendance  
- Secure Authentication System  

---

## 🛠️ Installation Guide

### Create a Virtual Environment

- python -m venv venv  # For Windows
- source venv/bin/activate  # For macOS/Linux
- venv\Scripts\activate  # For Windows (PowerShell)

### Install Dependencies

- pip install -r requirements.txt

### Apply Migrations

- python manage.py makemigrations auth
- python manage.py migrate

### Create Superuser (Admin Access)

- python manage.py createsuperuser

### Run the Development Server

- python manage.py runserver
