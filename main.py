import os
from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

# load environment variables
load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
GENAI_API_KEY = os.getenv('GENAI_API_KEY')

# Initialize clients
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
genai.configure(api_key=GENAI_API_KEY )
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)


# Initialize clients
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
genai.configure(api_key=GENAI_API_KEY)

app = Flask(__name__)
# Home route
@app.route('/')
def index():
    return "Hola, soy el servidor de conversaciones AI"

# Webhook to handle messages
@app.route("/callback", methods=['POST'])
@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    # AI-powered Spanish conversation generation
    response = generate_spanish_response(user_message)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )

def generate_spanish_response(message):
    # Configure the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are a friendly Spanish conversationalist. 
    Respond to the following message in Spanish, 
    followed by an English translation:
    
    User: {message}
    
    Spanish Response (with English translation):
    """
    
    try:
        # Generate response using Gemini
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lo siento, ha ocurrido un error. / Sorry, an error occurred. {str(e)}"

if __name__ == "__main__":
    app.run(port=5000)