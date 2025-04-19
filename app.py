# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # from config import Config
# # from utils.data_processing import load_and_process_data
# # from utils.vector_store import create_vector_store
# # from utils.groq_client import initialize_groq_client, generate_response
# # import pickle
# # import os
# # import hashlib
# # import logging
# # import secrets
# # import PyPDF2
# # import pytesseract
# # from PIL import Image
# # import io

# # # Set up logging
# # logging.basicConfig(level=logging.DEBUG)
# # logger = logging.getLogger(__name__)

# # app = Flask(__name__)
# # CORS(app, resources={r"/api/*": {"origins": "*"}})  # Explicit CORS for debugging

# # # Load data and initialize vector store once at startup
# # try:
# #     documents = load_and_process_data(Config.DATA_PATH)
# #     vectorstore = create_vector_store(documents, Config.EMBEDDING_MODEL)
# #     groq_client = initialize_groq_client(Config.GROQ_API_KEY)
# # except Exception as e:
# #     logger.error(f"Failed to initialize components: {e}")
# #     raise

# # # Directories and files
# # HISTORY_DIR = "history"
# # USERS_FILE = "users.pkl"
# # os.makedirs(HISTORY_DIR, exist_ok=True)

# # # Load or initialize the users dictionary
# # def load_users():
# #     if os.path.exists(USERS_FILE):
# #         try:
# #             with open(USERS_FILE, "rb") as f:
# #                 return pickle.load(f)
# #         except Exception as e:
# #             logger.error(f"Error loading users: {e}")
# #             return {}
# #     return {}

# # def save_users(users):
# #     try:
# #         with open(USERS_FILE, "wb") as f:
# #             pickle.dump(users, f)
# #     except Exception as e:
# #         logger.error(f"Error saving users: {e}")

# # # Generate a unique UUID using a random salt
# # def generate_uuid(username, password):
# #     salt = secrets.token_hex(16)
# #     combined = f"{username}:{password}:{salt}"
# #     hash_obj = hashlib.sha256(combined.encode())
# #     user_id = hash_obj.hexdigest()
# #     logger.debug(f"Generated UUID for {username}: {user_id}")
# #     return user_id, salt

# # def load_user_history(user_id):
# #     history_file = f"{HISTORY_DIR}/{user_id}.pkl"
# #     logger.debug(f"Attempting to load history for user_id: {user_id}, file: {history_file}")
# #     if os.path.exists(history_file):
# #         try:
# #             with open(history_file, "rb") as f:
# #                 history = pickle.load(f)
# #                 if not history or not isinstance(history, list) or not all(isinstance(chat, dict) and 'topic' in chat and 'messages' in chat for chat in history):
# #                     logger.warning(f"Invalid history format for {user_id}. Converting to default structure.")
# #                     return [{"topic": "Default Chat", "messages": history if isinstance(history, list) else []}]
# #                 return history
# #         except (pickle.UnpicklingError, EOFError, Exception) as e:
# #             logger.error(f"Error loading history for {user_id}: {e}. Creating new history.")
# #             return [{"topic": "Default Chat", "messages": []}]
# #     logger.debug(f"No history file found for {user_id}. Initializing empty history.")
# #     return [{"topic": "Default Chat", "messages": []}]

# # def save_user_history(user_id, history):
# #     history_file = f"{HISTORY_DIR}/{user_id}.pkl"
# #     try:
# #         with open(history_file, "wb") as f:
# #             pickle.dump(history, f)
# #         logger.debug(f"Successfully saved history for user_id: {user_id} to {history_file}")
# #     except Exception as e:
# #         logger.error(f"Error saving history for {user_id}: {e}")

# # @app.route("/api/login", methods=["POST"])
# # def login():
# #     data = request.get_json()
# #     username = data.get("username")
# #     password = data.get("password")

# #     if not username or not password:
# #         return jsonify({"error": "Username and password are required"}), 400

# #     users = load_users()
# #     if username not in users:
# #         user_id, salt = generate_uuid(username, password)
# #         users[username] = {"user_id": user_id, "salt": salt}
# #         save_users(users)
# #         logger.debug(f"New user {username} registered with user_id: {user_id}")
# #     else:
# #         user_id = users[username]["user_id"]
# #         logger.debug(f"Existing user {username} found with user_id: {user_id}")

# #     history = load_user_history(user_id)
# #     if not history or not all('topic' in chat for chat in history):
# #         history = [{"topic": "Default Chat", "messages": history if isinstance(history, list) else []}]
# #     return jsonify({"user_id": user_id, "username": username, "history": history})

# # @app.route("/api/chat", methods=["POST"])
# # def chat():
# #     data = request.get_json()
# #     prompt = data.get("prompt")
# #     user_id = data.get("user_id")

# #     if not prompt or not user_id:
# #         return jsonify({"error": "Prompt and user_id are required"}), 400

# #     history = load_user_history(user_id)
# #     if not history:
# #         history = [{"topic": "Default Chat", "messages": []}]
    
# #     current_chat = history[-1]
# #     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
# #         current_chat = {"topic": f"Chat {len(history)}", "messages": []}
# #         history.append(current_chat)
    
# #     current_chat["messages"].append({"role": "user", "content": prompt})

# #     try:
# #         docs = vectorstore.similarity_search(prompt, k=3)
# #         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
# #         full_context = "\n".join([msg["content"] for msg in current_chat["messages"]]) + "\n\n" + context
# #         response = generate_response(groq_client, prompt, full_context, Config.MODEL_NAME)
# #         if not response or not isinstance(response, str):
# #             raise ValueError("Invalid response from Groq API")
# #     except Exception as e:
# #         logger.error(f"Error in chat generation for user_id {user_id}: {e}")
# #         response = f"Error generating response: {str(e)}"

# #     current_chat["messages"].append({"role": "assistant", "content": response})
# #     save_user_history(user_id, history)
# #     return jsonify({"response": response, "user_id": user_id})

# # @app.route("/api/general_diagnosis", methods=["POST"])
# # def general_diagnosis():
# #     data = request.get_json()
# #     prompt = data.get("prompt")
# #     user_id = data.get("user_id")

# #     if not prompt or not user_id:
# #         return jsonify({"error": "Prompt and user_id are required"}), 400

# #     history = load_user_history(user_id)
# #     if not history:
# #         history = [{"topic": "General Diagnosis", "messages": []}]
    
# #     current_chat = history[-1]
# #     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
# #         current_chat = {"topic": "General Diagnosis", "messages": []}
# #         history.append(current_chat)
    
# #     current_chat["messages"].append({"role": "user", "content": prompt})

# #     try:
# #         docs = vectorstore.similarity_search(prompt, k=3)
# #         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
# #         full_context = "\n".join([msg["content"] for msg in current_chat["messages"]]) + "\n\n" + context
# #         diagnosis_prompt = (
# #             f"Act as a medical assistant. Based on the symptoms described: '{prompt}', "
# #             "provide a structured response with sections for Symptoms, Causes, and Remedies. "
# #             "If the information is insufficient or ambiguous, state that a definitive diagnosis cannot be made "
# #             "and recommend consulting a healthcare professional."
# #         )
# #         response = generate_response(groq_client, diagnosis_prompt, full_context, Config.MODEL_NAME)
# #         if not response or not isinstance(response, str):
# #             raise ValueError("Invalid response from Groq API")
# #     except Exception as e:
# #         logger.error(f"Error in general diagnosis for user_id {user_id}: {e}")
# #         response = f"Error generating response: {str(e)}"

# #     current_chat["messages"].append({"role": "assistant", "content": response})
# #     save_user_history(user_id, history)
# #     return jsonify({"response": response, "user_id": user_id})

# # @app.route("/api/report_analyzer", methods=["POST"])
# # def report_analyzer():
# #     logger.debug(f"Received request for /api/report_analyzer")
# #     if 'file' not in request.files or not request.form.get("user_id"):
# #         logger.error("Missing file or user_id")
# #         return jsonify({"error": "PDF file and user_id are required"}), 400

# #     file = request.files['file']
# #     user_id = request.form.get("user_id")
# #     logger.debug(f"Processing report for user_id: {user_id}, filename: {file.filename}")

# #     if not file.filename.endswith('.pdf'):
# #         logger.error(f"Invalid file type: {file.filename}")
# #         return jsonify({"error": "Only PDF files are supported"}), 400

# #     # Validate file size (e.g., 10MB limit)
# #     file.seek(0, os.SEEK_END)
# #     file_size = file.tell()
# #     if file_size > 10 * 1024 * 1024:
# #         logger.error(f"File size exceeds limit: {file_size} bytes")
# #         return jsonify({"error": "File size exceeds 10MB limit"}), 400
# #     file.seek(0)

# #     history = load_user_history(user_id)
# #     if not history:
# #         history = [{"topic": "Report Analysis", "messages": []}]
    
# #     current_chat = history[-1]
# #     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
# #         current_chat = {"topic": "Report Analysis", "messages": []}
# #         history.append(current_chat)
    
# #     current_chat["messages"].append({"role": "system", "content": "User uploaded a medical report for analysis"})

# #     try:
# #         # Extract text from PDF
# #         pdf_reader = PyPDF2.PdfReader(file)
# #         text = ""
# #         for page in pdf_reader.pages:
# #             page_text = page.extract_text()
# #             if page_text:
# #                 text += page_text + "\n"
        
# #         if not text.strip():
# #             logger.error("No text extracted from PDF")
# #             raise ValueError("No text could be extracted from the PDF")

