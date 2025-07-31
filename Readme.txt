# MedGenie: AI-Powered Medical Chatbot

Check out MedGenie, my AI-driven medical chatbot designed to provide fast and reliable health insights. Last updated: 03:59 PM IST, Thursday, July 31, 2025.

---

## Features

- *Diagnosis*: Answers symptom queries (e.g., "headache") with structured responses.
- *Report Analyzer*: Processes uploaded PDF medical reports for key insights.
- *Prescription Reader*: Extracts and interprets text from prescription images.
- *Google Calendar*: Sets medication and appointment reminders (e.g., "take meds at 8 AM").
- *Context-Aware Chats*: Remembers past conversations for personalized interactions.
- *Chat Management*: Offers edit, delete, new chat, and save options.
- *YouTube Links*: Provides relevant video references for education.
- *Assistive Mode*: Suggests follow-up questions or recommends doctor consultations.

---

## Tech Stack

### Backend
- *Python*: Core language for development.
- *Flask*: Lightweight web framework for API endpoints.
- *LangChain*: Manages LLM interactions and context.
- *Hugging Face*: Provides pre-trained embedding models.
- *Groq Llama3-70b-8192*: High-performance LLM for natural language processing.
- *FAISS*: Vector database for efficient similarity searches.
- *PyPDF2*: Extracts text from PDF files.
- *Pytesseract*: Performs OCR on images.
- *Google API*: Integrates Google Calendar and authentication.

### Frontend
- *React*: Component-based UI framework.
- *Axios*: Handles HTTP requests to the backend.

---

## Installation

### Clone the Repository
bash
git clone https://github.com/Rahul23314/MedGenie.git
cd MedGenie

Install Dependencies
bashpip install -r requirements.txt

Set Environment Variables
Create a .env file in the root directory:
textGROQ_API_KEY=your_groq_api_key
YOUTUBE_API_KEY=your_youtube_api_key

Run the Backend
bashpython app.py


Frontend Setup
Navigate to Frontend
bashcd frontend

Install Dependencies
bash
npm install

Start the Frontend
bash
npm start

Access the Application
Open http://localhost:3000 in your browser and use guest login:

Username: guest
Password: guest123



📡 API Routes

/api/login: Authenticates users with username and password.
/api/chat: Handles general chat interactions.
/api/general_diagnosis: Provides structured medical diagnosis.
/api/report_analyzer: Analyzes uploaded PDF reports.
/api/prescription_reader: Interprets prescription images.
/api/calendar: Creates Google Calendar events for reminders.
/api/transcribe: Converts voice input to text.
/api/delete_message: Removes a specific chat message.
/api/delete_chat: Deletes an entire chat session.
/api/edit_message: Updates the content of a chat message.
/api/logout: Ends the user session.
/api/google_login: Initiates Google OAuth for calendar access.
/callback: Handles OAuth callback from Google.


⚙ Flow

User Input: Entered via React interface (text, file upload, or calendar details).
Flask Routing: Directs the request to the appropriate API endpoint.
FAISS Retrieval: Fetches relevant data from ai-medical-chatbot.csv or uploaded PDFs.
Groq Llama3-70b-8192: Generates a structured response based on retrieved context.
Response Delivery: Returned to React with optional YouTube links.

Architecture Diagram
<img src="https://github.com/user-attachments/assets/6bd5d8d6-cda1-4b5e-8e25-47fe474c6a5b" alt="Architecture">
textUser (React) --> Flask API --> Knowledge Base (FAISS, CSV/PDFs) --> Groq LLM --> Response
                  |                        |
                  +----> YouTube API ----->+

🛠 Implementation Notes

OCR: Implements grayscale conversion to improve text extraction from low-quality images.
Audio: Validates WAV file headers for accurate transcription.
Calendar: Stores per-user tokens securely for Google Calendar integration.
Future Enhancements:

Fine-tune the LLM with domain-specific medical datasets.
Add support for multiple languages.
Deploy on AWS or Heroku for scalability.




##Glimpse 
1.
<img width="1379" height="772" alt="3" src="https://github.com/user-attachments/assets/90b7e79b-f1b4-4def-9a18-ddf2378d6e14" />
<br><br>
2.
<img width="1912" height="912" alt="4" src="https://github.com/user-attachments/assets/7d976bc7-b143-4dfc-a931-189d75977fcd" />
<br><br>
3. 
<img width="1919" height="914" alt="5" src="https://github.com/user-attachments/assets/c6ec567f-38c9-4b3d-a702-ec191e7f8c30" />
<br><br>
4.
<img width="1919" height="915" alt="6" src="https://github.com/user-attachments/assets/e99e8d14-410a-4866-9e48-0959fc100046" />
<br><br>
5.
<img width="1919" height="914" alt="7" src="https://github.com/user-attachments/assets/ff8dc43c-c2a2-4e2d-aedd-3702e68f93e4" />
<br><br>
6.
<img width="1919" height="915" alt="8" src="https://github.com/user-attachments/assets/14602e7e-4a50-4eed-b880-804c0424def0" />
<br><br>
7.Architecture Diagram:
<img width="1577" height="1417" alt="2" src="https://github.com/user-attachments/assets/b08fa276-15fe-4f1b-940e-d4fe86e0d49c" />


##🤝 Contribute

Fork the Repository: Create your own copy to work on.
Tweak the Code: Add features or improve existing ones.
Open Issues: Report bugs or suggest enhancements on GitHub.

---