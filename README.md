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

## 🧠 Advanced AI Capabilities

* **Azure OpenAI Integration**: Powers the intelligent chat and personalized learning suggestions.
* **Computer Vision**: Scan and digitization of handwritten notes and assignments for analysis.
* **Sentiment Analysis**: Monitors student well-being through interaction patterns.

---

## 💻 Tech Stack

* **Backend**: Python (Flask)
* **Database**: SQLite / Azure SQL
* **Frontend**: HTML5, CSS3, JavaScript (Jinja2 Templates)
* **AI Services**: Azure OpenAI (GPT-4o), Azure AI Vision
* **Deployment**: Azure App Service

---

## 🛠️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/javawithaaryan/EduPulse-AI.git
   cd EduPulse-AI
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Create a `.env` file in the root directory and add your Azure credentials:
   ```env
   AZURE_OPENAI_KEY=your_key
   AZURE_OPENAI_ENDPOINT=your_endpoint
   SECRET_KEY=your_flask_secret
   # Add other specific database or service keys
   ```

4. **Initialize Database**
   The application will automatically create the necessary database tables on the first run.

5. **Run the Application**
   ```bash
   python app.py
   ```
   Visit `http://localhost:5000` to access the platform.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
