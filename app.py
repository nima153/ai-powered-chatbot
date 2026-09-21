from flask import Flask, request, jsonify, render_template
from chatbot import generate_response
from database import init_db, log_interaction

app = Flask(__name__)

# Initialize database when app starts
init_db()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True)
    
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' field in request data"}), 400
    
    user_message = data['message']

    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({"error": "'message' must be a non-empty string"}), 400
    
    # Get the AI-powered response
    try:
        bot_reply = generate_response(user_message)
    except Exception as error:
        app.logger.exception("Unable to generate chatbot response")
        return jsonify({"error": "The AI model could not generate a response", "details": str(error)}), 503
    
    # Save the conversation history to SQLite
    log_interaction(user_message, bot_reply)
    
    return jsonify({
        "user": user_message,
        "bot": bot_reply
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
