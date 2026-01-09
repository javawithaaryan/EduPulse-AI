from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .assignment import Assignment
from .submission import Submission
from .ai_results import AIResult
from .performance import Performance
from .quiz import Quiz, Question, QuizAttempt
from .attendance import Attendance
from .library import Resource, LearningProgress, LibraryRecommendation
from .tasks import Task, Goal
from .wellbeing import EmotionalCheckin, SupportLog
from .chat import ChatSession, ChatMessage
from .fees import Fee, PaymentTransaction