# #         logger.debug(f"Extracted text (first 100 chars): {text[:100]}")
# #         text = text[:5000]  # Limit text
        
# #         docs = vectorstore.similarity_search(text, k=3)
# #         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
# #         full_context = text + "\n\n" + context
# #         analysis_prompt = (
# #             "Act as a medical assistant. Analyze the following medical report content: "
# #             f"'{text[:1000]}' (truncated for brevity). "
# #             "Provide a summary of key findings, such as diagnoses, test results, or recommendations. "
# #             "Structure the response with sections for Key Findings and Recommendations. "
# #             "If the content is unclear or insufficient, state that analysis is limited and recommend consulting a healthcare professional."
# #         )
# #         response = generate_response(groq_client, analysis_prompt, full_context, Config.MODEL_NAME)
# #         if not response or not isinstance(response, str):
# #             raise ValueError("Invalid response from Groq API")
# #     except Exception as e:
# #         logger.error(f"Error in report analysis for user_id {user_id}: {e}")
# #         response = f"Error processing report: {str(e)}"

# #     current_chat["messages"].append({"role": "assistant", "content": response})
# #     save_user_history(user_id, history)
# #     logger.debug(f"Report analysis completed for user_id: {user_id}")
# #     return jsonify({"response": response, "user_id": user_id})

# # @app.route("/api/prescription_reader", methods=["POST"])
# # def prescription_reader():
# #     logger.debug(f"Received request for /api/prescription_reader")
# #     if 'image' not in request.files or not request.form.get("user_id"):
# #         logger.error("Missing image or user_id")
# #         return jsonify({"error": "Image file and user_id are required"}), 400

# #     file = request.files['image']
# #     user_id = request.form.get("user_id")
# #     logger.debug(f"Processing prescription for user_id: {user_id}, filename: {file.filename}")

# #     if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
# #         logger.error(f"Invalid file type: {file.filename}")
# #         return jsonify({"error": "Only PNG, JPG, or JPEG images are supported"}), 400

# #     history = load_user_history(user_id)
# #     if not history:
# #         history = [{"topic": "Prescription Reading", "messages": []}]
    
# #     current_chat = history[-1]
# #     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
# #         current_chat = {"topic": "Prescription Reading", "messages": []}
# #         history.append(current_chat)
    
# #     current_chat["messages"].append({"role": "system", "content": "User uploaded a prescription image for reading"})

# #     try:
# #         image = Image.open(file)
# #         image = image.convert('L')
# #         text = pytesseract.image_to_string(image, lang='eng')
        
# #         if not text.strip():
# #             logger.error("No text extracted from image")
# #             raise ValueError("No text could be extracted from the image")

# #         logger.debug(f"Extracted text (first 100 chars): {text[:100]}")
# #         text = text[:5000]
        
# #         docs = vectorstore.similarity_search(text, k=3)
# #         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
# #         full_context = text + "\n\n" + context
# #         prescription_prompt = (
# #             "Act as a medical assistant. Analyze the following prescription text: "
# #             f"'{text[:1000]}' (truncated for brevity). "
# #             "Extract key details such as medications, dosages, and instructions. "
# #             "Structure the response with sections for Medications and Instructions. "
# #             "If the text is unclear or insufficient, state that analysis is limited and recommend consulting a pharmacist or healthcare professional."
# #         )
# #         response = generate_response(groq_client, prescription_prompt, full_context, Config.MODEL_NAME)
# #         if not response or not isinstance(response, str):
# #             raise ValueError("Invalid response from Groq API")
# #     except Exception as e:
# #         logger.error(f"Error in prescription reading for user_id {user_id}: {e}")
# #         response = f"Error processing prescription: {str(e)}"

# #     current_chat["messages"].append({"role": "assistant", "content": response})
# #     save_user_history(user_id, history)
# #     logger.debug(f"Prescription reading completed for user_id: {user_id}")
# #     return jsonify({"response": response, "user_id": user_id})

# # @app.route("/api/delete_message", methods=["POST"])
# # def delete_message():
# #     data = request.get_json()
# #     user_id = data.get("user_id")
# #     chat_index = data.get("chat_index")
# #     message_index = data.get("message_index")

# #     if not user_id or chat_index is None or message_index is None:
# #         return jsonify({"error": "user_id, chat_index, and message_index are required"}), 400

# #     history = load_user_history(user_id)
# #     if not history or chat_index >= len(history):
# #         return jsonify({"error": "Invalid chat index"}), 400

# #     if message_index >= len(history[chat_index]["messages"]):
# #         return jsonify({"error": "Invalid message index"}), 400

# #     history[chat_index]["messages"].pop(message_index)
# #     save_user_history(user_id, history)
# #     logger.debug(f"Deleted message {message_index} from chat {chat_index} for user_id: {user_id}")
# #     return jsonify({"message": "Message deleted successfully"})

# # @app.route("/api/delete_chat", methods=["POST"])
# # def delete_chat():
# #     data = request.get_json()
# #     user_id = data.get("user_id")
# #     chat_index = data.get("chat_index")

# #     if not user_id or chat_index is None:
# #         return jsonify({"error": "user_id and chat_index are required"}), 400

# #     history = load_user_history(user_id)
# #     if not history or chat_index >= len(history):
# #         return jsonify({"error": "Invalid chat index"}), 400

# #     history.pop(chat_index)
# #     save_user_history(user_id, history)
# #     logger.debug(f"Deleted chat {chat_index} for user_id: {user_id}")
# #     return jsonify({"message": "Chat deleted successfully"})

# # @app.route("/api/edit_message", methods=["POST"])
# # def edit_message():
# #     data = request.get_json()
# #     user_id = data.get("user_id")
# #     chat_index = data.get("chat_index")
# #     message_index = data.get("message_index")
# #     new_content = data.get("new_content")

# #     if not user_id or chat_index is None or message_index is None or not isinstance(new_content, str):
# #         return jsonify({"error": "user_id, chat_index, message_index, and new_content (string) are required"}), 400

# #     if not new_content.strip() or len(new_content) > 10000:
# #         return jsonify({"error": "new_content must be non-empty and less than 10,000 characters"}), 400

# #     history = load_user_history(user_id)
# #     if not history or chat_index >= len(history):
# #         return jsonify({"error": "Invalid chat index"}), 400

# #     if message_index >= len(history[chat_index]["messages"]):
# #         return jsonify({"error": "Invalid message index"}), 400

# #     history[chat_index]["messages"][message_index]["content"] = new_content.strip()
# #     save_user_history(user_id, history)
# #     logger.debug(f"Edited message {message_index} in chat {chat_index} for user_id: {user_id}")
# #     return jsonify({"message": "Message edited successfully"})

# # @app.route("/api/logout", methods=["POST"])
# # def logout():
# #     data = request.get_json()
# #     user_id = data.get("user_id")
# #     chat_history = data.get("chat_history", [])

# #     if user_id:
# #         if isinstance(chat_history, list) and all(isinstance(msg, dict) and 'role' in msg and 'content' in msg for msg in chat_history):
# #             formatted_history = [{"topic": "Default Chat", "messages": chat_history}]
# #         else:
# #             formatted_history = chat_history if all(isinstance(chat, dict) and 'topic' in chat and 'messages' in chat for chat in chat_history) else [{"topic": "Default Chat", "messages": []}]
# #         save_user_history(user_id, formatted_history)
# #         logger.debug(f"Logout for user_id: {user_id}. History saved.")
# #     return jsonify({"message": "Logged out successfully"})

# # if __name__ == "__main__":
# #     app.run(debug=True, host="0.0.0.0", port=5000) 
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from config import Config
# from utils.data_processing import load_and_process_data
# from utils.vector_store import create_vector_store
# from utils.groq_client import initialize_groq_client, generate_response
# import pickle
# import os
# import hashlib
# import logging
# import secrets
# import PyPDF2
# import pytesseract
# from PIL import Image
# import io
# from transformers import pipeline
# import tempfile
# from scipy.io.wavfile import write, read 
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# import datetime
# import numpy as np

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})
# SCOPES = ['https://www.googleapis.com/auth/calendar.events']
# CREDENTIALS_FILE = 'credentials.json' 

# # Load data and initialize components at startup
# try:
#     documents = load_and_process_data(Config.DATA_PATH)
#     vectorstore = create_vector_store(documents, Config.EMBEDDING_MODEL)
#     groq_client = initialize_groq_client(Config.GROQ_API_KEY)
#     # Initialize Whisper model for speech-to-text
#     logger.info("Loading Whisper model for speech-to-text...")
#     asr_pipeline = pipeline(
#         "automatic-speech-recognition",
#         model="openai/whisper-base",
#         chunk_length_s=2,
#         device=-1  # CPU; change to 0 for GPU
#     )
# except Exception as e:
#     logger.error(f"Failed to initialize components: {e}")
#     raise

# # Directories and files
# HISTORY_DIR = "history"
# USERS_FILE = "users.pkl"
# os.makedirs(HISTORY_DIR, exist_ok=True)

# # Load or initialize the users dictionary
# def load_users():
#     if os.path.exists(USERS_FILE):
#         try:
#             with open(USERS_FILE, "rb") as f:
#                 return pickle.load(f)
#         except Exception as e:
#             logger.error(f"Error loading users: {e}")
#             return {}
#     return {}

# def save_users(users):
#     try:
#         with open(USERS_FILE, "wb") as f:
#             pickle.dump(users, f)
#     except Exception as e:
#         logger.error(f"Error saving users: {e}")

