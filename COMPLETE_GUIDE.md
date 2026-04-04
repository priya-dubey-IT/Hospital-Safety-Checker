# 🏥 Hospital Safety Checker - Complete Project Guide

Welcome to the **Hospital Safety Checker**, a modern, full-stack medical management system designed to streamline patient registration, doctor verification, and clinical workflow management.

---

## 🌟 Project Overview

The **Hospital Safety Checker** is a professional-grade application built to help medical facilities manage their daily operations. It provides a secure and intuitive interface for doctors and staff to track patient assignments, manage consultations, and access real-time data analysis.

### What is this project?

At its core, it's a **Patient Relationship Management (PRM) system** specifically tailored for hospitals. It handles the lifecycle of a patient's visit: from registration with a doctor to the completion of their medical report.

### How does it work?

1. **Registration**: New doctors and patients are registered through a unified interface.
2. **Assignment**: Patients are automatically assigned to their respective doctors upon registration.
3. **Verification**: Doctors verify their identity (simplified name-based login) to access their specific dashboard.
4. **Workflow**: Doctors view their "Waiting List" of patients, conduct consultations, and mark them as "Completed".
5. **Reporting**: Data is aggregated into an Admin Panel where administrators can view stats and export reports as Excel files.
6. **AI Assistance**: A built-in chatbot helps users navigate the system and answers common queries.

---

## 🏗️ Technical Architecture

The project uses a modern **decoupled architecture**:

| Layer | Technology | Documentation |
| :--- | :--- | :--- |
| **Frontend** | React (Vite) | [frontend/README.md](file:///c:/Users/Rohit/OneDrive/Desktop/safety%20checker/frontend/README.md) |
| **Backend** | FastAPI (Python) | [backend/README.md](file:///c:/Users/Rohit/OneDrive/Desktop/safety%20checker/backend/README.md) |
| **Database** | SQLite | `hospital_safety.db` |
| **UI/UX** | Vanilla CSS + Icons | `index.css` & `App.css` |

### 🛠️ Key Components

- **FastAPI Backend**: A high-performance Python API that handles data logic, database interactions, and report generation.
- **React Frontend**: A dynamic SPA (Single Page Application) that provides a smooth, responsive user experience with modern aesthetics.
- **SQLite Storage**: A robust, file-based database that ensures data persistence without the need for complex server setup.
- **Excel Integration**: Built-in functionality to export clinical data for external analysis and record-keeping.

---

## 🚀 Getting Started

### 🏁 Quick Run

The easiest way to start both the frontend and backend is using the provided script:

1. Open PowerShell in the project root.
2. Run: `.\start.ps1`

### 🔧 Manual Setup

#### 1. Backend Setup

1. Navigate to `backend/`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the server: `python main.py` (Runs on port 8000)

#### 2. Frontend Setup

1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev` (Runs on port 3000 or 5173)

---

## 📖 Feature Walkthrough

### 1️⃣ Registration & Onboarding

The system allows registering a doctor and their first patient simultaneously.

- **Path**: `Registration` tab.
- **Inputs**: Doctor Name, Specialization (Category), and Patient Name.
- **Result**: Creates both records and a pending assignment.

### 2️⃣ Doctor Dashboard

Each doctor has a personalized view of their current tasks.

- **Path**: `Doctor Dashboard` (Log in with name).
- **Features**:
  - **Waiting List**: Overview of patients currently waiting for a consultation.
  - **Completed List**: History of patients already seen.
  - **One-Click Completion**: Move patients from waiting to completed after the visit.

### 3️⃣ Admin Control Panel

A centralized hub for hospital administrators.

- **Access**: `Admin` tab.
- **Capabilities**:
  - View all registered Doctors and Patients.
  - Monitor all Assignments and their statuses.
  - Real-time search and filtering.
  - **Export to Excel**: Download the entire database as a professional spreadsheet.

### 4️⃣ AI Chatbot Assistant

Need help? The AI assistant is ready to guide you.

- **Path**: `Chatbot` tab.
- **Purpose**: Answers questions about how many patients are in the system, how to register, or details about specific doctors.

---

## 📂 Project Structure

```text
safety checker/
├── backend/                # FASTAPI Backend
│   ├── app/                # Application logic
│   │   ├── routes/         # API Endpoints (Admin, Dashboard, etc.)
│   │   ├── services/       # Business logic layer
│   │   └── models/         # Pydantic schemas
│   ├── reports/            # Generated Excel files
│   └── main.py             # Entry point
├── frontend/               # REACT (Vite) Frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Layout views (Admin, Registration, etc.)
│   │   └── services/       # API integration
│   └── App.jsx             # Main router
└── hospital_safety.db      # Main SQLite Database
```

---

## 🛡️ Future Enhancements

- [ ] Addition of User Authentication (Username/Password).
- [ ] Real-time notifications for doctors when a new patient is assigned.
- [ ] Mobile application integration.
- [ ] Advanced medical report generation with PDF export.

---

> [!NOTE]
> This project has been simplified to prioritize ease of use and rapid deployment, removing complex biometric requirements in favor of a robust name-based management system.

**Built with ❤️ for Medical Professionals**
