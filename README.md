# EduPulse AI 🎓🚀

**Smarter Learning. Calmer Classrooms.**

EduPulse is a next-generation education platform that seamlessly integrates advanced AI to personalize learning for students, automate grading for teachers, and provide real-time peace of mind for parents.

Built with **React (Frontend)**, **Flask (Backend)**, and powered by **Microsoft Azure AI**.

---

## 🌟 Key Features

### 1. 🧠 AI-Powered Student Dashboard
*   **Personal AI Tutor (Azure OpenAI)**: Students can chat with an AI tutor that understands their context, helps with homework, and explains complex topics in simple terms.
*   **Adaptive Learning Paths**: Content adjusts real-time based on student performance.
*   **Interactive Quizzes**: Instant feedback and score tracking.

### 2. 📝 AI Grading for Teachers (Azure Vision)
*   **One-Click Grading**: Upload photos of handwritten assignments or standard test sheets.
*   **AI Vision Analysis**: Uses Azure AI Vision to scan and digitize content.
*   **Automated Feedback**: Generates detailed, constructive feedback for each student instantly.
*   **Class Analytics**: "Heatmaps" of student performance to identify struggling students early.

### 3. 👨‍👩‍👧‍👧 Connected Parent Dashboard (Azure ML)
*   **Real-Time Risk Prediction**: Uses Azure Machine Learning to analyze grades and attendance, predicting "At-Risk" status before it becomes a problem.
*   **Multi-Child Support**: Seamlessly switch between children (e.g., Bhoomi, Sneha) to view individual progress.
*   **Actionable Insights**: Plain-English summaries of how a child is doing, avoiding confusing jargon.

---

## 🛠️ Technology Stack

*   **Frontend**: React, TypeScript, Tailwind CSS, Framer Motion (for smooth, premium animations).
*   **Backend**: Python Flask, SQLAlchemy (SQLite/PostgreSQL).
*   **AI Services**:
    *   **Azure OpenAI Service**: GPT-4 for Chat and Reasoning.
    *   **Azure AI Vision**: OCR and Image Analysis.
    *   **Azure Machine Learning**: Predictive Analytics.

---

## 🚀 Quick Start (Deployment)

We've made it incredibly easy to run EduPulse locally.

1.  **Prerequisites**:
    *   Node.js & npm installed.
    *   Python 3.10+ installed.
    *   Azure API Keys configured in `backend/.env`.

2.  **One-Click Launch (Windows)**:
    *   Simply double-click the **`start_edupulse.bat`** script in the root directory.
    *   It will set up the environment, start the backend, and open your browser to `http://localhost:5000`.

3.  **Manual Start**:
    *   **Frontend**:
        ```bash
        cd Frontend
        npm install
        npm run build
        ```
    *   **Backend**:
        ```bash
        cd backend
        pip install -r requirements.txt
        python app.py
        ```

---

## 📂 Project Structure

*   **/Frontend**: The React application source code.
    *   `src/components`: UI Components (Dashboards, Chat Widget, etc.).
    *   `src/api.js`: API connectors to the Flask backend.
*   **/backend**: The Flask API server.
    *   `app.py`: Main entry point.
    *   `blueprints/`: Modular route handlers for Student, Teacher, Parent.
    *   `services/`: Python wrappers for Azure AI services.
*   **start_edupulse.bat**: Deployment script.

---

## 🛡️ Security & Privacy
*   **Role-Based Access**: Strict separation between Student, Teacher, and Parent data.
*   **Secure API Proxy**: All AI calls are routed through the Flask backend; API keys are never exposed to the frontend.

---

*Verified and Tested on Windows 11 environment with Python 3.11 and Node v18.*