# # Generate a unique UUID using a random salt
# def generate_uuid(username, password):
#     salt = secrets.token_hex(16)
#     combined = f"{username}:{password}:{salt}"
#     hash_obj = hashlib.sha256(combined.encode())
#     user_id = hash_obj.hexdigest()
#     logger.debug(f"Generated UUID for {username}: {user_id}")
#     return user_id, salt

# def load_user_history(user_id):
#     history_file = f"{HISTORY_DIR}/{user_id}.pkl"
#     logger.debug(f"Attempting to load history for user_id: {user_id}, file: {history_file}")
#     if os.path.exists(history_file):
#         try:
#             with open(history_file, "rb") as f:
#                 history = pickle.load(f)
#                 if not history or not isinstance(history, list) or not all(isinstance(chat, dict) and 'topic' in chat and 'messages' in chat for chat in history):
#                     logger.warning(f"Invalid history format for {user_id}. Converting to default structure.")
#                     return [{"topic": "Default Chat", "messages": history if isinstance(history, list) else []}]
#                 return history
#         except (pickle.UnpicklingError, EOFError, Exception) as e:
#             logger.error(f"Error loading history for {user_id}: {e}. Creating new history.")
#             return [{"topic": "Default Chat", "messages": []}]
#     logger.debug(f"No history file found for {user_id}. Initializing empty history.")
#     return [{"topic": "Default Chat", "messages": []}]

# def save_user_history(user_id, history):
#     history_file = f"{HISTORY_DIR}/{user_id}.pkl"
#     try:
#         with open(history_file, "wb") as f:
#             pickle.dump(history, f)
#         logger.debug(f"Successfully saved history for user_id: {user_id} to {history_file}")
#     except Exception as e:
#         logger.error(f"Error saving history for {user_id}: {e}")

# @app.route("/api/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     username = data.get("username")
#     password = data.get("password")

#     if not username or not password:
#         return jsonify({"error": "Username and password are required"}), 400

#     users = load_users()
#     if username not in users:
#         user_id, salt = generate_uuid(username, password)
#         users[username] = {"user_id": user_id, "salt": salt}
#         save_users(users)
#         logger.debug(f"New user {username} registered with user_id: {user_id}")
#     else:
#         user_id = users[username]["user_id"]
#         logger.debug(f"Existing user {username} found with user_id: {user_id}")

#     history = load_user_history(user_id)
#     if not history or not all('topic' in chat for chat in history):
#         history = [{"topic": "Default Chat", "messages": []}]
#     return jsonify({"user_id": user_id, "username": username, "history": history})

# @app.route("/api/transcribe", methods=["POST"])
# def transcribe():
#     logger.debug("Received request for /api/transcribe")
#     if 'audio' not in request.files or not request.form.get("user_id"):
#         logger.error("Missing audio or user_id")
#         return jsonify({"error": "Audio file and user_id are required"}), 400

#     audio_file = request.files['audio']
#     user_id = request.form.get("user_id")
#     logger.debug(f"Processing audio for user_id: {user_id}, filename: {audio_file.filename}")

#     try:
#         # Save audio blob to temporary WAV file
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
#             audio_file.save(f.name)
#             temp_audio_path = f.name

#         # Verify file is readable
#         with open(temp_audio_path, 'rb') as f:
#             header = f.read(44)  # WAV header size
#             if not header.startswith(b'RIFF') or b'WAVE' not in header:
#                 logger.error("Invalid WAV file")
#                 return jsonify({"error": "Invalid audio format, expected WAV"}), 400

#         # Read WAV file
#         sample_rate, audio_data = read(temp_audio_path)
#         if sample_rate != 16000:
#             logger.warning(f"Audio sample rate {sample_rate} != 16000, may affect transcription quality")
        
#         # Transcribe audio
#         result = asr_pipeline(temp_audio_path)
#         transcription = result.get("text", "").strip()
#         if not transcription:
#             logger.error("No transcription received")
#             return jsonify({"error": "No speech detected in audio"}), 400

#         logger.debug(f"Transcription: {transcription}")
#         return jsonify({"transcription": transcription, "user_id": user_id})
#     except Exception as e:
#         logger.error(f"Error in transcription for user_id {user_id}: {e}")
#         return jsonify({"error": f"Transcription failed: {str(e)}"}), 500
#     finally:
#         if os.path.exists(temp_audio_path):
#             os.remove(temp_audio_path)

# @app.route("/api/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     prompt = data.get("prompt")
#     user_id = data.get("user_id")

#     if not prompt or not user_id:
#         return jsonify({"error": "Prompt and user_id are required"}), 400

#     history = load_user_history(user_id)
#     if not history:
#         history = [{"topic": "Default Chat", "messages": []}]
    
#     current_chat = history[-1]
#     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
#         current_chat = {"topic": f"Chat {len(history)}", "messages": []}
#         history.append(current_chat)
    
#     current_chat["messages"].append({"role": "user", "content": prompt})

#     try:
#         docs = vectorstore.similarity_search(prompt, k=3)
#         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
#         full_context = "\n".join([msg["content"] for msg in current_chat["messages"]]) + "\n\n" + context
#         response = generate_response(groq_client, prompt, full_context, Config.MODEL_NAME)
#         if not response or not isinstance(response, str):
#             raise ValueError("Invalid response from Groq API")
#     except Exception as e:
#         logger.error(f"Error in chat generation for user_id {user_id}: {e}")
#         response = f"Error generating response: {str(e)}"

#     current_chat["messages"].append({"role": "assistant", "content": response})
#     save_user_history(user_id, history)
#     return jsonify({"response": response, "user_id": user_id})

# @app.route("/api/general_diagnosis", methods=["POST"])
# def general_diagnosis():
#     data = request.get_json()
#     prompt = data.get("prompt")
#     user_id = data.get("user_id")

#     if not prompt or not user_id:
#         return jsonify({"error": "Prompt and user_id are required"}), 400

#     history = load_user_history(user_id)
#     if not history:
#         history = [{"topic": "General Diagnosis", "messages": []}]
    
#     current_chat = history[-1]
#     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
#         current_chat = {"topic": "General Diagnosis", "messages": []}
#         history.append(current_chat)
    
#     current_chat["messages"].append({"role": "user", "content": prompt})

#     try:
#         docs = vectorstore.similarity_search(prompt, k=3)
#         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
#         full_context = "\n".join([msg["content"] for msg in current_chat["messages"]]) + "\n\n" + context
#         diagnosis_prompt = (
#             f"Act as a medical assistant. Based on the symptoms described: '{prompt}', "
#             "provide a structured response with sections for Symptoms, Causes, and Remedies. "
#             "If the information is insufficient or ambiguous, state that a definitive diagnosis cannot be made "
#             "and recommend consulting a healthcare professional."
#         )
#         response = generate_response(groq_client, diagnosis_prompt, full_context, Config.MODEL_NAME)
#         if not response or not isinstance(response, str):
#             raise ValueError("Invalid response from Groq API")
#     except Exception as e:
#         logger.error(f"Error in general diagnosis for user_id {user_id}: {e}")
#         response = f"Error generating response: {str(e)}"

#     current_chat["messages"].append({"role": "assistant", "content": response})
#     save_user_history(user_id, history)
#     return jsonify({"response": response, "user_id": user_id})

# @app.route("/api/report_analyzer", methods=["POST"])
# def report_analyzer():
#     logger.debug(f"Received request for /api/report_analyzer")
#     if 'file' not in request.files or not request.form.get("user_id"):
#         logger.error("Missing file or user_id")
#         return jsonify({"error": "PDF file and user_id are required"}), 400

#     file = request.files['file']
#     user_id = request.form.get("user_id")
#     logger.debug(f"Processing report for user_id: {user_id}, filename: {file.filename}")

#     if not file.filename.endswith('.pdf'):
#         logger.error(f"Invalid file type: {file.filename}")
#         return jsonify({"error": "Only PDF files are supported"}), 400

#     file.seek(0, os.SEEK_END)
#     file_size = file.tell()
#     if file_size > 10 * 1024 * 1024:
#         logger.error(f"File size exceeds limit: {file_size} bytes")
#         return jsonify({"error": "File size exceeds 10MB limit"}), 400
#     file.seek(0)

#     history = load_user_history(user_id)
#     if not history:
#         history = [{"topic": "Report Analysis", "messages": []}]
    
#     current_chat = history[-1]
#     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
#         current_chat = {"topic": "Report Analysis", "messages": []}
#         history.append(current_chat)
    
#     current_chat["messages"].append({"role": "system", "content": "User uploaded a medical report for analysis"})

#     try:
#         pdf_reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page in pdf_reader.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
        
#         if not text.strip():
#             logger.error("No text extracted from PDF")
#             raise ValueError("No text could be extracted from the PDF")

#         logger.debug(f"Extracted text (first 100 chars): {text[:100]}")
#         text = text[:5000]
        
#         docs = vectorstore.similarity_search(text, k=3)
#         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
#         full_context = text + "\n\n" + context
#         analysis_prompt = (
#             "Act as a medical assistant. Analyze the following medical report content: "
#             f"'{text[:1000]}' (truncated for brevity). "
#             "Provide a summary of key findings, such as diagnoses, test results, or recommendations. "
#             "Structure the response with sections for Key Findings and Recommendations. "
#             "If the content is unclear or insufficient, state that analysis is limited and recommend consulting a healthcare professional."
#         )
#         response = generate_response(groq_client, analysis_prompt, full_context, Config.MODEL_NAME)
#         if not response or not isinstance(response, str):
#             raise ValueError("Invalid response from Groq API")
#     except Exception as e:
#         logger.error(f"Error in report analysis for user_id {user_id}: {e}")
#         response = f"Error processing report: {str(e)}"

