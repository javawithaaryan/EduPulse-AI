# EduPulse AI - Next-Gen Intelligent Education Ecosystem

EduPulse AI is a comprehensive, AI-powered educational platform designed to bridge the gap between Students, Teachers, Parents, and Administrators. It goes beyond simple management to provide intelligent tutoring, automated grading, emotional well-being support, and real-time analytics.

---

## 🚀 Key Modules & Features

### 🎓 Student Portal
* **AI Personal Tutor**: Context-aware chat assistant helping with homework and concepts.
* **Smart Library**: Access to digital resources and study materials.
* **Task Management**: Track assignments, deadlines, and project status.
* **Well-being Support**: AI-driven emotional support and mental health check-ins.

### 👩‍🏫 Teacher Dashboard
* **Classroom Management**: Organize classes, students, and schedules.
* **Automated & AI Grading**: Speed up assessments with AI assistance.
* **Performance Analytics**: Deep insights into student progress and learning gaps.
* **Attendance Tracking**: Digital attendance logs and reports.

### 👨‍👩‍👧 Parent Connect
* **Progress Tracking**: Real-time view of child's grades, attendance, and efficienty.
* **Communication**: Direct channel to teachers and school announcements.

### 🛠️ Admin Console
* **User Management**: Centralized control for Students, Teachers, and Parents.
* **System Configuration**: Manage platform settings and global announcements.

---

## 💻 Tech Stack

* **Architecture**: Unified Full-Stack Application (Single-Server Deployment)
* **Backend**: Python (Flask) - Acts as API Server & Static File Server
* **Frontend**: React + Vite (Served via Flask)
* **Database**: SQLite / Azure SQL
* **AI Services**: Azure OpenAI (GPT-4o), Azure AI Vision
* **Deployment**: Azure App Service

---

## 📂 Project Structure

```
EduPulse-AI/
├── backend/            # Flask API & Server Logic
│   ├── app.py          # Entry point
│   ├── blueprints/     # API Route Modules
│   ├── models/         # Database Models
│   └── requirements.txt
├── frontend/           # React + Vite Frontend
│   ├── src/            # UI Source Code
│   ├── build/          # Production Build Outputs
│   └── package.json
└── README.md
```

---

## 🛠️ Installation & Setup

### 1. Requirements
*   Python 3.10+
*   Node.js 18+ (for building frontend)

### 2. Setup Backend
```bash
git clone https://github.com/javawithaaryan/EduPulse-AI.git
cd EduPulse-AI/backend

# Install Python Dependencies
pip install -r requirements.txt

# Configure Environment
# Create a .env file in 'backend/' with your credentials:
# AZURE_OPENAI_KEY=your_key
# AZURE_OPENAI_ENDPOINT=your_endpoint
# SECRET_KEY=your_flask_secret
```

### 3. Build Frontend (One-time)
*Note: This generates the static files needed for production.*
```bash
cd ../frontend
npm install
npm run build
```

---

## ▶️ Running the Application

The entire system (Frontend + Backend) runs on a single server port.

1.  **Start the Server**
    ```bash
    # From the 'backend' directory
    python app.py
    ```

2.  **Access the Platform**
    Open your browser and visit:  
    👉 **http://localhost:5000**

---

## 🧪 Verification
You can verify the system health and connectivity by visiting:
*   **Health Check**: `http://localhost:5000/ping`
*   **Connection Test**: `http://localhost:5000/test`

---

## 🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request.
