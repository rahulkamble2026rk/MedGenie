# MedGenie: AI-Powered Medical Chatbot

Check out MedGenie, my AI-driven medical chatbot designed to provide fast and reliable health insights. Last updated: 03:59 PM IST, Thursday, July 31, 2025.

---

## Features

- **Diagnosis**: Answers symptom queries (e.g., "headache") with structured responses.
- **Report Analyzer**: Processes uploaded PDF medical reports for key insights.
- **Prescription Reader**: Extracts and interprets text from prescription images.
- **Google Calendar**: Sets medication and appointment reminders (e.g., "take meds at 8 AM").
- **Context-Aware Chats**: Remembers past conversations for personalized interactions.
- **Chat Management**: Offers edit, delete, new chat, and save options.
- **YouTube Links**: Provides relevant video references for education.
- **Assistive Mode**: Suggests follow-up questions or recommends doctor consultations.

---

## Tech Stack

### Backend
- **Python**: Core language for development.
- **Flask**: Lightweight web framework for API endpoints.
- **LangChain**: Manages LLM interactions and context.
- **Hugging Face**: Provides pre-trained embedding models.
- **Groq Llama3-70b-8192**: High-performance LLM for natural language processing.
- **FAISS**: Vector database for efficient similarity searches.
- **PyPDF2**: Extracts text from PDF files.
- **Pytesseract**: Performs OCR on images.
- **Google API**: Integrates Google Calendar and authentication.

### Frontend
- **React**: Component-based UI framework.
- **Axios**: Handles HTTP requests to the backend.

---

## Installation

### Clone the Repository
```bash
git clone https://github.com/Rahul23314/MedGenie.git
cd MedGenie
Backend Setup
<img src="https://github.com/user-attachments/assets/fb7c57ee-4027-434d-b415-999367e0a306" alt="Backend Directory">

Install Dependencies
bashpip install -r requirements.txt

Set Environment Variables
Create a .env file in the root directory:
textGROQ_API_KEY=your_groq_api_key
YOUTUBE_API_KEY=your_youtube_api_key

Run the Backend
bashpython app.py


Frontend Setup
<img src="https://github.com/user-attachments/assets/de593524-7c7d-46d8-8209-b1d0194be20e" alt="Frontend Directory">

Navigate to Frontend
bashcd frontend

Install Dependencies
bashnpm install

Start the Frontend
bashnpm start

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


⚙️ Flow

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




Some Glimpses
<img src="https://github.com/user-attachments/assets/6a5a4c98-b811-4465-bc19-721878223fde" alt="Glimpse 1">
<img src="https://github.com/user-attachments/assets/ab2a2f39-503b-4e56-a493-b264844cf38e" alt="Glimpse 2">
<img src="https://github.com/user-attachments/assets/5c11a42e-783b-45c9-83d3-53c356d4856c" alt="Glimpse 3">
<img src="https://github.com/user-attachments/assets/8fa151f1-f11a-4671-ab96-cbb8d3d2342b" alt="Glimpse 4">
<img src="https://github.com/user-attachments/assets/9d5abf2a-a964-4288-8529-098258f7098a" alt="Glimpse 5">
<img src="https://github.com/user-attachments/assets/e80fd910-bb4b-4b67-b757-b76ad60c76c4" alt="Glimpse 6">

🤝 Contribute

Fork the Repository: Create your own copy to work on.
Tweak the Code: Add features or improve existing ones.
Open Issues: Report bugs or suggest enhancements on GitHub.