#     current_chat["messages"].append({"role": "assistant", "content": response})
#     save_user_history(user_id, history)
#     logger.debug(f"Report analysis completed for user_id: {user_id}")
#     return jsonify({"response": response, "user_id": user_id})

# @app.route("/api/prescription_reader", methods=["POST"])
# def prescription_reader():
#     logger.debug(f"Received request for /api/prescription_reader")
#     if 'image' not in request.files or not request.form.get("user_id"):
#         logger.error("Missing image or user_id")
#         return jsonify({"error": "Image file and user_id are required"}), 400

#     file = request.files['image']
#     user_id = request.form.get("user_id")
#     logger.debug(f"Processing prescription for user_id: {user_id}, filename: {file.filename}")

#     if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#         logger.error(f"Invalid file type: {file.filename}")
#         return jsonify({"error": "Only PNG, JPG, or JPEG images are supported"}), 400

#     history = load_user_history(user_id)
#     if not history:
#         history = [{"topic": "Prescription Reading", "messages": []}]
    
#     current_chat = history[-1]
#     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
#         current_chat = {"topic": "Prescription Reading", "messages": []}
#         history.append(current_chat)
    
#     current_chat["messages"].append({"role": "system", "content": "User uploaded a prescription image for reading"})

#     try:
#         image = Image.open(file)
#         image = image.convert('L')
#         text = pytesseract.image_to_string(image, lang='eng')
        
#         if not text.strip():
#             logger.error("No text extracted from image")
#             raise ValueError("No text could be extracted from the image")

#         logger.debug(f"Extracted text (first 100 chars): {text[:100]}")
#         text = text[:5000]
        
#         docs = vectorstore.similarity_search(text, k=3)
#         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
#         full_context = text + "\n\n" + context
#         prescription_prompt = (
#             "Act as a medical assistant. Analyze the following prescription text: "
#             f"'{text[:1000]}' (truncated for brevity). "
#             "Extract key details such as medications, dosages, and instructions. "
#             "Structure the response with sections for Medications and Instructions. "
#             "If the text is unclear or insufficient, state that analysis is limited and recommend consulting a pharmacist or healthcare professional."
#         )
#         response = generate_response(groq_client, prescription_prompt, full_context, Config.MODEL_NAME)
#         if not response or not isinstance(response, str):
#             raise ValueError("Invalid response from Groq API")
#     except Exception as e:
#         logger.error(f"Error in prescription reading for user_id {user_id}: {e}")
#         response = f"Error processing prescription: {str(e)}"

#     current_chat["messages"].append({"role": "assistant", "content": response})
#     save_user_history(user_id, history)
#     logger.debug(f"Prescription reading completed for user_id: {user_id}")
#     return jsonify({"response": response, "user_id": user_id})

# @app.route("/api/delete_message", methods=["POST"])
# def delete_message():
#     data = request.get_json()
#     user_id = data.get("user_id")
#     chat_index = data.get("chat_index")
#     message_index = data.get("message_index")

#     if not user_id or chat_index is None or message_index is None:
#         return jsonify({"error": "user_id, chat_index, and message_index are required"}), 400

#     history = load_user_history(user_id)
#     if not history or chat_index >= len(history):
#         return jsonify({"error": "Invalid chat index"}), 400

#     if message_index >= len(history[chat_index]["messages"]):
#         return jsonify({"error": "Invalid message index"}), 400

#     history[chat_index]["messages"].pop(message_index)
#     save_user_history(user_id, history)
#     logger.debug(f"Deleted message {message_index} from chat {chat_index} for user_id: {user_id}")
#     return jsonify({"message": "Message deleted successfully"})

# @app.route("/api/delete_chat", methods=["POST"])
# def delete_chat():
#     data = request.get_json()
#     user_id = data.get("user_id")
#     chat_index = data.get("chat_index")

#     if not user_id or chat_index is None:
#         return jsonify({"error": "user_id and chat_index are required"}), 400

#     history = load_user_history(user_id)
#     if not history or chat_index >= len(history):
#         return jsonify({"error": "Invalid chat index"}), 400

#     history.pop(chat_index)
#     save_user_history(user_id, history)
#     logger.debug(f"Deleted chat {chat_index} for user_id: {user_id}")
#     return jsonify({"message": "Chat deleted successfully"})

# @app.route("/api/edit_message", methods=["POST"])
# def edit_message():
#     data = request.get_json()
#     user_id = data.get("user_id")
#     chat_index = data.get("chat_index")
#     message_index = data.get("message_index")
#     new_content = data.get("new_content")

#     if not user_id or chat_index is None or message_index is None or not isinstance(new_content, str):
#         return jsonify({"error": "user_id, chat_index, message_index, and new_content (string) are required"}), 400

#     if not new_content.strip() or len(new_content) > 10000:
#         return jsonify({"error": "new_content must be non-empty and less than 10,000 characters"}), 400

#     history = load_user_history(user_id)
#     if not history or chat_index >= len(history):
#         return jsonify({"error": "Invalid chat index"}), 400

#     if message_index >= len(history[chat_index]["messages"]):
#         return jsonify({"error": "Invalid message index"}), 400

#     history[chat_index]["messages"][message_index]["content"] = new_content.strip()
#     save_user_history(user_id, history)
#     logger.debug(f"Edited message {message_index} in chat {chat_index} for user_id: {user_id}")
#     return jsonify({"message": "Message edited successfully"})

# @app.route("/api/logout", methods=["POST"])
# def logout():
#     data = request.get_json()
#     user_id = data.get("user_id")
#     chat_history = data.get("chat_history", [])

#     if user_id:
#         if isinstance(chat_history, list) and all(isinstance(msg, dict) and 'role' in msg and 'content' in msg for msg in chat_history):
#             formatted_history = [{"topic": "Default Chat", "messages": chat_history}]
#         else:
#             formatted_history = chat_history if all(isinstance(chat, dict) and 'topic' in chat and 'messages' in chat for chat in chat_history) else [{"topic": "Default Chat", "messages": []}]
#         save_user_history(user_id, formatted_history)
#         logger.debug(f"Logout for user_id: {user_id}. History saved.")
#     return jsonify({"message": "Logged out successfully"})
# def get_calendar_service(user_id):
#     creds = None
#     token_path = f'token_{user_id}.json'
#     if os.path.exists(token_path):
#         creds = Credentials.from_authorized_user_file(token_path, SCOPES)
#     if not creds or not creds.valid:
#         flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
#         creds = flow.run_local_server(port=0)
#         with open(token_path, 'w') as token:
#             token.write(creds.to_json())
#     return build('calendar', 'v3', credentials=creds)

# @app.route("/api/google_login", methods=["POST"])
# def google_login():
#     user_id = request.form.get("user_id")
#     if not user_id:
#         return jsonify({"error": "User ID required"}), 400
#     flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
#     flow.redirect_uri = 'http://localhost:5000/callback'
#     authorization_url, _ = flow.authorization_response()
#     return jsonify({"auth_url": authorization_url})

# @app.route("/callback")
# def callback():
#     return jsonify({"message": "OAuth2 callback received, close this tab"})

# @app.route("/api/calendar", methods=["POST"])
# def create_calendar_event():
#     user_id = request.form.get("user_id")
#     summary = request.form.get("summary", "Medical Reminder")
#     start_time = request.form.get("start_time")  # ISO format: 2025-04-17T08:00:00
#     end_time = request.form.get("end_time")      # ISO format: 2025-04-17T08:30:00
#     if not all([user_id, start_time, end_time]):
#         logger.error("Missing calendar params")
#         return jsonify({"error": "Missing parameters"}), 400

#     try:
#         service = get_calendar_service(user_id)
#         event = {
#             'summary': summary,
#             'start': {'dateTime': start_time, 'timeZone': 'UTC'},
#             'end': {'dateTime': end_time, 'timeZone': 'UTC'},
#         }
#         event = service.events().insert(calendarId='primary', body=event).execute()
#         logger.debug(f"Event created: {event.get('htmlLink')}")
#         return jsonify({"message": "Event created", "link": event.get('htmlLink')})
#     except Exception as e:
#         logger.error(f"Calendar error: {e}")
#         return jsonify({"error": str(e)}), 500
    
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000) 
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from config import Config
# from utils.data_processing import load_and_process_data
# from utils.vector_store import create_vector_store
# from utils.groq_client import initialize_groq_client, generate_response
# import pickle
# import os
# import hashlib
# import logging
# import secrets
# import PyPDF2
# import pytesseract
# from PIL import Image
# import io
# from transformers import pipeline
# import tempfile
# from scipy.io.wavfile import write, read 
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# import datetime
# import numpy as np

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})
# SCOPES = ['https://www.googleapis.com/auth/calendar.events']
# CREDENTIALS_FILE = 'credentials.json' 

# # Load data and initialize components at startup
# try:
#     documents = load_and_process_data(Config.DATA_PATH)
#     vectorstore = create_vector_store(documents, Config.EMBEDDING_MODEL)
#     groq_client = initialize_groq_client(Config.GROQ_API_KEY)
#     # Initialize Whisper model for speech-to-text
#     logger.info("Loading Whisper model for speech-to-text...")
#     asr_pipeline = pipeline(
#         "automatic-speech-recognition",
#         model="openai/whisper-base",
#         chunk_length_s=2,
#         device=-1  # CPU; change to 0 for GPU
#     )
# except Exception as e:
#     logger.error(f"Failed to initialize components: {e}")
#     raise

