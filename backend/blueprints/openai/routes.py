from flask import request, jsonify
from . import openai_bp
from services.openai_service import OpenAIService

@openai_bp.route('/chat', methods=['POST'])
def chat_completion():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400

        message = data.get('message')
        if not message:
            return jsonify({"error": "Message is required"}), 400

        history = data.get('history', [])
        context = data.get('context', "General Assistant")

        # Basic history formatting validation if needed, assuming list of dicts
        # OpenAIService.ask_ai expects a list of message dicts for history

        # Add current user message to logical history for the service call if not explicitly separated
        # Looking at OpenAIService.ask_ai, it takes (history, context). 
        # It assumes history implies *previous* messages. 
        # But wait, lines 90-91 of openai_service.py: 
        # messages = [{"role": "system"...}]
        # messages.extend(history)
        # So it does NOT automatically add the user message if it's not in the 'history' list passed to it?
        # Let's check ask_ai again. 
        # Step 551 View Code:
        # def ask_ai(cls, history, context="General learning"):
        # ... messages.extend(history)
        # ... client.chat.completions.create(..., messages=messages)
        # 
        # So 'history' MUST include the user's current query as the last item.
        
        # Prepare history
        full_history = history if history else []
        full_history.append({"role": "user", "content": message})
        
        response_text = OpenAIService.ask_ai(full_history, context=context)

        return jsonify({
            "response": response_text
        }), 200

    except Exception as e:
        return jsonify({"error": f"OpenAI Error: {str(e)}"}), 500
