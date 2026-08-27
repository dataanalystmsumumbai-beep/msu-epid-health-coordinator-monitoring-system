# MSU/EPID Health Coordinator Monitoring System

## Enterprise Edition v3.0

Developed for:

**Metropolitan Surveillance Unit (MSU)**  
**Epidemiology Cell (EPID), Mumbai**

### Status

**Production Ready / Final Submission Version**

---

## Overview

The **MSU/EPID Health Coordinator Monitoring System** is a web-based monitoring application developed using **Python and Streamlit**.

The system provides a centralized platform for managing coordinators, tasks, daily reviews, notifications, reports, users, and system information through role-based access.

The application supports **Developer, Admin, and Coordinator** users with appropriate access to system functions.

---

## Key Features

- 🔐 User authentication
- 👥 Role-based access control
- 🛠️ Developer Dashboard
- 👨‍💼 Admin Dashboard
- 👨‍⚕️ Coordinator Dashboard
- 📋 Task Management
- 📌 Task Assignment
- 📝 Daily Review Management
- 🔔 Notifications
- 📊 Reports Dashboard
- 👤 User Management
- ⚙️ System Settings
- 📖 System Manual
- ❓ Help Center
- 📡 System Status
- 📝 Audit and login history support
- 🚪 Secure logout

---

## User Roles

### Developer

Provides access to developer-level system functions and monitoring.

### Admin

Provides administrative access for managing users, coordinators, tasks, reviews, reports, and other configured system functions.

### Coordinator

Provides access to assigned tasks, daily reviews, notifications, and coordinator-specific monitoring functions.

---

## Technology Stack

- **Python**
- **Streamlit**
- **Pandas**
- **OpenPyXL**
- **Plotly**
- **Google Sheets / Google APIs**
- **Google Service Account Authentication**

---

## Data Source

The application is configured to use Google Sheets as its primary data source.

Configured worksheets include:

- `01_User_Master`
- `02_Coordinator_Master`
- `03_Task_Master`
- `04_Coordinator_Task_Map`
- `05_Daily_Review`
- `06_Login_History`
- `07_Audit_Log`
- `08_System_Settings`
- `09_App_Manual`
- `10_Notifications`

---

## Security

The application implements:

- Role-based page access
- Password verification
- Session-based authentication
- Role normalization
- Logout/session clearing
- Login history
- Audit logging support
- Configurable session and login settings

---

## Application Structure

```text
MSU-EPID Health Coordinator Monitoring System
│
├── app.py
├── config/
├── core/
├── services/
├── utils/
├── pages/
├── requirements.txt
└── README.md