# # Directories and files
# HISTORY_DIR = "history"
# USERS_FILE = "users.pkl"
# os.makedirs(HISTORY_DIR, exist_ok=True)

# # Load or initialize the users dictionary
# def load_users():
#     if os.path.exists(USERS_FILE):
#         try:
#             with open(USERS_FILE, "rb") as f:
#                 return pickle.load(f)
#         except Exception as e:
#             logger.error(f"Error loading users: {e}")
#             return {}
#     return {}

# def save_users(users):
#     try:
#         with open(USERS_FILE, "wb") as f:
#             pickle.dump(users, f)
#     except Exception as e:
#         logger.error(f"Error saving users: {e}")

# # Generate a unique UUID using a random salt
# def generate_uuid(username, password):
#     salt = secrets.token_hex(16)
#     combined = f"{username}:{password}:{salt}"
#     hash_obj = hashlib.sha256(combined.encode())
#     user_id = hash_obj.hexdigest()
#     logger.debug(f"Generated UUID for {username}: {user_id}")
#     return user_id, salt

# def load_user_history(user_id):
#     history_file = f"{HISTORY_DIR}/{user_id}.pkl"
#     logger.debug(f"Attempting to load history for user_id: {user_id}, file: {history_file}")
#     if os.path.exists(history_file):
#         try:
#             with open(history_file, "rb") as f:
#                 history = pickle.load(f)
#                 if not history or not isinstance(history, list) or not all(isinstance(chat, dict) and 'topic' in chat and 'messages' in chat for chat in history):
#                     logger.warning(f"Invalid history format for {user_id}. Converting to default structure.")
#                     return [{"topic": "Default Chat", "messages": history if isinstance(history, list) else []}]
#                 return history
#         except (pickle.UnpicklingError, EOFError, Exception) as e:
#             logger.error(f"Error loading history for {user_id}: {e}. Creating new history.")
#             return [{"topic": "Default Chat", "messages": []}]
#     logger.debug(f"No history file found for {user_id}. Initializing empty history.")
#     return [{"topic": "Default Chat", "messages": []}]

# def save_user_history(user_id, history):
#     history_file = f"{HISTORY_DIR}/{user_id}.pkl"
#     try:
#         with open(history_file, "wb") as f:
#             pickle.dump(history, f)
#         logger.debug(f"Successfully saved history for user_id: {user_id} to {history_file}")
#     except Exception as e:
#         logger.error(f"Error saving history for {user_id}: {e}")

# @app.route("/api/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     username = data.get("username")
#     password = data.get("password")

#     if not username or not password:
#         return jsonify({"error": "Username and password are required"}), 400

#     users = load_users()
#     if username not in users:
#         user_id, salt = generate_uuid(username, password)
#         users[username] = {"user_id": user_id, "salt": salt}
#         save_users(users)
#         logger.debug(f"New user {username} registered with user_id: {user_id}")
#     else:
#         user_id = users[username]["user_id"]
#         logger.debug(f"Existing user {username} found with user_id: {user_id}")

#     history = load_user_history(user_id)
#     if not history or not all('topic' in chat for chat in history):
#         history = [{"topic": "Default Chat", "messages": []}]
#     return jsonify({"user_id": user_id, "username": username, "history": history})

# @app.route("/api/transcribe", methods=["POST"])
# def transcribe():
#     logger.debug("Received request for /api/transcribe")
#     if 'audio' not in request.files or not request.form.get("user_id"):
#         logger.error("Missing audio or user_id")
#         return jsonify({"error": "Audio file and user_id are required"}), 400

#     audio_file = request.files['audio']
#     user_id = request.form.get("user_id")
#     logger.debug(f"Processing audio for user_id: {user_id}, filename: {audio_file.filename}")

#     try:
#         # Save audio blob to temporary WAV file
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
#             audio_file.save(f.name)
#             temp_audio_path = f.name

#         # Verify file is readable
#         with open(temp_audio_path, 'rb') as f:
#             header = f.read(44)  # WAV header size
#             if not header.startswith(b'RIFF') or b'WAVE' not in header:
#                 logger.error("Invalid WAV file")
#                 return jsonify({"error": "Invalid audio format, expected WAV"}), 400

#         # Read WAV file
#         sample_rate, audio_data = read(temp_audio_path)
#         if sample_rate != 16000:
#             logger.warning(f"Audio sample rate {sample_rate} != 16000, may affect transcription quality")
        
#         # Transcribe audio
#         result = asr_pipeline(temp_audio_path)
#         transcription = result.get("text", "").strip()
#         if not transcription:
#             logger.error("No transcription received")
#             return jsonify({"error": "No speech detected in audio"}), 400

#         logger.debug(f"Transcription: {transcription}")
#         return jsonify({"transcription": transcription, "user_id": user_id})
#     except Exception as e:
#         logger.error(f"Error in transcription for user_id {user_id}: {e}")
#         return jsonify({"error": f"Transcription failed: {str(e)}"}), 500
#     finally:
#         if os.path.exists(temp_audio_path):
#             os.remove(temp_audio_path)

# @app.route("/api/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     prompt = data.get("prompt")
#     user_id = data.get("user_id")

#     if not prompt or not user_id:
#         return jsonify({"error": "Prompt and user_id are required"}), 400

#     history = load_user_history(user_id)
#     if not history:
#         history = [{"topic": "Default Chat", "messages": []}]
    
#     current_chat = history[-1]
#     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
#         current_chat = {"topic": f"Chat {len(history)}", "messages": []}
#         history.append(current_chat)
    
#     current_chat["messages"].append({"role": "user", "content": prompt})

#     try:
#         docs = vectorstore.similarity_search(prompt, k=3)
#         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
#         full_context = "\n".join([msg["content"] for msg in current_chat["messages"]]) + "\n\n" + context
#         response = generate_response(groq_client, prompt, full_context, Config.MODEL_NAME)
#         if not response or not isinstance(response, str):
#             raise ValueError("Invalid response from Groq API")
#     except Exception as e:
#         logger.error(f"Error in chat generation for user_id {user_id}: {e}")
#         response = f"Error generating response: {str(e)}"

#     current_chat["messages"].append({"role": "assistant", "content": response})
#     save_user_history(user_id, history)
#     return jsonify({"response": response, "user_id": user_id})

# @app.route("/api/general_diagnosis", methods=["POST"])
# def general_diagnosis():
#     data = request.get_json()
#     prompt = data.get("prompt")
#     user_id = data.get("user_id")

#     if not prompt or not user_id:
#         return jsonify({"error": "Prompt and user_id are required"}), 400

#     history = load_user_history(user_id)
#     if not history:
#         history = [{"topic": "General Diagnosis", "messages": []}]
    
#     current_chat = history[-1]
#     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
#         current_chat = {"topic": "General Diagnosis", "messages": []}
#         history.append(current_chat)
    
#     current_chat["messages"].append({"role": "user", "content": prompt})

#     try:
#         docs = vectorstore.similarity_search(prompt, k=3)
#         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
#         full_context = "\n".join([msg["content"] for msg in current_chat["messages"]]) + "\n\n" + context
#         diagnosis_prompt = (
#             f"Act as a medical assistant. Based on the symptoms described: '{prompt}', "
#             "provide a structured response with sections for Symptoms, Causes, and Remedies. "
#             "If the information is insufficient or ambiguous, state that a definitive diagnosis cannot be made "
#             "and recommend consulting a healthcare professional. "
#             "If the prompt mentions a specific disease (e.g., 'diabetes', 'hypertension'), "
#             "append a video link at the end in the exact format '[Watch a video on <disease>](https://www.youtube.com/watch?v=<video_id>)' "
#             "using the following mappings: "
#             "'diabetes' -> 'https://www.youtube.com/watch?v=7B-0Kz5Q16w', "
#             "'hypertension' -> 'https://www.youtube.com/watch?v=5r66bS8q9Nk'."
#         )
#         response = generate_response(groq_client, diagnosis_prompt, full_context, Config.MODEL_NAME)
#         if not response or not isinstance(response, str):
#             raise ValueError("Invalid response from Groq API")
#     except Exception as e:
#         logger.error(f"Error in general diagnosis for user_id {user_id}: {e}")
#         response = f"Error generating response: {str(e)}"

#     current_chat["messages"].append({"role": "assistant", "content": response})
#     save_user_history(user_id, history)
#     return jsonify({"response": response, "user_id": user_id})

# @app.route("/api/report_analyzer", methods=["POST"])
# def report_analyzer():
#     logger.debug(f"Received request for /api/report_analyzer")
#     if 'file' not in request.files or not request.form.get("user_id"):
#         logger.error("Missing file or user_id")
#         return jsonify({"error": "PDF file and user_id are required"}), 400

#     file = request.files['file']
#     user_id = request.form.get("user_id")
#     logger.debug(f"Processing report for user_id: {user_id}, filename: {file.filename}")

#     if not file.filename.endswith('.pdf'):
#         logger.error(f"Invalid file type: {file.filename}")
#         return jsonify({"error": "Only PDF files are supported"}), 400

