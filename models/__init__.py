from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .assignment import Assignment
from .submission import Submission
from .ai_results import AIResult
from .performance import Performance
from .quiz import Quiz, Question, QuizAttempt
from .attendance import Attendance
