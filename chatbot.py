import os
from dotenv import load_dotenv

load_dotenv()

# Load Microsoft's pre-trained conversational model when no API key is configured.
model_name = "microsoft/DialoGPT-small"
tokenizer = None
model = None
openai_client = None


def load_model():
    global tokenizer, model

    if tokenizer is None or model is None:
        from transformers import AutoModelForCausalLM, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

    return tokenizer, model

def generate_response(user_input):
    if not isinstance(user_input, str) or not user_input.strip():
        return "Please enter a message."

    message = user_input.strip()
    normalized_message = message.lower().strip(" .,!?")
    if normalized_message in {"hi", "hello", "hey", "good morning", "good afternoon", "good evening"}:
        return "Hi! How can I help you today?"

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return "Please configure OPENAI_API_KEY before asking general questions."

    try:
        from openai import OpenAI

        global openai_client
        if openai_client is None:
            openai_client = OpenAI(api_key=api_key)

        result = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful, concise assistant."},
                {"role": "user", "content": message}
            ],
            max_tokens=300
        )
        response = result.choices[0].message.content
        if response and response.strip():
            return response.strip()
    except Exception:
        return "I could not reach the AI service. Check your API key, internet connection, and account billing."

    try:
        tokenizer, model = load_model()

        # Encode the new user input
        new_user_input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors='pt')

        # Generate a response from the model
        chat_history_ids = model.generate(
            new_user_input_ids,
            max_new_tokens=100,
            pad_token_id=tokenizer.eos_token_id
        )

        # Decode the response tokens back to clear text
        bot_response = tokenizer.decode(
            chat_history_ids[:, new_user_input_ids.shape[-1]:],
            skip_special_tokens=True
        ).strip()
        if bot_response:
            return bot_response
    except Exception:
        # Keep the chat usable when the local model is not installed or unavailable.
        pass

    return "I can help with that. Could you tell me a little more?"