#     file.seek(0, os.SEEK_END)
#     file_size = file.tell()
#     if file_size > 10 * 1024 * 1024:
#         logger.error(f"File size exceeds limit: {file_size} bytes")
#         return jsonify({"error": "File size exceeds 10MB limit"}), 400
#     file.seek(0)

#     history = load_user_history(user_id)
#     if not history:
#         history = [{"topic": "Report Analysis", "messages": []}]
    
#     current_chat = history[-1]
#     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
#         current_chat = {"topic": "Report Analysis", "messages": []}
#         history.append(current_chat)
    
#     current_chat["messages"].append({"role": "system", "content": "User uploaded a medical report for analysis"})

#     try:
#         pdf_reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page in pdf_reader.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
        
#         if not text.strip():
#             logger.error("No text extracted from PDF")
#             raise ValueError("No text could be extracted from the PDF")

#         logger.debug(f"Extracted text (first 100 chars): {text[:100]}")
#         text = text[:5000]
        
#         docs = vectorstore.similarity_search(text, k=3)
#         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
#         full_context = text + "\n\n" + context
#         analysis_prompt = (
#             "Act as a medical assistant. Analyze the following medical report content: "
#             f"'{text[:1000]}' (truncated for brevity). "
#             "Provide a summary of key findings, such as diagnoses, test results, or recommendations. "
#             "Structure the response with sections for Key Findings and Recommendations. "
#             "If the content is unclear or insufficient, state that analysis is limited and recommend consulting a healthcare professional."
#         )
#         response = generate_response(groq_client, analysis_prompt, full_context, Config.MODEL_NAME)
#         if not response or not isinstance(response, str):
#             raise ValueError("Invalid response from Groq API")
#     except Exception as e:
#         logger.error(f"Error in report analysis for user_id {user_id}: {e}")
#         response = f"Error processing report: {str(e)}"

#     current_chat["messages"].append({"role": "assistant", "content": response})
#     save_user_history(user_id, history)
#     logger.debug(f"Report analysis completed for user_id: {user_id}")
#     return jsonify({"response": response, "user_id": user_id})

# @app.route("/api/prescription_reader", methods=["POST"])
# def prescription_reader():
#     logger.debug(f"Received request for /api/prescription_reader")
#     if 'image' not in request.files or not request.form.get("user_id"):
#         logger.error("Missing image or user_id")
#         return jsonify({"error": "Image file and user_id are required"}), 400

#     file = request.files['image']
#     user_id = request.form.get("user_id")
#     logger.debug(f"Processing prescription for user_id: {user_id}, filename: {file.filename}")

#     if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#         logger.error(f"Invalid file type: {file.filename}")
#         return jsonify({"error": "Only PNG, JPG, or JPEG images are supported"}), 400

#     history = load_user_history(user_id)
#     if not history:
#         history = [{"topic": "Prescription Reading", "messages": []}]
    
#     current_chat = history[-1]
#     if not isinstance(current_chat, dict) or 'messages' not in current_chat:
#         current_chat = {"topic": "Prescription Reading", "messages": []}
#         history.append(current_chat)
    
#     current_chat["messages"].append({"role": "system", "content": "User uploaded a prescription image for reading"})

#     try:
#         image = Image.open(file)
#         image = image.convert('L')
#         text = pytesseract.image_to_string(image, lang='eng')
        
#         if not text.strip():
#             logger.error("No text extracted from image")
#             raise ValueError("No text could be extracted from the image")

#         logger.debug(f"Extracted text (first 100 chars): {text[:100]}")
#         text = text[:5000]
        
#         docs = vectorstore.similarity_search(text, k=3)
#         context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
#         full_context = text + "\n\n" + context
#         prescription_prompt = (
#             "Act as a medical assistant. Analyze the following prescription text: "
#             f"'{text[:1000]}' (truncated for brevity). "
#             "Extract key details such as medications, dosages, and instructions. "
#             "Structure the response with sections for Medications and Instructions. "
#             "If the text is unclear or insufficient, state that analysis is limited and recommend consulting a pharmacist or healthcare professional."
#         )
#         response = generate_response(groq_client, prescription_prompt, full_context, Config.MODEL_NAME)
#         if not response or not isinstance(response, str):
#             raise ValueError("Invalid response from Groq API")
#     except Exception as e:
#         logger.error(f"Error in prescription reading for user_id {user_id}: {e}")
#         response = f"Error processing prescription: {str(e)}"

#     current_chat["messages"].append({"role": "assistant", "content": response})
#     save_user_history(user_id, history)
#     logger.debug(f"Prescription reading completed for user_id: {user_id}")
#     return jsonify({"response": response, "user_id": user_id})

# @app.route("/api/delete_message", methods=["POST"])
# def delete_message():
#     data = request.get_json()
#     user_id = data.get("user_id")
#     chat_index = data.get("chat_index")
#     message_index = data.get("message_index")

#     if not user_id or chat_index is None or message_index is None:
#         return jsonify({"error": "user_id, chat_index, and message_index are required"}), 400

#     history = load_user_history(user_id)
#     if not history or chat_index >= len(history):
#         return jsonify({"error": "Invalid chat index"}), 400

#     if message_index >= len(history[chat_index]["messages"]):
#         return jsonify({"error": "Invalid message index"}), 400

#     history[chat_index]["messages"].pop(message_index)
#     save_user_history(user_id, history)
#     logger.debug(f"Deleted message {message_index} from chat {chat_index} for user_id: {user_id}")
#     return jsonify({"message": "Message deleted successfully"})

# @app.route("/api/delete_chat", methods=["POST"])
# def delete_chat():
#     data = request.get_json()
#     user_id = data.get("user_id")
#     chat_index = data.get("chat_index")

#     if not user_id or chat_index is None:
#         return jsonify({"error": "user_id and chat_index are required"}), 400

#     history = load_user_history(user_id)
#     if not history or chat_index >= len(history):
#         return jsonify({"error": "Invalid chat index"}), 400

#     history.pop(chat_index)
#     save_user_history(user_id, history)
#     logger.debug(f"Deleted chat {chat_index} for user_id: {user_id}")
#     return jsonify({"message": "Chat deleted successfully"})

# @app.route("/api/edit_message", methods=["POST"])
# def edit_message():
#     data = request.get_json()
#     user_id = data.get("user_id")
#     chat_index = data.get("chat_index")
#     message_index = data.get("message_index")
#     new_content = data.get("new_content")

#     if not user_id or chat_index is None or message_index is None or not isinstance(new_content, str):
#         return jsonify({"error": "user_id, chat_index, message_index, and new_content (string) are required"}), 400

#     if not new_content.strip() or len(new_content) > 10000:
#         return jsonify({"error": "new_content must be non-empty and less than 10,000 characters"}), 400

#     history = load_user_history(user_id)
#     if not history or chat_index >= len(history):
#         return jsonify({"error": "Invalid chat index"}), 400

#     if message_index >= len(history[chat_index]["messages"]):
#         return jsonify({"error": "Invalid message index"}), 400

#     history[chat_index]["messages"][message_index]["content"] = new_content.strip()
#     save_user_history(user_id, history)
#     logger.debug(f"Edited message {message_index} in chat {chat_index} for user_id: {user_id}")
#     return jsonify({"message": "Message edited successfully"})

# @app.route("/api/logout", methods=["POST"])
# def logout():
#     data = request.get_json()
#     user_id = data.get("user_id")
#     chat_history = data.get("chat_history", [])

#     if user_id:
#         if isinstance(chat_history, list) and all(isinstance(msg, dict) and 'role' in msg and 'content' in msg for msg in chat_history):
#             formatted_history = [{"topic": "Default Chat", "messages": chat_history}]
#         else:
#             formatted_history = chat_history if all(isinstance(chat, dict) and 'topic' in chat and 'messages' in chat for chat in chat_history) else [{"topic": "Default Chat", "messages": []}]
#         save_user_history(user_id, formatted_history)
#         logger.debug(f"Logout for user_id: {user_id}. History saved.")
#     return jsonify({"message": "Logged out successfully"})
# def get_calendar_service(user_id):
#     creds = None
#     token_path = f'token_{user_id}.json'
#     if os.path.exists(token_path):
#         creds = Credentials.from_authorized_user_file(token_path, SCOPES)
#     if not creds or not creds.valid:
#         flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
#         creds = flow.run_local_server(port=0)
#         with open(token_path, 'w') as token:
#             token.write(creds.to_json())
#     return build('calendar', 'v3', credentials=creds)

# @app.route("/api/google_login", methods=["POST"])
# def google_login():
#     user_id = request.form.get("user_id")
#     if not user_id:
#         return jsonify({"error": "User ID required"}), 400
#     flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
#     flow.redirect_uri = 'http://localhost:5000/callback'
#     authorization_url, _ = flow.authorization_response()
#     return jsonify({"auth_url": authorization_url})

# @app.route("/callback")
# def callback():
#     return jsonify({"message": "OAuth2 callback received, close this tab"})

# @app.route("/api/calendar", methods=["POST"])
# def create_calendar_event():
#     user_id = request.form.get("user_id")
#     summary = request.form.get("summary", "Medical Reminder")
#     start_time = request.form.get("start_time")  # ISO format: 2025-04-17T08:00:00
#     end_time = request.form.get("end_time")      # ISO format: 2025-04-17T08:30:00
#     if not all([user_id, start_time, end_time]):
#         logger.error("Missing calendar params")
#         return jsonify({"error": "Missing parameters"}), 400

