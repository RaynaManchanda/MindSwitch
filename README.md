📌 MindSwitch

Domain-Switchable Cognitive Training Chrome Extension with Persistent Behavioral Analytics
MindSwitch is a full-stack Chrome Extension + Flask backend system designed to provide structured cognitive guidance instead of direct solutions.
Unlike traditional AI sidebars that give answers, MindSwitch follows a mentor-style escalation approach to improve problem-solving skills while tracking behavioral dependency metrics.

🚀 Features
🧠 Domain-Switchable Modes

DSA Mode – Structured algorithmic guidance
Interview Mode – STAR-based response framework
Study Mode – Concept extraction and reinforcement

📈 Structured Hint Escalation

Each guidance request provides 3 controlled levels:

Level 1 – Concept direction
Level 2 – Pattern insight
Level 3 – Structured approach

No direct solutions are provided.

🗄 Persistent Analytics (MySQL)

Session-based tracking
Unlock logging
Mode usage tracking
Level 2 vs Level 3 usage distribution
Level 3 dependency percentage calculation

🔍 Context-Aware Content Extraction

Dynamically injects content script (Manifest V3 compliant)
Extracts page content safely
Applies rule-based pattern detection (e.g., Binary Search, Graph, DP)

📊 Behavioral Metrics

The system computes:
Total unlocks
Mode distribution
Level usage frequency
Level 3 dependency percentage
This enables quantifying over-reliance on deeper hints.

🏗 Architecture
Chrome Extension (Manifest V3)
        ↓
Flask REST API
        ↓
MySQL Database
        ↓
Analytics Engine

🛠 Tech Stack
Frontend: JavaScript (Chrome Extension - MV3)
Backend: Flask (Python)
Database: MySQL
Architecture: REST API-based modular design

📂 Project Structure
MindSwitch/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── styles.css
│   ├── content.js
│
└── README.md

⚙️ Setup Instructions
1️⃣ Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py


Backend runs on:
http://127.0.0.1:5000

2️⃣ Database Setup
CREATE DATABASE mindswitch;
USE mindswitch;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    mode VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE unlock_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    mode VARCHAR(50),
    level_unlocked INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

3️⃣ Chrome Extension Setup

Open chrome://extensions/
Enable Developer Mode
Click Load Unpacked
Select the extension/ folder

🔮 Future Enhancements

AI-powered hint engine with strict solution guardrails
Adaptive weakness scoring
Personalized learning recommendations
Interactive analytics dashboard
User authentication system

🎯 Project Objective

MindSwitch aims to:
Encourage structured thinking
Prevent passive solution dependency
Quantify learning behavior
Provide domain-specific cognitive assistance

📌 Version
v1.0 – Rule-Based Cognitive Engine with Persistent Analytics

Future versions will include AI-powered guarded hint generation.
