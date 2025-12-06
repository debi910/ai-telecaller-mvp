"""
100% FREE AI Telecaller MVP
No costs - perfect for testing!
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from groq import Groq
import json
from datetime import datetime
import os

# Get port from environment (Railway provides this)
PORT = int(os.getenv("PORT", 8000))

app = FastAPI(title="Free AI Telecaller MVP")

# Initialize Groq (FREE!)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-api-key-here")
groq_client = Groq(api_key=GROQ_API_KEY)

# In-memory storage for MVP (no database needed!)
conversations = {}
all_leads = []

class FreeMVPTelecaller:
    """100% Free AI Telecaller"""
    
    def __init__(self):
        self.languages = {
            'hi': 'Hindi',
            'en': 'English',
            'or': 'Odia'
        }
    
    def detect_language(self, text):
        """Auto-detect language"""
        text_lower = text.lower()
        
        # Odia script detection
        if any('\u0B00' <= c <= '\u0B7F' for c in text):
            return 'or'
        
        # Hindi script detection
        if any('\u0900' <= c <= '\u097F' for c in text):
            return 'hi'
        
        # English (default)
        return 'en'
    
    def get_system_prompt(self, language, customer_data):
        """Get language-specific system prompt"""
        
        prompts = {
            'hi': f"""आप एक professional telecalling agent हैं। 

पहले से मिली जानकारी: {json.dumps(customer_data, ensure_ascii=False)}

आपको ये collect करना है:
- नाम (name)
- शहर (city)
- सर्विस (service: fiber/software/iot)
- मोबाइल नंबर (phone)

नियम:
1. हर reply में सिर्फ 1-2 वाक्य बोलें
2. आप और जी का उपयोग करें
3. अगर कोई info missing है तो उसके बारे में पूछें
4. सब info मिलने पर धन्यवाद कहें और बताएं कि टीम contact करेगी

संक्षिप्त और स्वाभाविक रहें।""",
            
            'en': f"""You are a professional telecalling agent.

Already collected: {customer_data}

You need to collect:
- name
- city  
- service (fiber/software/iot)
- phone number

Rules:
1. Keep responses to 1-2 sentences
2. Be polite and professional
3. Ask for missing information
4. When complete, thank them and say team will contact

Be brief and natural.""",
            
            'or': f"""ଆପଣ ଜଣେ professional telecalling agent।

ପୂର୍ବରୁ ମିଳିଛି: {customer_data}

ଆପଣଙ୍କୁ collect କରିବାକୁ ହେବ:
- ନାମ
- ସହର
- ସେବା (fiber/software/iot)
- ଫୋନ୍ ନମ୍ବର

ନିୟମ:
1. ପ୍ରତ୍ୟେକ reply ରେ 1-2 ବାକ୍ୟ
2. ବିନୟୀ ରୁହନ୍ତୁ
3. Missing info ପାଇଁ ପଚାରନ୍ତୁ
4. Complete ହେଲେ ଧନ୍ୟବାଦ ଦିଅନ୍ତୁ

ସଂକ୍ଷିପ୍ତ ଏବଂ ସ୍ୱାଭାବିକ ରୁହନ୍ତୁ।"""
        }
        
        return prompts.get(language, prompts['en'])
    
    def get_groq_response(self, user_message, language, customer_data, history):
        """Get AI response using FREE Groq API"""
        
        system_prompt = self.get_system_prompt(language, customer_data)
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 4 messages only)
        for h in history[-4:]:
            messages.append({"role": "user", "content": h.get('user', '')})
            if 'assistant' in h:
                messages.append({"role": "assistant", "content": h['assistant']})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def extract_info(self, text, language):
        """Extract customer information"""
        
        prompt = f"""From this text, extract ONLY these fields as JSON:

Text: "{text}"

Return format (use null if not found):
{{"name": null, "city": null, "service": null, "phone": null}}

Service must be one of: fiber, software, iot (lowercase)
Phone should be 10 digits only.

Return ONLY the JSON, nothing else."""

        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=80
            )
            
            response = completion.choices[0].message.content.strip()
            response = response.replace('```json', '').replace('```', '').strip()
            
            return json.loads(response)
        except:
            return {}
    
    def is_complete(self, data):
        """Check if all required info collected"""
        required = ['name', 'city', 'service']
        return all(data.get(field) for field in required)
    
    def simulate_whatsapp(self, phone, customer_data, language):
        """Simulate WhatsApp message (for MVP)"""
        
        messages = {
            'hi': f"""✅ WhatsApp Message (Simulated)