#     try:
#         service = get_calendar_service(user_id)
#         event = {
#             'summary': summary,
#             'start': {'dateTime': start_time, 'timeZone': 'UTC'},
#             'end': {'dateTime': end_time, 'timeZone': 'UTC'},
#         }
#         event = service.events().insert(calendarId='primary', body=event).execute()
#         logger.debug(f"Event created: {event.get('htmlLink')}")
#         return jsonify({"message": "Event created", "link": event.get('htmlLink')})
#     except Exception as e:
#         logger.error(f"Calendar error: {e}")
#         return jsonify({"error": str(e)}), 500
    
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000) 
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from utils.data_processing import load_and_process_data
from utils.vector_store import create_vector_store
from utils.groq_client import initialize_groq_client, generate_response
import pickle
import os
import hashlib
import logging
import secrets
import PyPDF2
import pytesseract
from PIL import Image
import io
from transformers import pipeline
import tempfile
from scipy.io.wavfile import write, read
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import numpy as np

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CREDENTIALS_FILE = 'credentials.json'

# Load data and initialize components at startup
try:
    documents = load_and_process_data(Config.DATA_PATH)
    vectorstore = create_vector_store(documents, Config.EMBEDDING_MODEL)
    groq_client = initialize_groq_client(Config.GROQ_API_KEY)
    # Initialize Whisper model for speech-to-text
    logger.info("Loading Whisper model for speech-to-text...")
    asr_pipeline = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-base",
        chunk_length_s=2,
        device=-1  # CPU; change to 0 for GPU
    )
except Exception as e:
    logger.error(f"Failed to initialize components: {e}")
    raise

# Directories and files
HISTORY_DIR = "history"
USERS_FILE = "users.pkl"
os.makedirs(HISTORY_DIR, exist_ok=True)

# Load or initialize the users dictionary
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            return {}
    return {}

def save_users(users):
    try:
        with open(USERS_FILE, "wb") as f:
            pickle.dump(users, f)
    except Exception as e:
        logger.error(f"Error saving users: {e}")

# Generate a unique UUID using a random salt
def generate_uuid(username, password):
    salt = secrets.token_hex(16)
    combined = f"{username}:{password}:{salt}"
    hash_obj = hashlib.sha256(combined.encode())
    user_id = hash_obj.hexdigest()
    logger.debug(f"Generated UUID for {username}: {user_id}")
    return user_id, salt

def load_user_history(user_id):
    history_file = f"{HISTORY_DIR}/{user_id}.pkl"
    logger.debug(f"Attempting to load history for user_id: {user_id}, file: {history_file}")
    if os.path.exists(history_file):
        try:
            with open(history_file, "rb") as f:
                history = pickle.load(f)
                if not history or not isinstance(history, list) or not all(isinstance(chat, dict) and 'topic' in chat and 'messages' in chat for chat in history):
                    logger.warning(f"Invalid history format for {user_id}. Converting to default structure.")
                    return [{"topic": "Default Chat", "messages": history if isinstance(history, list) else []}]
                return history
        except (pickle.UnpicklingError, EOFError, Exception) as e:
            logger.error(f"Error loading history for {user_id}: {e}. Creating new history.")
            return [{"topic": "Default Chat", "messages": []}]
    logger.debug(f"No history file found for {user_id}. Initializing empty history.")
    return [{"topic": "Default Chat", "messages": []}]

def save_user_history(user_id, history):
    history_file = f"{HISTORY_DIR}/{user_id}.pkl"
    try:
        with open(history_file, "wb") as f:
            pickle.dump(history, f)
        logger.debug(f"Successfully saved history for user_id: {user_id} to {history_file}")
    except Exception as e:
        logger.error(f"Error saving history for {user_id}: {e}")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    users = load_users()
    if username not in users:
        user_id, salt = generate_uuid(username, password)
        users[username] = {"user_id": user_id, "salt": salt}
        save_users(users)
        logger.debug(f"New user {username} registered with user_id: {user_id}")
    else:
        user_id = users[username]["user_id"]
        logger.debug(f"Existing user {username} found with user_id: {user_id}")

    history = load_user_history(user_id)
    if not history or not all('topic' in chat for chat in history):
        history = [{"topic": "Default Chat", "messages": []}]
    return jsonify({"user_id": user_id, "username": username, "history": history})

@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    logger.debug("Received request for /api/transcribe")
    if 'audio' not in request.files or not request.form.get("user_id"):
        logger.error("Missing audio or user_id")
        return jsonify({"error": "Audio file and user_id are required"}), 400

    audio_file = request.files['audio']
    user_id = request.form.get("user_id")
    logger.debug(f"Processing audio for user_id: {user_id}, filename: {audio_file.filename}")

    try:
        # Save audio blob to temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            audio_file.save(f.name)
            temp_audio_path = f.name

        # Verify file is readable
        with open(temp_audio_path, 'rb') as f:
            header = f.read(44)  # WAV header size
            if not header.startswith(b'RIFF') or b'WAVE' not in header:
                logger.error("Invalid WAV file")
                return jsonify({"error": "Invalid audio format, expected WAV"}), 400

        # Read WAV file
        sample_rate, audio_data = read(temp_audio_path)
        if sample_rate != 16000:
            logger.warning(f"Audio sample rate {sample_rate} != 16000, may affect transcription quality")
       
        # Transcribe audio
        result = asr_pipeline(temp_audio_path)
        transcription = result.get("text", "").strip()
        if not transcription:
            logger.error("No transcription received")
            return jsonify({"error": "No speech detected in audio"}), 400

        logger.debug(f"Transcription: {transcription}")
        return jsonify({"transcription": transcription, "user_id": user_id})
    except Exception as e:
        logger.error(f"Error in transcription for user_id {user_id}: {e}")
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500
    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt")
    user_id = data.get("user_id")

    if not prompt or not user_id:
        return jsonify({"error": "Prompt and user_id are required"}), 400

    history = load_user_history(user_id)
    if not history:
        history = [{"topic": "Default Chat", "messages": []}]
   
    current_chat = history[-1]
    if not isinstance(current_chat, dict) or 'messages' not in current_chat:
        current_chat = {"topic": f"Chat {len(history)}", "messages": []}
        history.append(current_chat)
   
    current_chat["messages"].append({"role": "user", "content": prompt})

    try:
        docs = vectorstore.similarity_search(prompt, k=3)
        context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
        full_context = "\n".join([msg["content"] for msg in current_chat["messages"]]) + "\n\n" + context
        response = generate_response(
            groq_client,
            prompt,
            full_context,
            Config.MODEL_NAME,
            youtube_api_key=Config.YOUTUBE_API_KEY  # Pass YouTube API key
        )
        if not response or not isinstance(response, str):
            raise ValueError("Invalid response from Groq API")
    except Exception as e:
        logger.error(f"Error in chat generation for user_id {user_id}: {e}")
        response = f"Error generating response: {str(e)}"

    current_chat["messages"].append({"role": "assistant", "content": response})
    save_user_history(user_id, history)
    return jsonify({"response": response, "user_id": user_id})

@app.route("/api/general_diagnosis", methods=["POST"])
def general_diagnosis():
    data = request.get_json()
    prompt = data.get("prompt")
    user_id = data.get("user_id")

    if not prompt or not user_id:
        return jsonify({"error": "Prompt and user_id are required"}), 400

    history = load_user_history(user_id)
    if not history:
        history = [{"topic": "General Diagnosis", "messages": []}]
   
    current_chat = history[-1]
    if not isinstance(current_chat, dict) or 'messages' not in current_chat:
        current_chat = {"topic": "General Diagnosis", "messages": []}
        history.append(current_chat)
   
    current_chat["messages"].append({"role": "user", "content": prompt})

    try:
        docs = vectorstore.similarity_search(prompt, k=3)
        context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
        full_context = "\n".join([msg["content"] for msg in current_chat["messages"]]) + "\n\n" + context
        diagnosis_prompt = (
            f"Act as a medical assistant. Based on the symptoms described: '{prompt}', "
            "provide a structured response with sections for Symptoms, Causes, and Remedies. "
            "If the information is insufficient or ambiguous, state that a definitive diagnosis cannot be made "
            "and recommend consulting a healthcare professional. "
            "If the prompt mentions a specific disease (e.g., 'diabetes', 'hypertension'), "
            "append a video link at the end in the exact format '[Watch a video on <disease>](https://www.youtube.com/watch?v=<video_id>)' "
            "using the following mappings: "
            "'diabetes' -> 'https://www.youtube.com/watch?v=7B-0Kz5Q16w', "
            "'hypertension' -> 'https://www.youtube.com/watch?v=5r66bS8q9Nk'."
        )
        response = generate_response(
            groq_client,
            diagnosis_prompt,
            full_context,
            Config.MODEL_NAME,
            youtube_api_key=Config.YOUTUBE_API_KEY  # Pass YouTube API key
        )
        if not response or not isinstance(response, str):
            raise ValueError("Invalid response from Groq API")
    except Exception as e:
        logger.error(f"Error in general diagnosis for user_id {user_id}: {e}")
        response = f"Error generating response: {str(e)}"

    current_chat["messages"].append({"role": "assistant", "content": response})
    save_user_history(user_id, history)
    return jsonify({"response": response, "user_id": user_id})

