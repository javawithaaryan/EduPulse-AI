import os
import json
from openai import AzureOpenAI
from config import Config

class OpenAIService:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            if Config.USE_MOCK_AI:
                return None
            cls._client = AzureOpenAI(
                azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
                api_key=Config.AZURE_OPENAI_KEY,
                api_version="2024-02-15-preview"
            )
        return cls._client

    @classmethod
    def ask_ai(cls, question, context="General learning"):
        """Doubt Resolution System - Phase 2"""
        if Config.USE_MOCK_AI:
            return f"Mock AI Response: '{question}'. Focus on core subject principles. [Placeholder for real Azure AI]"

        client = cls.get_client()
        prompt = f"""
        Role: Helpful AI Tutor
        Objective: Answer the student's question clearly and calmly.
        Context: {context}
        Question: {question}
        Format: Markdown.
        """
        response = client.chat.completions.create(
            model=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    @staticmethod
    def grade_submission(submission_text, subject, grade_level, rubric, max_marks):
        """Core Grading Enhancement - Phase 2"""
        if Config.USE_MOCK_AI:
            return {
                "score": 8.5,
                "feedback": "Great effort! Your explanation of the core concepts is clear, but you could add more detail in the second paragraph.",
                "strengths": ["Clear structure", "Good terminology"],
                "improvements": ["Add specific examples", "Check calculation on page 2"],
                "practice_tip": "Review the impact of temperature changes on the water cycle."
            }

        client = OpenAIService.get_client()
        prompt = f"""
        Role: Expert Educator
        Subject: {subject}
        Grade: {grade_level}
        Rubric: {rubric}
        Max Marks: {max_marks}
        Submission: {submission_text}
        Output: JSON with 'score', 'feedback', 'strengths' (list), 'improvements' (list), 'practice_tip'.
        """
        response = client.chat.completions.create(
            model=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    def generate_class_insights(performance_summary):
        """Teacher Insight Summary - Phase 2"""
        if Config.USE_MOCK_AI:
            return {
                "headline": "Class Strength: Algebraic Thinking",
                "summary": "Most students are excelling at linear equations, but 3 students have high risk levels in quadratic logic.",
                "action_item": "Dedicate 15 mins to a recap on the Quadratic Formula tomorrow."
            }

        client = OpenAIService.get_client()
        prompt = f"""
        Role: Senior Academic Advisor
        Objective: Analyze class data and provide a supportive, 'Calm' insight for the teacher.
        Data: {performance_summary}
        Output: JSON with 'headline', 'summary' (1-2 sentences), 'action_item' (short instruction).
        """
        response = client.chat.completions.create(
            model=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    @staticmethod
    def generate_parent_report(student_name, records_json):
        """Parent Academic Summary - Phase 2"""
        if Config.USE_MOCK_AI:
            return f"Hello! {student_name} is doing exceptionally well in Science. We suggest focusing on advanced calculus this weekend to stay ahead. Overall health: CALM."

        client = OpenAIService.get_client()
        prompt = f"""
        Role: Supportive School Counselor
        Objective: Provide a 'Calm' and clear summary for a parent.
        Student: {student_name}
        Data: {records_json}
        Tone: Encouraging, professional, non-alarmist.
        Output: Plain text summary (2-3 sentences).
        """
        response = client.chat.completions.create(
            model=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