नमस्ते {customer_data['name']} जी!

आपके call के लिए धन्यवाद।

📍 शहर: {customer_data.get('city', 'N/A')}
🎯 सर्विस: {customer_data.get('service', 'N/A').title()}

हमारी टीम 24 घंटे में संपर्क करेगी।

धन्यवाद!
- AI Telecaller Team""",
            
            'en': f"""✅ WhatsApp Message (Simulated)

Hello {customer_data['name']}!

Thank you for your call.

📍 City: {customer_data.get('city', 'N/A')}
🎯 Service: {customer_data.get('service', 'N/A').title()}

Our team will contact you within 24 hours.

Thank you!
- AI Telecaller Team""",
            
            'or': f"""✅ WhatsApp Message (Simulated)

ନମସ୍କାର {customer_data['name']} ଜୀ!

ଆପଣଙ୍କ call ପାଇଁ ଧନ୍ୟବାଦ।

📍 ସହର: {customer_data.get('city', 'N/A')}
🎯 ସେବା: {customer_data.get('service', 'N/A').title()}

ଆମ ଟିମ୍ 24 ଘଣ୍ଟା ମଧ୍ୟରେ ସମ୍ପର୍କ କରିବ।

ଧନ୍ୟବାଦ!
- AI Telecaller Team"""
        }
        
        return messages.get(language, messages['en'])
    
    def save_to_sheets_simulation(self, data):
        """Simulate saving to Google Sheets"""
        
        all_leads.append({
            'timestamp': datetime.now().isoformat(),
            **data
        })
        
        print(f"\n✅ Saved to 'Google Sheets':")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"\nTotal leads collected: {len(all_leads)}\n")

# Initialize telecaller
telecaller = FreeMVPTelecaller()

@app.get("/", response_class=HTMLResponse)
async def home():
    """Web chat interface"""
    
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Telecaller - Free MVP</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            width: 100%;
            max-width: 600px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 25px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 1.8em;
            margin-bottom: 5px;
        }
        
        .free-badge {
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 15px;
            display: inline-block;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .chat-container {
            height: 500px;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message.bot {
            justify-content: flex-start;
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-bubble {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        
        .bot .message-bubble {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-bottom-left-radius: 4px;
        }
        
        .user .message-bubble {
            background: #e3f2fd;
            color: #1565c0;
            border-bottom-right-radius: 4px;
        }
        
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
        }
        
        #userInput {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 1em;
            outline: none;
            transition: border 0.3s;
        }
        
        #userInput:focus {
            border-color: #667eea;
        }
        
        #sendBtn {
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        #sendBtn:hover {
            transform: scale(1.05);
        }
        
        #sendBtn:active {
            transform: scale(0.95);
        }
        
        .typing-indicator {
            display: none;
            padding: 12px 18px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 18px;
            border-bottom-left-radius: 4px;
            max-width: 70px;
        }
        
        .typing-indicator span {
            height: 8px;
            width: 8px;
            background: white;
            border-radius: 50%;
            display: inline-block;
            margin: 0 2px;
            animation: bounce 1.4s infinite;
        }
        
        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes bounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        
        .language-indicator {
            text-align: center;
            padding: 8px;
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            font-size: 0.9em;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Telecaller</h1>
            <div class="free-badge">100% FREE MVP</div>
            <p style="font-size: 0.9em; margin-top: 10px;">Testing Multi-Language AI Agent</p>
        </div>
        
        <div class="language-indicator" id="langIndicator">
            Detecting language...
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message bot">
                <div class="message-bubble">
                    नमस्ते! Hello! ନମସ୍କାର!<br><br>
                    मैं AI Telecaller हूं। I'm an AI Telecaller.<br>
                    आपका नाम क्या है? What's your name?
                </div>
            </div>
        </div>
        
        <div class="input-container">
            <div class="input-group">
                <input type="text" id="userInput" placeholder="Type your message..." />
                <button id="sendBtn">Send</button>
            </div>
        </div>
    </div>
    
    <script>
        const chatContainer = document.getElementById('chatContainer');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');
        const langIndicator = document.getElementById('langIndicator');
        
        let sessionId = 'session_' + Date.now();
        
        function addMessage(text, isBot = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isBot ? 'bot' : 'user'}`;
            
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            bubble.innerHTML = text.replace(/\\n/g, '<br>');
            
            messageDiv.appendChild(bubble);
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function showTyping() {
            const typing = document.createElement('div');
            typing.className = 'message bot';
            typing.id = 'typingIndicator';
            typing.innerHTML = `
                <div class="typing-indicator" style="display: flex;">
                    <span></span><span></span><span></span>
                </div>
            `;
            chatContainer.appendChild(typing);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function hideTyping() {
            const typing = document.getElementById('typingIndicator');
            if (typing) typing.remove();
        }
        
        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;
            
            addMessage(message, false);
            userInput.value = '';
            showTyping();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        session_id: sessionId,
                        message: message
                    })
                });
                
                const data = await response.json();
                hideTyping();
                
                addMessage(data.response, true);
                
                if (data.language) {
                    const langs = {hi: 'Hindi', en: 'English', or: 'Odia'};
                    langIndicator.textContent = `Language: ${langs[data.language]} ✓`;
                }
                
                if (data.complete) {
                    addMessage(`
                        ✅ <strong>Information Collected!</strong><br><br>
                        ${data.whatsapp_preview}
                    `, true);
                }
                
            } catch (error) {
                hideTyping();
                addMessage('Error: Could not connect to server', true);
            }
        }
        
        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        userInput.focus();
    </script>
</body>
</html>
    """
    return html