@app.route("/api/report_analyzer", methods=["POST"])
def report_analyzer():
    logger.debug(f"Received request for /api/report_analyzer")
    if 'file' not in request.files or not request.form.get("user_id"):
        logger.error("Missing file or user_id")
        return jsonify({"error": "PDF file and user_id are required"}), 400

    file = request.files['file']
    user_id = request.form.get("user_id")
    logger.debug(f"Processing report for user_id: {user_id}, filename: {file.filename}")

    if not file.filename.endswith('.pdf'):
        logger.error(f"Invalid file type: {file.filename}")
        return jsonify({"error": "Only PDF files are supported"}), 400

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    if file_size > 10 * 1024 * 1024:
        logger.error(f"File size exceeds limit: {file_size} bytes")
        return jsonify({"error": "File size exceeds 10MB limit"}), 400
    file.seek(0)

    history = load_user_history(user_id)
    if not history:
        history = [{"topic": "Report Analysis", "messages": []}]
   
    current_chat = history[-1]
    if not isinstance(current_chat, dict) or 'messages' not in current_chat:
        current_chat = {"topic": "Report Analysis", "messages": []}
        history.append(current_chat)
   
    current_chat["messages"].append({"role": "system", "content": "User uploaded a medical report for analysis"})

    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
       
        if not text.strip():
            logger.error("No text extracted from PDF")
            raise ValueError("No text could be extracted from the PDF")

        logger.debug(f"Extracted text (first 100 chars): {text[:100]}")
        text = text[:5000]
       
        docs = vectorstore.similarity_search(text, k=3)
        context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
        full_context = text + "\n\n" + context
        analysis_prompt = (
            "Act as a medical assistant. Analyze the following medical report content: "
            f"'{text[:1000]}' (truncated for brevity). "
            "Provide a summary of key findings, such as diagnoses, test results, or recommendations. "
            "Structure the response with sections for Key Findings and Recommendations. "
            "If the content is unclear or insufficient, state that analysis is limited and recommend consulting a healthcare professional."
        )
        response = generate_response(groq_client, analysis_prompt, full_context, Config.MODEL_NAME)
        if not response or not isinstance(response, str):
            raise ValueError("Invalid response from Groq API")
    except Exception as e:
        logger.error(f"Error in report analysis for user_id {user_id}: {e}")
        response = f"Error processing report: {str(e)}"

    current_chat["messages"].append({"role": "assistant", "content": response})
    save_user_history(user_id, history)
    logger.debug(f"Report analysis completed for user_id: {user_id}")
    return jsonify({"response": response, "user_id": user_id})

@app.route("/api/prescription_reader", methods=["POST"])
def prescription_reader():
    logger.debug(f"Received request for /api/prescription_reader")
    if 'image' not in request.files or not request.form.get("user_id"):
        logger.error("Missing image or user_id")
        return jsonify({"error": "Image file and user_id are required"}), 400

    file = request.files['image']
    user_id = request.form.get("user_id")
    logger.debug(f"Processing prescription for user_id: {user_id}, filename: {file.filename}")

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        logger.error(f"Invalid file type: {file.filename}")
        return jsonify({"error": "Only PNG, JPG, or JPEG images are supported"}), 400

    history = load_user_history(user_id)
    if not history:
        history = [{"topic": "Prescription Reading", "messages": []}]
   
    current_chat = history[-1]
    if not isinstance(current_chat, dict) or 'messages' not in current_chat:
        current_chat = {"topic": "Prescription Reading", "messages": []}
        history.append(current_chat)
   
    current_chat["messages"].append({"role": "system", "content": "User uploaded a prescription image for reading"})

    try:
        image = Image.open(file)
        image = image.convert('L')
        text = pytesseract.image_to_string(image, lang='eng')
       
        if not text.strip():
            logger.error("No text extracted from image")
            raise ValueError("No text could be extracted from the image")

        logger.debug(f"Extracted text (first 100 chars): {text[:100]}")
        text = text[:5000]
       
        docs = vectorstore.similarity_search(text, k=3)
        context = "\n".join([doc.page_content[:500] for doc in docs])[:2000]
        full_context = text + "\n\n" + context
        prescription_prompt = (
            "Act as a medical assistant. Analyze the following prescription text: "
            f"'{text[:1000]}' (truncated for brevity). "
            "Extract key details such as medications, dosages, and instructions. "
            "Structure the response with sections for Medications and Instructions. "
            "If the text is unclear or insufficient, state that analysis is limited and recommend consulting a pharmacist or healthcare professional."
        )
        response = generate_response(groq_client, prescription_prompt, full_context, Config.MODEL_NAME)
        if not response or not isinstance(response, str):
            raise ValueError("Invalid response from Groq API")
    except Exception as e:
        logger.error(f"Error in prescription reading for user_id {user_id}: {e}")
        response = f"Error processing prescription: {str(e)}"

    current_chat["messages"].append({"role": "assistant", "content": response})
    save_user_history(user_id, history)
    logger.debug(f"Prescription reading completed for user_id: {user_id}")
    return jsonify({"response": response, "user_id": user_id})

@app.route("/api/delete_message", methods=["POST"])
def delete_message():
    data = request.get_json()
    user_id = data.get("user_id")
    chat_index = data.get("chat_index")
    message_index = data.get("message_index")

    if not user_id or chat_index is None or message_index is None:
        return jsonify({"error": "user_id, chat_index, and message_index are required"}), 400

    history = load_user_history(user_id)
    if not history or chat_index >= len(history):
        return jsonify({"error": "Invalid chat index"}), 400

    if message_index >= len(history[chat_index]["messages"]):
        return jsonify({"error": "Invalid message index"}), 400

    history[chat_index]["messages"].pop(message_index)
    save_user_history(user_id, history)
    logger.debug(f"Deleted message {message_index} from chat {chat_index} for user_id: {user_id}")
    return jsonify({"message": "Message deleted successfully"})

@app.route("/api/delete_chat", methods=["POST"])
def delete_chat():
    data = request.get_json()
    user_id = data.get("user_id")
    chat_index = data.get("chat_index")

    if not user_id or chat_index is None:
        return jsonify({"error": "user_id and chat_index are required"}), 400

    history = load_user_history(user_id)
    if not history or chat_index >= len(history):
        return jsonify({"error": "Invalid chat index"}), 400

    history.pop(chat_index)
    save_user_history(user_id, history)
    logger.debug(f"Deleted chat {chat_index} for user_id: {user_id}")
    return jsonify({"message": "Chat deleted successfully"})

@app.route("/api/edit_message", methods=["POST"])
def edit_message():
    data = request.get_json()
    user_id = data.get("user_id")
    chat_index = data.get("chat_index")
    message_index = data.get("message_index")
    new_content = data.get("new_content")

    if not user_id or chat_index is None or message_index is None or not isinstance(new_content, str):
        return jsonify({"error": "user_id, chat_index, message_index, and new_content (string) are required"}), 400

    if not new_content.strip() or len(new_content) > 10000:
        return jsonify({"error": "new_content must be non-empty and less than 10,000 characters"}), 400

    history = load_user_history(user_id)
    if not history or chat_index >= len(history):
        return jsonify({"error": "Invalid chat index"}), 400

    if message_index >= len(history[chat_index]["messages"]):
        return jsonify({"error": "Invalid message index"}), 400

    history[chat_index]["messages"][message_index]["content"] = new_content.strip()
    save_user_history(user_id, history)
    logger.debug(f"Edited message {message_index} in chat {chat_index} for user_id: {user_id}")
    return jsonify({"message": "Message edited successfully"})

@app.route("/api/logout", methods=["POST"])
def logout():
    data = request.get_json()
    user_id = data.get("user_id")
    chat_history = data.get("chat_history", [])

    if user_id:
        if isinstance(chat_history, list) and all(isinstance(msg, dict) and 'role' in msg and 'content' in msg for msg in chat_history):
            formatted_history = [{"topic": "Default Chat", "messages": chat_history}]
        else:
            formatted_history = chat_history if all(isinstance(chat, dict) and 'topic' in chat and 'messages' in chat for chat in chat_history) else [{"topic": "Default Chat", "messages": []}]
        save_user_history(user_id, formatted_history)
        logger.debug(f"Logout for user_id: {user_id}. History saved.")
    return jsonify({"message": "Logged out successfully"})

def get_calendar_service(user_id):
    creds = None
    token_path = f'token_{user_id}.json'
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

@app.route("/api/google_login", methods=["POST"])
def google_login():
    user_id = request.form.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    flow.redirect_uri = 'http://localhost:5000/callback'
    authorization_url, _ = flow.authorization_response()
    return jsonify({"auth_url": authorization_url})

@app.route("/callback")
def callback():
    return jsonify({"message": "OAuth2 callback received, close this tab"})

@app.route("/api/calendar", methods=["POST"])
def create_calendar_event():
    user_id = request.form.get("user_id")
    summary = request.form.get("summary", "Medical Reminder")
    start_time = request.form.get("start_time")  # ISO format: 2025-04-17T08:00:00
    end_time = request.form.get("end_time")      # ISO format: 2025-04-17T08:30:00
    if not all([user_id, start_time, end_time]):
        logger.error("Missing calendar params")
        return jsonify({"error": "Missing parameters"}), 400

    try:
        service = get_calendar_service(user_id)
        event = {
            'summary': summary,
            'start': {'dateTime': start_time, 'timeZone': 'UTC'},
            'end': {'dateTime': end_time, 'timeZone': 'UTC'},
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        logger.debug(f"Event created: {event.get('htmlLink')}")
        return jsonify({"message": "Event created", "link": event.get('htmlLink')})
    except Exception as e:
        logger.error(f"Calendar error: {e}")
        return jsonify({"error": str(e)}), 500
   
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)