# MSU/EPID Health Coordinator Monitoring System

## Enterprise Edition v3.0

A Streamlit-based monitoring system developed for the Metropolitan Surveillance Unit (MSU), Epidemiology Cell (EPID), Mumbai.

## Purpose

The system provides a centralized application for user authentication, role-based access, coordinator/task management, daily review monitoring, notifications, reports, system information, and support documentation.

## Technology Stack

- Python
- Streamlit 1.46.1
- Google Sheets / Google APIs
- Pandas
- OpenPyXL
- Plotly
- Google Service Account authentication through Streamlit Secrets

## User Roles

### Developer
System-level access and developer dashboard functions.

### Admin
Administrative dashboard, user/task management, reviews, notifications, reports and system functions according to configured permissions.

### Coordinator
Coordinator dashboard, assigned task monitoring and daily review functions according to configured permissions.

## Main Application Pages

1. Developer Dashboard
2. Admin Dashboard
3. Coordinator Dashboard
4. Daily Review
5. Task Management
6. User Management
7. Help Center
8. System Settings
9. System Manual
10. Notifications
11. Reports Dashboard
12. System Status
13. About
14. Contact Support

## Data Structure

The application is configured to use the following Google Sheet worksheets:

- 01_User_Master
- 02_Coordinator_Master
- 03_Task_Master
- 04_Coordinator_Task_Map
- 05_Daily_Review
- 06_Login_History
- 07_Audit_Log
- 08_System_Settings
- 09_App_Manual
- 10_Notifications

## Security

- Role-based page access
- Password verification
- Session-based authentication
- Session logout
- Role normalization for Developer, Admin and Coordinator
- Audit logging support
- Configurable login-attempt and session-timeout settings

## Deployment

The application is designed for deployment through Streamlit with Google credentials supplied through Streamlit Secrets.

Required secret:

`gcp_service_account`

The Google service account must have appropriate access to the configured Google Sheet.

## Local Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

## Version

Application version: 3.0.0

Environment: Production

Owner: MSU / EPID

## Current Status

Core authentication, role-based access, dashboards, task assignment, daily review, notifications, and logout functionality have been tested in the final working application.
