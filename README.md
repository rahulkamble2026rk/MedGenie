#MedGenie: AI-Powered Medical Chatbot
Check out MedGenie, my AI-powered medical chatbot built for quick health insights. Perfect for showing off my coding skills in interviews!

#Features
General Diagnosis: Answers symptom queries (e.g., "headache").

Report Analyzer: Processes uploaded PDF reports.
Prescription Reader: Reads prescription images.
Google Calendar: Sets med reminders (e.g., "take meds at 8 AM").
Context-Aware Chats: Remembers past talks.
Chat Management: Edit, delete, new chat, save.
YouTube Links: Adds video refs.
Assistive Mode: Asks follow-ups or suggests doctors.
Tech Stack
Backend: Python, Flask, LangChain, Hugging Face, Groq Llama3-70b-8192, FAISS, PyPDF2, Pytesseract, Google API.
Frontend: React, Axios.
Installation
Clone
bash
git clone https://github.com/your-username/medgenie.git
cd medgenie
Backend
Install:
bash
pip install -r requirements.txt
Set .env:
text
GROQ_API_KEY=your_key
YOUTUBE_API_KEY=your_key
Run:
bash
python app.py
Frontend
Go to frontend:
bash
cd frontend
Install:
bash
npm install
Start:
bash
npm start
Access: Hit http://localhost:3000, use guest login: Username: guest, Password: guest123.
Routes
/api/login: Handles user login.
/api/chat: Processes general chats.
/api/general_diagnosis: Gives structured diagnosis.
/api/report_analyzer: Analyzes PDF reports.
/api/prescription_reader: Reads prescription images.
/api/calendar: Sets calendar events.
/api/transcribe: Converts voice to text.
/api/delete_message: Removes a message.
/api/delete_chat: Deletes a chat.
/api/edit_message: Edits a message.
/api/logout: Logs out user.
/api/google_login: Initiates Google auth.
/callback: Handles OAuth callback.
Flow
User inputs via React (chat, file, calendar).
Flask routes to the right API endpoint.
FAISS pulls relevant data from ai-medical-chatbot.csv (and PDFs if added).
Groq Llama3-70b-8192 generates structured response.
Response sent back to React, with YouTube links if applicable.
Architecture
text
User (React) --> Flask API --> Knowledge Base (FAISS, CSV/PDFs) --> Groq LLM --> Response
                  |                        |
                  +----> YouTube API ----->+
Fixes
OCR: Grayscale fix for bad images.
Audio: Validated WAV headers.
Calendar: Per-user token storage.
Next Steps
Fine-tune LLM with med data.
Add multi-language.
Deploy on AWS.
Contribute
Fork it, tweak it, or open issues!
