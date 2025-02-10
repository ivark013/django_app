Surveillance Camera System with AI-Powered Threat Detection
This project is an AI-powered Surveillance Camera System designed to detect and identify threats in real-time. The system integrates advanced AI models to detect weapons, masked thieves, and other suspicious activities. It features a backend built with Django, a database system for storage, and multiple notification channels for alerting users.

Features:
Real-Time Threat Detection: AI models detect potential threats such as weapons or thieves wearing masks in live camera feeds.
Customizable Alerts: Users receive notifications based on their preferred settings (Email, Telegram, WhatsApp).
Dashboard: An intuitive dashboard for admins to monitor live feeds, view detected threats, and manage camera settings.
Camera Control: Ability to activate/deactivate cameras remotely via the system.
Database Storage: All alerts and camera feed information are stored securely in a PostgreSQL (or SQLite) database for future reference.
User Authentication: Admin login and secure access to the system's features.
Technologies Used:
Django: Web framework for backend and API handling.
PostgreSQL (or SQLite): Database management for storing camera and alert data.
AI Models: Custom-trained models for detecting threats like weapons and masked thieves.
SMTP, Telegram API, WhatsApp API: For sending real-time notifications.
WebSockets: For live video streaming from cameras.
How It Works:
Detection: The system processes real-time video feeds from cameras using AI models to detect anomalies.
Alert Creation: When a threat is detected, an alert is generated and stored in the database.
Notification: Alerts are sent to users via their preferred notification method.
Dashboard: Admins can view the alerts and manage cameras through the dashboard.
