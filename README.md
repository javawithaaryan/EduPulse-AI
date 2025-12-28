# EduPulse AI

**Revolutionizing Education with Azure AI** - Microsoft Imagine Cup 2026

EduPulse AI is an intelligent educational platform that reduces teacher grading time by 85% using Microsoft Azure AI services, while providing personalized learning experiences for students.

## 🚀 Features

### For Teachers
- **AI-Powered Grading**: Instant assignment evaluation using Azure OpenAI GPT-4
- **Smart Attendance System**: QR code-based classroom check-ins
- **Live Quiz Builder**: Create interactive assessments with real-time feedback
- **Risk Analytics**: ML-powered student performance predictions
- **OCR Integration**: Handwritten assignment extraction via Azure Vision

### For Students
- **Instant AI Feedback**: Detailed performance reports with improvement suggestions
- **Interactive Quizzes**: Engaging assessments with immediate results
- **QR Attendance**: Quick classroom check-ins via mobile scanning
- **Progress Tracking**: Visual dashboards showing academic growth

### For Parents
- **Real-time Monitoring**: Link children and view comprehensive academic profiles
- **AI Insights**: Personalized performance summaries and risk indicators
- **Attendance Tracking**: Live attendance health monitoring

### For Admins
- **System Intelligence**: Dynamic analytics dashboard with live metrics
- **User Management**: Comprehensive role-based access control
- **Performance Metrics**: Track AI accuracy, time saved, and system health

## 🛠️ Tech Stack

**Backend**: Python, Flask, SQLAlchemy  
**Frontend**: HTML, CSS (Custom Design System), JavaScript  
**Database**: Azure SQL Database  
**Cloud Services**: Azure App Service, Azure Blob Storage  
**AI Services**:
- Azure OpenAI (GPT-4 for grading & insights)
- Azure ML (Risk prediction models)
- Azure Vision (OCR for handwritten content)
- Azure Communication Services (Notifications)

## 📦 Installation

### Prerequisites
- Python 3.10+
- Azure Account with active AI services
- Git

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/javawithaaryan/EduPulse-AI.git
cd EduPulse-AI
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file:
```env
SECRET_KEY=your-secret-key-here
AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
AZURE_OPENAI_KEY=your-azure-openai-key
AZURE_OPENAI_DEPLOYMENT=gpt-4
DATABASE_URL=your-database-connection-string
```

5. **Initialize database**
```bash
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

6. **Run the application**
```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## 🔐 Demo Accounts

**Teacher**: `teacher1@edupulse.ai` / `password`  
**Student**: `tester@test.com` / `password`  
**Admin**: `admin1@edupulse.ai` / `password`  
**Parent**: Register and link a student via email

## 🎨 Design System

EduPulse AI features a premium "Calm & Modern" design with:
- **Color Palette**: Soft Mist Blue (#F3F6FB) with vibrant accent gradients
- **Glass Morphism**: Translucent cards with backdrop blur effects
- **Smooth Animations**: CSS transitions and micro-interactions
- **Responsive Layout**: Mobile-first design approach

## 🏗️ Project Structure

```
EduPulse-AI/
├── blueprints/          # Flask blueprints (auth, teacher, student, etc.)
├── models/              # Database models
├── services/            # Azure AI service integrations
├── static/              # CSS, JS, images
├── templates/           # HTML templates
├── app.py              # Main application entry point
└── requirements.txt    # Python dependencies
```

## 🚢 Deployment

### Azure App Service

1. **Create Azure resources** via Azure Portal
2. **Configure deployment** from GitHub
3. **Set environment variables** in App Service settings
4. **Enable continuous deployment**

Detailed deployment guide: [View Documentation](docs/DEPLOYMENT.md)

## 🤝 Contributing

This project was built for Microsoft Imagine Cup 2026. Contributions, issues, and feature requests are welcome!

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🏆 Acknowledgments

Built with ❤️ for Microsoft Imagine Cup 2026  
Powered by Microsoft Azure AI Services

---

**Live Demo**: [Coming Soon]  
**Contact**: javawithaaryan@github.com
