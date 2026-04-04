# Hospital Safety Checker - Project Summary

## 📊 Project Overview

**Name**: Hospital Safety Checker  
**Type**: Full-Stack Medical Workflow Management Application  
**Purpose**: Efficient patient tracking and doctor-patient relationship management  
**Status**: Simplified & Production-Ready  
**Updated**: 2026-02-27

---

## 🏗️ Technical Architecture

### Technology Stack

**Frontend**:

- **React.js 18.3**: Modern functional components with Hooks.
- **Vite**: Ultra-fast build tool and development server.
- **React Router DOM**: Client-side routing for seamless navigation.
- **Vanilla CSS**: Premium design with glassmorphism, gradients, and custom animations.
- **React Icons**: Comprehensive medical and UI iconography.

**Backend**:

- **Python 3.8+**: Core programming language.
- **FastAPI**: High-performance, asynchronous REST API framework.
- **Uvicorn**: Lightning-fast ASGI server.
- **SQLite (aiosqlite)**: Robust, asynchronous, file-based relational database.
- **Pandas & Openpyxl**: Advanced data processing for Excel report generation.

---

## 📁 Core Directory Structure

```text
safety checker/
├── backend/                # FASTAPI Backend
│   ├── app/                # Application logic
│   │   ├── routes/         # Endpoints: registration, patient, dashboard, admin, chatbot, reports
│   │   ├── services/       # Services: report generation, excel export, AI integration
│   │   ├── models/         # Pydantic schemas for data validation
│   │   └── database_sqlite.py # SQLite database engine and queries
│   ├── main.py             # Entry point (Port 8000)
│   └── .env                # Server and API configuration
├── frontend/               # REACT (Vite) Frontend
│   ├── src/
│   │   ├── components/     # Reusable UI elements (Webcam, Navbar, Timers)
│   │   ├── pages/          # Full-page views (Dashboard, Admin, Registration)
│   │   ├── services/       # API abstraction layer
│   │   └── index.css       # Global design system
│   └── App.jsx             # Main Router and Page Layout
└── hospital_safety.db      # Local SQLite database file
```

---

## 🎯 Key Features & Modules

### 1. Unified Registration

- Register both a doctor (name and category) and their first patient in one step.
- Automatic creation of a "waiting" assignment linking the two.

### 2. Personalized Doctor Dashboard

- Specialized view for doctors after a name-based login.
- **Waiting List**: Track patients currently in line for consultation.
- **Completed List**: Maintain a history of previous consultations.
- **Instant Actions**: Move assignments from waiting to completed with a single click.

### 3. Comprehensive Admin Panel

- Real-time statistics on system usage (Total Doctors, Patients, Assignments).
- Full database visibility with advanced search and filtering.
- **Excel Report Engine**: Bulk export all clinical data into a professional spreadsheet for external auditing.

### 4. AI Chatbot Assistant

- Integrated AI powered by Google Gemini (flash model).
- Helps users with system navigation, registration steps, and general medical inquiries.

---

## 💾 Database Schema (SQLite)

- **doctors**: Stores ID, name, specialization, and registration date.
- **patients**: Stores ID, name, and registration metadata.
- **assignments**: Bridges doctors and patients, tracks consultation status (`waiting`/`completed`), and timestamps.
- **patient_reports**: Stores clinical notes, diagnosis, and treatment details for each consultation.

---

## 🛡️ Best Practices & Security

- **Asynchronous Execution**: All DB and API calls are async for maximum performance.
- **Environment Variables**: Sensitive configurations (API keys, ports) are decoupled from the code.
- **Input Validation**: Strict schema enforcement using Pydantic.
- **Decoupled Architecture**: Clean separation between UI and business logic.

---

**Project Status**: 🚀 Fully Updated & Documented  
**Version**: 1.1.0  
**License**: Hospital Safety Standard  
