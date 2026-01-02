import os
import json
import logging
from openai import AzureOpenAI, APIError
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIService:
    _client = None

    @classmethod
    def get_client(cls):
        try:
            if cls._client is None:
                if Config.USE_MOCK_AI:
                    logger.info("Using Mock AI Service")
                    return None
                
                if not Config.AZURE_OPENAI_KEY or not Config.AZURE_OPENAI_ENDPOINT:
                    logger.error("Azure OpenAI credentials missing")
                    return None

                cls._client = AzureOpenAI(
                    azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
                    api_key=Config.AZURE_OPENAI_KEY,
                    api_version=Config.AZURE_OPENAI_API_VERSION
                )
            return cls._client
        except Exception as e:
            logger.error(f"Failed to initialize AzureOpenAI client: {str(e)}")
            return None

    @classmethod
    def ask_ai(cls, history, context="General learning"):
        """Doubt Resolution System - Chat Mode (Phase 3)"""
        if Config.USE_MOCK_AI:
            return f"Mock AI Response to: '{history[-1]['content']}'. Focus on core subject principles. [Placeholder for real Azure AI]"

        client = cls.get_client()
        if not client:
            return "Error: AI Service unavailable."

        try:
            # Master System Prompt
            system_prompt = f"""
            You are an intelligent, friendly, and conversational AI assistant designed to behave exactly like ChatGPT.

            Your goals:
            - Maintain conversation context across multiple messages.
            - Respond in a natural, human-like, friendly tone.
            - Explain concepts simply and clearly.
            - Avoid robotic or textbook-style responses.
            - Use clean formatting that looks good in a chat UI.
            - Do NOT expose markdown symbols like ###, **, or raw formatting unless rendered by the UI.
            - Adapt explanations based on user understanding level.

            Behavior rules:
            - Always remember previous user messages in the conversation.
            - Never reset context unless explicitly asked.
            - If a user asks a follow-up question, continue from the previous explanation.
            - Keep responses visually clean and readable.
            - Use bullet points and spacing naturally (not markdown-heavy).
            - If the user is confused, simplify further.
            - If the user asks for technical depth, go deeper.
            
            Format: Markdown (formatted for clean UI display).
            Context: {context}
            """
            
            # Construct full message list
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(history)

            response = client.chat.completions.create(
                model=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in ask_ai: {str(e)}", exc_info=True)
            return f"Error: {str(e)} - Please check logs or try again."

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
        if not client:
            return {"error": "AI Service unavailable"}

        try:
            prompt = f"""
            Role: Expert Educator
            Subject: {subject}
            Grade: {grade_level}
            Rubric: {rubric}
            Max Marks: {max_marks}
            Submission: {submission_text}
            Output: JSON with 'score' (number), 'feedback' (string), 'strengths' (list of strings), 'improvements' (list of strings), 'practice_tip' (string).
            """
            response = client.chat.completions.create(
                model=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error in grade_submission: {str(e)}")
            return {"error": str(e), "score": 0, "feedback": "System error during grading."}

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
        if not client:
            return {"error": "AI Service unavailable"}

        try:
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
        except Exception as e:
            logger.error(f"Error in generate_class_insights: {str(e)}")
            return {"headline": "Error", "summary": "Unable to generate insights.", "action_item": "Check system logs."}

    @staticmethod
    def generate_parent_report(student_name, records_json):
        """Parent Academic Summary - Phase 2"""
        if Config.USE_MOCK_AI:
            return f"Hello! {student_name} is doing exceptionally well in Science. We suggest focusing on advanced calculus this weekend to stay ahead. Overall health: CALM."

        client = OpenAIService.get_client()
        if not client:
            return "Error: AI Service unavailable."

        try:
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
        except Exception as e:
            logger.error(f"Error in generate_parent_report: {str(e)}")
            return "Unable to generate report at this time."