@app.post("/chat")
async def chat(request: Request):
    """Handle chat messages"""
    
    data = await request.json()
    session_id = data['session_id']
    user_message = data['message']
    
    # Initialize session if new
    if session_id not in conversations:
        conversations[session_id] = {
            'language': None,
            'data': {},
            'history': []
        }
    
    session = conversations[session_id]
    
    # Detect language
    if not session['language']:
        session['language'] = telecaller.detect_language(user_message)
    
    # Extract information
    extracted = telecaller.extract_info(user_message, session['language'])
    session['data'].update({k: v for k, v in extracted.items() if v})
    
    # Get AI response
    ai_response = telecaller.get_groq_response(
        user_message,
        session['language'],
        session['data'],
        session['history']
    )
    
    # Add to history
    session['history'].append({
        'user': user_message,
        'assistant': ai_response
    })
    
    # Check if complete
    is_complete = telecaller.is_complete(session['data'])
    
    response_data = {
        'response': ai_response,
        'language': session['language'],
        'complete': is_complete,
        'collected_data': session['data']
    }
    
    if is_complete:
        # Simulate saving and WhatsApp
        telecaller.save_to_sheets_simulation(session['data'])
        whatsapp_msg = telecaller.simulate_whatsapp(
            session['data'].get('phone', 'N/A'),
            session['data'],
            session['language']
        )
        response_data['whatsapp_preview'] = whatsapp_msg
        
        print(f"\n{whatsapp_msg}\n")
    
    return response_data

@app.get("/leads")
async def get_leads():
    """View all collected leads"""
    return {
        'total': len(all_leads),
        'leads': all_leads
    }

@app.get("/stats")
async def get_stats():
    """Get statistics"""
    
    stats = {
        'total_conversations': len(conversations),
        'total_leads': len(all_leads),
        'by_language': {},
        'by_service': {}
    }
    
    for lead in all_leads:
        lang = lead.get('language', 'unknown')
        service = lead.get('service', 'unknown')
        
        stats['by_language'][lang] = stats['by_language'].get(lang, 0) + 1
        stats['by_service'][service] = stats['by_service'].get(service, 0) + 1
    
    return stats

# This is the only if __name__ block - removed duplicate!
if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║        🚀 FREE AI TELECALLER MVP - STARTING...          ║
    ║                                                          ║
    ║  ✓ No phone calls needed (web chat)                     ║
    ║  ✓ Multi-language AI (Hindi/English/Odia)               ║
    ║  ✓ 100% FREE - No costs!                                ║
    ║                                                          ║
    ║  Open: http://localhost:8000                            ║
    ║                                                          ║
    ║  View leads: http://localhost:8000/leads                ║
    ║  View stats: http://localhost:8000/stats                ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)
