import os
import json
import logging
from openai import AzureOpenAI, OpenAI, APIError
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIService:
    _client = None
    _openai_client = None

    @classmethod
    def get_openai_client(cls):
        try:
            if cls._openai_client is None:
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key or any(p in api_key.lower() for p in ["your_key_here", "your_api_key_here", "placeholder"]):
                    logger.error("Standard OpenAI API key missing or placeholder used")
                    return None
                
                cls._openai_client = OpenAI(api_key=api_key)
            return cls._openai_client
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            return None

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

    @classmethod
    def ask_ai_rag(cls, user_message: str, history: list = None, subject: str = None) -> dict:
        """
        RAG-powered doubt resolution using Azure AI Search + Azure OpenAI.
        Answers are grounded ONLY on indexed academic notes.
        
        Args:
            user_message: The student's question
            history: Previous conversation messages
            subject: Optional subject filter (e.g., "Mathematics")
        
        Returns:
            dict with 'content' and 'citations' keys
        """
        if Config.USE_MOCK_AI:
            return {
                "content": f"[Mock RAG Response] Based on your notes: '{user_message}'. This topic is covered in Chapter 5 of your syllabus.",
                "citations": [{"title": "Mock Notes", "content": "Sample citation content"}]
            }

        client = cls.get_client()
        if not client:
            return {"content": "Error: AI Service unavailable.", "citations": []}

        # Check for Azure Search configuration
        search_endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
        search_key = os.getenv('AZURE_SEARCH_KEY')
        search_index = os.getenv('AZURE_SEARCH_INDEX', 'edupulse-index')

        if not search_endpoint or not search_key:
            logger.warning("Azure Search credentials not configured, falling back to standard chat")
            return {
                "content": cls.ask_ai([{"role": "user", "content": user_message}], "Student Chat"),
                "citations": []
            }

        try:
            # 1. Manual Azure Search Query
            from azure.core.credentials import AzureKeyCredential
            from azure.search.documents import SearchClient
            
            search_client = SearchClient(search_endpoint, search_index, AzureKeyCredential(search_key))
            
            # Simple keyword search on the question
            search_results = search_client.search(search_text=user_message, top=5)
            
            retrieved_docs = []
            citations = []
            
            for doc in search_results:
                # Assuming 'content' field in index, adjust if your index schema differs
                doc_content = doc.get("content", str(doc)) 
                doc_title = doc.get("title", doc.get("sourcefile", f"Doc {doc.get('id')}"))
                
                retrieved_docs.append(f"--- Document: {doc_title} ---\n{doc_content}\n")
                citations.append({"title": doc_title, "content": doc_content[:200] + "..."})
            
            context_text = "\n".join(retrieved_docs)
            
            if not context_text:
                context_text = "No relevant documents found."

            # 2. Build system prompt with retrieved context
            subject_context = f" Focus specifically on {subject} content." if subject else ""
            system_prompt = f"""You are EduPulse AI, an intelligent academic assistant.

CRITICAL RULES:
- Answer ONLY using the provided academic notes and documents below.
- If the information is not found in the notes, clearly state: "This information is not available in your uploaded notes."
- Do NOT make up information or use external knowledge.
- Cite which document/section the answer comes from when possible.
- Explain concepts clearly and in an exam-friendly manner.{subject_context}

--- RETRIEVED ACADEMIC NOTES ---
{context_text}
--------------------------------

Format: Use clean, readable formatting suitable for a chat interface."""

            # Build messages with history
            messages = [{"role": "system", "content": system_prompt}]
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": user_message})

            # 3. Azure OpenAI Call (Standard Chat Completion)
            # Use max_completion_tokens for o1-like models
            response = client.chat.completions.create(
                model=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=messages,
                max_completion_tokens=2000
            )

            # Extract response
            content = response.choices[0].message.content

            return {
                "content": content,
                "citations": citations
            }

        except Exception as e:
            logger.error(f"Error in ask_ai_rag: {str(e)}", exc_info=True)
            return {
                "content": f"Error processing your question: {str(e)}",
                "citations": []
            }

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

    @staticmethod
    def generate_question_paper(grade, subject, chapters, difficulty, question_types, blooms_levels):
        """AI Question Paper Generator - Phase 2"""
        if Config.USE_MOCK_AI:
            return {
                "mcqs": [
                    {"text": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Ribosome", "Chloroplast"], "answer": "Mitochondria", "difficulty": "easy", "bloom": "Remember"},
                    {"text": "Which organelle is responsible for protein synthesis?", "options": ["Golgi", "Ribosome", "Lysosome", "ER"], "answer": "Ribosome", "difficulty": "medium", "bloom": "Understand"}
                ],
                "short_answer": [
                    {"text": "Explain photosynthesis in 50 words.", "marks": 3, "difficulty": "medium", "bloom": "Understand"}
                ],
                "long_answer": [
                    {"text": "Describe the process of mitosis and its importance in cell division.", "marks": 5, "difficulty": "hard", "bloom": "Apply"}
                ]
            }

        client = OpenAIService.get_client()
        if not client:
            return {"error": "AI Service unavailable"}

        try:
            prompt = f"""
            Role: Expert Question Paper Designer
            Task: Generate a balanced question paper
            
            Grade: {grade}
            Subject: {subject}
            Chapters: {', '.join(chapters) if chapters else 'All chapters'}
            Difficulty Distribution: Easy {difficulty.get('easy', 30)}%, Medium {difficulty.get('medium', 50)}%, Hard {difficulty.get('hard', 20)}%
            Question Types: {json.dumps(question_types)}
            Bloom's Taxonomy Levels: {', '.join(blooms_levels)}
            
            Output: JSON with keys 'mcqs' (array), 'short_answer' (array), 'long_answer' (array).
            Each question should have: 'text', 'difficulty', 'bloom', and appropriate fields (options/answer for MCQ, marks for others).
            """
            response = client.chat.completions.create(
                model=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error in generate_question_paper: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def analyze_assignment_feedback(assignment_text, subject):
        """AI Assignment Feedback Assistant - Phase 2"""
        if Config.USE_MOCK_AI:
            return {
                "grammar_issues": [{"line": 12, "issue": "effecting → affecting", "type": "spelling"}],
                "structure_score": 85,
                "structure_feedback": "Clear introduction with thesis statement. Conclusion could be stronger.",
                "syllabus_coverage": {"covered": ["Greenhouse effect", "Human impact"], "missing": ["Mitigation strategies", "International agreements"]},
                "similarity_risk": "low",
                "similarity_percent": 8,
                "suggested_comments": ["Excellent thesis statement!", "Add more about international climate agreements", "Good use of scientific evidence"]
            }

        client = OpenAIService.get_client()
        if not client:
            return {"error": "AI Service unavailable"}

        try:
            prompt = f"""
            Role: Expert Academic Reviewer
            Task: Analyze student assignment and provide constructive feedback suggestions
            
            Subject: {subject}
            Assignment Text: {assignment_text[:3000]}
            
            Output: JSON with:
            - grammar_issues: array of {{line, issue, type}}
            - structure_score: 0-100
            - structure_feedback: string
            - syllabus_coverage: {{covered: [], missing: []}}
            - similarity_risk: "low"/"medium"/"high"
            - similarity_percent: number
            - suggested_comments: array of feedback strings
            
            Note: This is AI-assisted feedback. Teacher will review before sending.
            """
            response = client.chat.completions.create(
                model=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error in analyze_assignment_feedback: {str(e)}")
            return {"error": str(e)}

    @classmethod
    def ask_tutor(cls, question, student_name, grade, subject, weak_topics):
        """AI Tutor for school students - Phase 4"""
        # Prefer Azure OpenAI if configured
        client = cls.get_client()
        deployment = getattr(Config, 'AZURE_OPENAI_DEPLOYMENT_NAME', os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4o-mini'))
        
        # Fallback to standard OpenAI if Azure not available
        if not client:
            client = cls.get_openai_client()
            deployment = "gpt-4o-mini" # Default for standard OpenAI

        if not client:
            # Fallback to mock if API keys are not set or invalid for easier testing
            if Config.USE_MOCK_AI or not os.getenv("AZURE_OPENAI_KEY"):
                return f"[Mock AI Tutor] Hi {student_name}, it seems the AI service is not yet configured. But to answer your question about {subject}: Let's look at this step-by-step..."
            return "Error: AI Tutor service unavailable. Please check your API keys."

        try:
            system_prompt = """You are an AI Tutor for school students.
Explain concepts step by step in simple language.
Be supportive and encouraging.
Do not give direct exam answers.
Help students understand mistakes and concepts.
Adapt explanations to the student’s grade and subject."""

            user_context = f"Student Name: {student_name}\nGrade: {grade}\nSubject: {subject}\nWeak Topics: {', '.join(weak_topics) if weak_topics else 'None'}"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{user_context}\n\nQuestion: {question}"}
            ]

            response = client.chat.completions.create(
                model=deployment,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in ask_tutor: {str(e)}", exc_info=True)
            return f"I'm having trouble right now. Let's try again."

    @staticmethod
    def analyze_uploaded_file(file_content, filename):
        """
        Analyzes uploaded assessment file content to generate insights.
        """
        client = OpenAIService.get_client()
        # Fallback to standard OpenAI if Azure not available or mock
        if not client and not Config.USE_MOCK_AI:
             client = OpenAIService.get_openai_client()

        if Config.USE_MOCK_AI or not client:
             # Realistic Mock Response
             return {
                "weak_topics": ["Quadratic Equations", "Newton's Second Law"],
                "students_needing_attention": ["Alex Johnson", "Sam Smith"],
                "suggested_actions": ["Review Chapter 4", "Assign practice problems on Kinetics"],
                "feedback_summary": "Overall, the class has a good grasp of the basics, but many struggled with the application questions. 85% of students showed improvement in theoretical understanding."
             }

        try:
            prompt = f"""
            You are an AI assistant for teachers.
            Analyze the following student assessment content (extracted from {filename}).
            Identify learning gaps, summarize common mistakes, and generate clear, actionable feedback.
            Do not replace the teacher’s judgment.

            Content Snippet:
            {file_content[:4000]}... (truncated)

            Output JSON:
            {{
                "weak_topics": ["topic1", "topic2"],
                "students_needing_attention": ["student1", "student2"], # infer from context or return generic
                "suggested_actions": ["action1", "action2"],
                "feedback_summary": "text summary"
            }}
            """
            
            response = client.chat.completions.create(
                model=Config.AZURE_OPENAI_DEPLOYMENT_NAME if isinstance(client, AzureOpenAI) else "gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
             logger.error(f"Error in analyze_uploaded_file: {str(e)}")
             return {
                "weak_topics": ["Error analyzing topics"],
                "students_needing_attention": [],
                "suggested_actions": ["Please review manually"],
                "feedback_summary": "AI analysis failed. Please try again."
             }