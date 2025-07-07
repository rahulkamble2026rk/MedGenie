**MedGenie: AI-Powered Medical Chatbot**
Check out MedGenie, my AI-driven medical chatbot for fast health insights. Built to impress in interviews!

**Features**
Diagnosis: Answers symptom queries (e.g., "headache").
Report Analyzer: Processes uploaded PDF reports.
Prescription Reader: Reads prescription images.
Google Calendar: Sets med reminders (e.g., "take meds at 8 AM").
Context-Aware Chats: Remembers past talks.
Chat Management: Edit, delete, new chat, save.
YouTube Links: Adds video references.
Assistive Mode: Follow-up questions or doctor suggestions.

**Tech Stack**
Backend: Python, Flask, LangChain, Hugging Face, Groq Llama3-70b-8192, FAISS, PyPDF2, Pytesseract, Google API.
Frontend: React, Axios.

**git clone https://github.com/your-username/medgenie.git** 
![image](https://github.com/user-attachments/assets/57808c79-d2a4-44e9-9825-0d24048020c4)                       




cd medgenie
Backend
![image](https://github.com/user-attachments/assets/c4b08f58-0102-408b-9fe8-f9572ca9d2ab)                     





**Backend**
**Install**
pip install -r requirements.txt**

**Set .env:**
GROQ_API_KEY=your_key
YOUTUBE_API_KEY=your_key 

Run:
python app.py 

**Frontend **
Go to frontend:
cd frontend

![image](https://github.com/user-attachments/assets/de593524-7c7d-46d8-8209-b1d0194be20e)

**Install:**
npm install

**Start:**
npm start
Access: Hit http://localhost:3000, use guest login: Username: guest, Password: guest123. 

** 📡 API Routes**  
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


**⚙️Flow**
User inputs via React (chat, file, calendar).
Flask routes to the right API endpoint.
FAISS pulls relevant data from ai-medical-chatbot.csv (and PDFs if added).
Groq Llama3-70b-8192 generates structured response.
Response sent back to React, with YouTube links if applicable. 

**🏗 Architecture**

**User (React) --> Flask API --> Knowledge Base (FAISS, CSV/PDFs) --> Groq LLM --> Response
                  |                        |
                  +----> YouTube API ----->+** 

![image](https://github.com/user-attachments/assets/6bd5d8d6-cda1-4b5e-8e25-47fe474c6a5b)

**🛠 Implementation Notes**
OCR: Grayscale fix for bad images.
Audio: Validated WAV headers.
Calendar: Per-user token storage.
Fine-tune LLM with med data.
Add multi-language.
Deploy on AWS.

**🤝Contribute**
Fork it, tweak it, or open issues!
