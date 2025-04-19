// // import React, { useState, useEffect } from "react";
// // import axios from "axios";
// // import Login from "./Login";
// // import "./App.css";

// // function App() {
// //   const [isLoggedIn, setIsLoggedIn] = useState(false);
// //   const [user, setUser] = useState({ id: "", username: "" });
// //   const [chatHistory, setChatHistory] = useState([]);
// //   const [currentChatIndex, setCurrentChatIndex] = useState(-1);
// //   const [input, setInput] = useState("");
// //   const [file, setFile] = useState(null);
// //   const [selectedFeature, setSelectedFeature] = useState("chat");
// //   const [error, setError] = useState(null);
// //   const [editState, setEditState] = useState({ index: null, content: "" });
// //   const [isSidebarOpen, setIsSidebarOpen] = useState(true);

// //   // Handle login and initialize user state
// //   const handleLogin = (userId, username, history) => {
// //     setUser({ id: userId, username });
// //     const formattedHistory = Array.isArray(history) && history.length > 0
// //       ? history.map((chat) => ({
// //           topic: chat.topic || `Chat ${history.length + 1}`,
// //           messages: Array.isArray(chat.messages)
// //             ? chat.messages.filter(
// //                 (msg) => msg && typeof msg.content === "string" && msg.content.trim() !== ""
// //               )
// //             : [],
// //         }))
// //       : [{ topic: "Default Chat", messages: [] }]; // Default chat if history is empty/invalid
// //     setChatHistory(formattedHistory);
// //     setCurrentChatIndex(formattedHistory.length > 0 ? 0 : -1);
// //     setIsLoggedIn(true);
// //   };

// //   // Handle logout and reset state
// //   const handleLogout = async () => {
// //     try {
// //       const flatHistory = chatHistory.flatMap((chat) => chat.messages);
// //       await axios.post("/api/logout", { user_id: user.id, chat_history: flatHistory }, {
// //         headers: { "Content-Type": "application/json" },
// //       });
// //     } catch (err) {
// //       console.error("Logout error:", err);
// //     }
// //     setIsLoggedIn(false);
// //     setUser({ id: "", username: "" });
// //     setChatHistory([]);
// //     setCurrentChatIndex(-1);
// //     setInput("");
// //     setFile(null);
// //     setSelectedFeature("chat");
// //     setError(null);
// //     setEditState({ index: null, content: "" });
// //   };

// //   // Create a new chat
// //   const handleNewChat = () => {
// //     if (!input.trim()) {
// //       setError("Please enter a topic for the new chat");
// //       return;
// //     }
// //     const newChat = { topic: input.trim(), messages: [] };
// //     setChatHistory([...chatHistory, newChat]);
// //     setCurrentChatIndex(chatHistory.length);
// //     setInput("");
// //     setFile(null);
// //     setError(null);
// //   };

// //   // Handle message submission
// //   const handleSend = async (e) => {
// //     if (currentChatIndex === -1) {
// //       setError("Please select or start a conversation");
// //       return;
// //     }

// //     let endpoint, data, headers = { "Content-Type": "application/json" };

// //     if (selectedFeature === "chat" || selectedFeature === "general") {
// //       if (!input.trim()) {
// //         setError("Please enter a message");
// //         return;
// //       }
// //       endpoint = selectedFeature === "chat" ? "/api/chat" : "/api/general_diagnosis";
// //       data = { prompt: input, user_id: user.id };
// //       const newMessage = { role: "user", content: input };
// //       updateChatHistory(newMessage);
// //     } else {
// //       if (!file) {
// //         setError("Please select a file");
// //         return;
// //       }
// //       endpoint = selectedFeature === "report" ? "/api/report_analyzer" : "/api/prescription_reader";
// //       const formData = new FormData();
// //       formData.append(selectedFeature === "report" ? "file" : "image", file);
// //       formData.append("user_id", user.id);
// //       data = formData;
// //       headers = {}; // Let browser set multipart/form-data boundary
// //       updateChatHistory({
// //         role: "system",
// //         content: `User requested ${selectedFeature} ${selectedFeature === "report" ? "analysis" : "reading"}`,
// //       });
// //     }

// //     try {
// //       const response = await axios.post(endpoint, data, { headers });
// //       const responseText = response.data.response || "No response received";
// //       updateChatHistory({ role: "assistant", content: responseText });
// //       if (responseText.includes("Please consult a nearby doctor")) {
// //         setError("The AI couldn't provide a definitive answer. Consider searching for a nearby doctor or hospital.");
// //       }
// //       setInput("");
// //       setFile(null);
// //       if (e && e.target && e.target.querySelector('input[type="file"]')) {
// //         e.target.querySelector('input[type="file"]').value = ""; // Reset file input
// //       }
// //       setError(null);
// //     } catch (error) {
// //       console.error("Axios Error:", error);
// //       setError(`Failed to process: ${error.message}`);
// //       updateChatHistory({ role: "assistant", content: "Error occurred. Please try again." });
// //     }
// //   };

// //   // Utility to update chat history
// //   const updateChatHistory = (message) => {
// //     const updatedChatHistory = [...chatHistory];
// //     updatedChatHistory[currentChatIndex].messages.push(message);
// //     setChatHistory(updatedChatHistory);
// //   };

// //   // Switch to a different chat
// //   const switchChat = (index) => {
// //     setCurrentChatIndex(index);
// //     setError(null);
// //     setEditState({ index: null, content: "" });
// //   };

// //   // Edit message handlers
// //   const handleEdit = (chatIndex, messageIndex) => {
// //     const messageContent = chatHistory[chatIndex].messages[messageIndex].content || "";
// //     setEditState({
// //       index: messageIndex,
// //       content: messageContent, // Ensure content is always a string
// //     });
// //   };

// //   const handleSaveEdit = async (chatIndex, messageIndex) => {
// //     if (editState.index !== null && editState.content.trim()) {
// //       try {
// //         await axios.post("/api/edit_message", {
// //           user_id: user.id,
// //           chat_index: chatIndex,
// //           message_index: messageIndex,
// //           new_content: editState.content,
// //         }, { headers: { "Content-Type": "application/json" } });
// //         const updatedChatHistory = [...chatHistory];
// //         updatedChatHistory[chatIndex].messages[messageIndex].content = editState.content;
// //         setChatHistory(updatedChatHistory);
// //         setEditState({ index: null, content: "" });
// //         setError(null);
// //       } catch (error) {
// //         console.error("Edit error:", error);
// //         setError(`Failed to edit message: ${error.message}`);
// //       }
// //     } else {
// //       setError("Edited message cannot be empty");
// //     }
// //   };

// //   const handleSendEditedQuery = async (chatIndex, messageIndex) => {
// //     if (editState.index !== null && editState.content.trim()) {
// //       try {
// //         const response = await axios.post("/api/chat", {
// //           prompt: editState.content,
// //           user_id: user.id,
// //         }, { headers: { "Content-Type": "application/json" } });
// //         const assistantMessage = {
// //           role: "assistant",
// //           content: response.data.response || "No response received",
// //         };
// //         const updatedChatHistory = [...chatHistory];
// //         updatedChatHistory[chatIndex].messages[messageIndex].content = editState.content;
// //         updatedChatHistory[chatIndex].messages.push(assistantMessage);
// //         setChatHistory(updatedChatHistory);
// //         setEditState({ index: null, content: "" });
// //         setError(null);
// //       } catch (error) {
// //         console.error("Send edited query error:", error);
// //         setError(`Failed to send edited query: ${error.message}`);
// //       }
// //     } else {
// //       setError("Edited message cannot be empty");
// //     }
// //   };

// //   // Delete handlers
// //   const handleDeleteMessage = async (chatIndex, messageIndex) => {
// //     try {
// //       await axios.post("/api/delete_message", {
// //         user_id: user.id,
// //         chat_index: chatIndex,
// //         message_index: messageIndex,
// //       }, { headers: { "Content-Type": "application/json" } });
// //       const updatedChatHistory = [...chatHistory];
// //       updatedChatHistory[chatIndex].messages.splice(messageIndex, 1);
// //       setChatHistory(updatedChatHistory);
// //       setError(null);
// //     } catch (error) {
// //       console.error("Delete error:", error);
// //       setError(`Failed to delete message: ${error.message}`);
// //     }
// //   };

// //   const handleDeleteChat = async (chatIndex) => {
// //     try {
// //       await axios.post("/api/delete_chat", {
// //         user_id: user.id,
// //         chat_index: chatIndex,
// //       }, { headers: { "Content-Type": "application/json" } });
// //       const updatedChatHistory = [...chatHistory];
// //       updatedChatHistory.splice(chatIndex, 1);
// //       setChatHistory(updatedChatHistory);
// //       setCurrentChatIndex(updatedChatHistory.length > 0 ? 0 : -1);
// //       setError(null);
// //     } catch (error) {
// //       console.error("Delete chat error:", error);
// //       setError(`Failed to delete chat: ${error.message}`);
// //     }
// //   };

// //   // Format response for display
// //   const formatResponse = (text) => {
// //     if (!text) return <p className="response-text">No content available</p>;
// //     const textStr = typeof text === "string" ? text : JSON.stringify(text);
// //     const cleanedText = textStr.replace(/(\*\*|#|\*|:|\(|\))/g, "").trim();
// //     const sections = cleanedText.split("\n\n").filter((s) => s.trim());

// //     return sections.map((section, index) => {
// //       if (section.startsWith("Symptoms") || section.startsWith("Causes") || section.startsWith("Remedies")) {
// //         return <h2 key={index} className="response-header">{section.split("\n")[0]}</h2>;
// //       }
// //       if (section.includes("- ")) {
// //         const items = section.split("\n").filter((i) => i.trim());
// //         return (
// //           <ul key={index} className="response-list">
// //             {items.map((item, i) => (
// //               <li key={i} className="list-item">{item.replace("- ", "")}</li>
// //             ))}
// //           </ul>
// //         );
// //       }
// //       return <p key={index} className="response-text">{section}</p>;
// //     }).filter(Boolean);
// //   };

// //   if (!isLoggedIn) return <Login onLogin={handleLogin} />;

// //   return (
// //     <div className="app-container">
// //       <header className="app-header">
// //         <div className="header-left">
// //           <button className="sidebar-toggle" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
// //             {isSidebarOpen ? "◄" : "►"}
// //           </button>
// //           <h1 className="app-title">Medical AI Assistant</h1>
// //         </div>
// //         <div className="header-right">
// //           <span className="user-name">{user.username}</span>
// //           <button className="logout-btn" onClick={handleLogout}>Logout</button>
// //         </div>
// //       </header>
// //       <div className="main-layout">
// //         <aside className={`sidebar ${isSidebarOpen ? "open" : "closed"}`}>
// //           <h2>Conversations</h2>
// //           {chatHistory.length === 0 ? (
// //             <p className="no-chats">No conversations yet</p>
// //           ) : (
// //             chatHistory.map((chat, index) => (
// //               <div
// //                 key={index}
// //                 className={`chat-item ${index === currentChatIndex ? "active" : ""}`}
// //                 onClick={() => switchChat(index)}
// //               >
// //                 <span className="chat-topic">{chat.topic}</span>
// //                 <button
// //                   className="delete-chat-btn"
// //                   onClick={(e) => {
// //                     e.stopPropagation();
// //                     handleDeleteChat(index);
// //                   }}
// //                 >
// //                   ✕
// //                 </button>
// //               </div>
// //             ))
// //           )}
// //           <button className="new-chat-btn" onClick={handleNewChat}>+ New Chat</button>
// //         </aside>
// //         <main className="chat-area">
// //           <div className="feature-tabs">
// //             {["chat", "general", "report", "prescription"].map((feature) => (
// //               <button
// //                 key={feature}
// //                 className={`tab-btn ${selectedFeature === feature ? "active" : ""}`}
// //                 onClick={() => setSelectedFeature(feature)}
// //               >
// //                 {feature.charAt(0).toUpperCase() + feature.slice(1).replace("prescription", "Prescription Reader")}
// //               </button>
// //             ))}
// //           </div>
// //           <div className="messages-container">
// //             {currentChatIndex === -1 ? (
// //               <div className="placeholder">Select or start a new conversation</div>
// //             ) : (
// //               chatHistory[currentChatIndex].messages.map((msg, index) => (
// //                 <div key={index} className={`message ${msg.role}`}>
// //                   {msg.role === "system" ? (
// //                     <div className="system-message">{msg.content || "System message"}</div>
// //                   ) : (
// //                     <>
// //                       <div className="message-content">
// //                         {editState.index === index ? (
// //                           <div className="edit-container">
// //                             <input
// //                               type="text"
// //                               value={editState.content}
// //                               onChange={(e) => setEditState({ ...editState, content: e.target.value })}
// //                               autoFocus
// //                             />
// //                             <div className="edit-actions">
// //                               <button onClick={() => handleSaveEdit(currentChatIndex, index)}>Save</button>
// //                               <button onClick={() => handleSendEditedQuery(currentChatIndex, index)}>Send</button>
// //                               <button onClick={() => setEditState({ index: null, content: "" })}>Cancel</button>
// //                             </div>
// //                           </div>
// //                         ) : (
// //                           formatResponse(msg.content)
// //                         )}
// //                       </div>
// //                       {editState.index !== index && (
// //                         <div className="message-actions">
// //                           <button onClick={() => handleEdit(currentChatIndex, index)}>Edit</button>
// //                           <button onClick={() => handleDeleteMessage(currentChatIndex, index)}>Delete</button>
// //                         </div>
// //                       )}
// //                     </>
// //                   )}
// //                 </div>
// //               ))
// //             )}
// //             {error && <div className="error-message">{error}</div>}
// //           </div>
// //           <div className="input-section">
// //             {selectedFeature === "chat" || selectedFeature === "general" ? (
// //               <input
// //                 type="text"
// //                 value={input}
// //                 onChange={(e) => setInput(e.target.value)}
// //                 onKeyPress={(e) => e.key === "Enter" && handleSend(e)}
// //                 placeholder={selectedFeature === "chat" ? "Ask a medical question..." : "Describe symptoms..."}
// //               />
// //             ) : (
// //               <input
// //                 type="file"
// //                 onChange={(e) => setFile(e.target.files[0] || null)}
// //                 accept={selectedFeature === "report" ? ".pdf" : "image/*"}
// //               />
// //             )}
// //             <button onClick={handleSend}>Send</button>
// //           </div>
// //         </main>
// //       </div>
// //     </div>
// //   );
// // }

// // export default App; 
// import React, { useState, useEffect, useRef } from "react";
// import axios from "axios";
// import Login from "./Login";
// import "./App.css";

// function App() {
//   const [isLoggedIn, setIsLoggedIn] = useState(false);
//   const [user, setUser] = useState({ id: "", username: "" });
//   const [chatHistory, setChatHistory] = useState([]);
//   const [currentChatIndex, setCurrentChatIndex] = useState(-1);
//   const [input, setInput] = useState("");
//   const [file, setFile] = useState(null);
//   const [selectedFeature, setSelectedFeature] = useState("chat");
//   const [error, setError] = useState(null);
//   const [editState, setEditState] = useState({ index: null, content: "" });
//   const [isSidebarOpen, setIsSidebarOpen] = useState(true);
//   const [isRecording, setIsRecording] = useState(false);
//   const [mediaRecorder, setMediaRecorder] = useState(null);
//   const [calendarEvent, setCalendarEvent] = useState({ summary: "", date: "", time: "" });
//   const [showDeleteConfirm, setShowDeleteConfirm] = useState({ visible: false, type: '', index: null, messageIndex: null });
//   const audioChunksRef = useRef([]);

//   const handleLogin = (userId, username, history) => {
//     setUser({ id: userId, username });
//     const formattedHistory = Array.isArray(history) && history.length > 0
//       ? history.map((chat) => ({
//           topic: chat.topic || `Chat ${history.length + 1}`,
//           messages: Array.isArray(chat.messages)
//             ? chat.messages.filter(
//                 (msg) => msg && typeof msg.content === "string" && msg.content.trim() !== ""
//               )
//             : [],
//         }))
//       : [{ topic: "Default Chat", messages: [] }];
//     setChatHistory(formattedHistory);
//     setCurrentChatIndex(formattedHistory.length > 0 ? 0 : -1);
//     setIsLoggedIn(true);
//   };

//   const handleLogout = async () => {
//     try {
//       const flatHistory = chatHistory.flatMap((chat) => chat.messages);
//       await axios.post("/api/logout", { user_id: user.id, chat_history: flatHistory }, {
//         headers: { "Content-Type": "application/json" },
//       });
//     } catch (err) {
//       console.error("Logout error:", err);
//     }
//     setIsLoggedIn(false);
//     setUser({ id: "", username: "" });
//     setChatHistory([]);
//     setCurrentChatIndex(-1);
//     setInput("");
//     setFile(null);
//     setSelectedFeature("chat");
//     setError(null);
//     setEditState({ index: null, content: "" });
//     setCalendarEvent({ summary: "", date: "", time: "" });
//     stopRecording();
//   };

//   const handleNewChat = () => {
//     const newChat = { topic: `Chat ${chatHistory.length + 1}`, messages: [] };
//     setChatHistory([...chatHistory, newChat]);
//     setCurrentChatIndex(chatHistory.length);
//     setInput("");
//     setFile(null);
//     setError(null);
//     setCalendarEvent({ summary: "", date: "", time: "" });
//   };

//   const startRecording = async () => {
//     if (currentChatIndex === -1) {
//       setError("Please select or start a conversation");
//       return;
//     }
//     if (selectedFeature !== "chat" && selectedFeature !== "general") {
//       setError("Voice input is only available for Chat and General Diagnosis");
//       return;
//     }
//     try {
//       const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//       const recorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
//       setMediaRecorder(recorder);
//       audioChunksRef.current = [];

//       recorder.ondataavailable = (event) => {
//         if (event.data.size > 0) {
//           audioChunksRef.current.push(event.data);
//           sendAudioChunk(event.data);
//         }
//       };

//       recorder.onstop = () => {
//         stream.getTracks().forEach((track) => track.stop());
//       };

//       recorder.start(2000);
//       setIsRecording(true);
//       setError(null);
//     } catch (err) {
//       console.error("Recording error:", err);
//       setError("Failed to access microphone. Please check permissions.");
//     }
//   };

//   const stopRecording = () => {
//     if (mediaRecorder && mediaRecorder.state !== "inactive") {
//       mediaRecorder.stop();
//       setIsRecording(false);
//       setMediaRecorder(null);
//       audioChunksRef.current = [];
//     }
//   };

//   const sendAudioChunk = async (audioBlob) => {
//     const formData = new FormData();
//     formData.append("audio", audioBlob, "chunk.webm");
//     formData.append("user_id", user.id);

//     try {
//       const response = await axios.post("/api/transcribe", formData, {
//         headers: { "Content-Type": "multipart/form-data" },
//       });
//       const transcription = response.data.transcription;
//       if (transcription) {
//         setInput(transcription);
//         if (transcription.trim()) {
//           await handleSend({ preventDefault: () => {} });
//         }
//       }
//     } catch (error) {
//       console.error("Transcription error:", error.response?.data || error.message);
//       setError(`Failed to transcribe audio: ${error.response?.data?.error || error.message}`);
//       stopRecording();
//     }
//   };

//   const handleSend = async (e) => {
//     e.preventDefault && e.preventDefault();
//     if (currentChatIndex === -1) {
//       setError("Please select or start a conversation");
//       return;
//     }

//     let endpoint, data, headers = { "Content-Type": "application/json" };

//     if (selectedFeature === "chat" || selectedFeature === "general") {
//       if (!input.trim()) {
//         setError("Please enter a message");
//         return;
//       }
//       endpoint = selectedFeature === "chat" ? "/api/chat" : "/api/general_diagnosis";
//       data = { prompt: input, user_id: user.id };
//       const newMessage = { role: "user", content: input };
//       updateChatHistory(newMessage);
//     } else if (selectedFeature === "report" || selectedFeature === "prescription") {
//       if (!file) {
//         setError("Please select a file");
//         return;
//       }
//       endpoint = selectedFeature === "report" ? "/api/report_analyzer" : "/api/prescription_reader";
//       const formData = new FormData();
//       formData.append(selectedFeature === "report" ? "file" : "image", file);
//       formData.append("user_id", user.id);
//       data = formData;
//       headers = {};
//       updateChatHistory({
//         role: "system",
//         content: `User requested ${selectedFeature} ${selectedFeature === "report" ? "analysis" : "reading"}`,
//       });
//     } else if (selectedFeature === "calendar") {
//       if (!calendarEvent.summary || !calendarEvent.date || !calendarEvent.time) {
//         setError("Please fill all calendar fields");
//         return;
//       }
//       endpoint = "/api/calendar";
//       const timeParts = calendarEvent.time.split(':');
//       const formattedTime = `${timeParts[0].padStart(2, '0')}:${timeParts[1] || '00'}:00Z`;
//       const startTime = `${calendarEvent.date}T${formattedTime}`;
//       const endTime = new Date(new Date(startTime).getTime() + 30 * 60000).toISOString();
//       data = {
//         user_id: user.id,
//         summary: calendarEvent.summary,
//         start_time: startTime,
//         end_time: endTime,
//       };
//       updateChatHistory({
//         role: "user",
//         content: `Set reminder: ${calendarEvent.summary} at ${calendarEvent.date} ${formattedTime}`,
//       });
//     }

//     try {
//       const response = await axios.post(endpoint, data, { headers });
//       let responseText = response.data.response || response.data.message || "No response received";
//       if (selectedFeature === "calendar") {
//         responseText = `Reminder set: ${response.data.link}`;
//         if (response.data.auth_url) {
//           window.open(response.data.auth_url, "_blank");
//           responseText = "Please authorize Google Calendar access in the new window.";
//         }
//       }
//       updateChatHistory({ role: "assistant", content: responseText });
//       setError(null);
//       setInput("");
//       setFile(null);
//       setCalendarEvent({ summary: "", date: "", time: "" });
//       if (e.target && e.target.querySelector('input[type="file"]')) {
//         e.target.querySelector('input[type="file"]').value = "";
//       }
//     } catch (error) {
//       console.error("Axios Error:", error);
//       setError(`Failed to process: ${error.message}`);
//       updateChatHistory({ role: "assistant", content: "Error occurred. Please try again." });
//     }
//   };

//   const updateChatHistory = (message) => {
//     const updatedChatHistory = [...chatHistory];
//     updatedChatHistory[currentChatIndex].messages.push(message);
//     setChatHistory(updatedChatHistory);
//   };

//   const switchChat = (index) => {
//     setCurrentChatIndex(index);
//     setError(null);
//     setEditState({ index: null, content: "" });
//     setCalendarEvent({ summary: "", date: "", time: "" });
//     stopRecording();
//   };

//   const handleEdit = (chatIndex, messageIndex) => {
//     const messageContent = chatHistory[chatIndex].messages[messageIndex].content || "";
//     setEditState({ index: messageIndex, content: messageContent });
//   };

//   const handleSaveEdit = async (chatIndex, messageIndex) => {
//     if (editState.index !== null && editState.content.trim()) {
//       try {
//         await axios.post("/api/edit_message", {
//           user_id: user.id,
//           chat_index: chatIndex,
//           message_index: messageIndex,
//           new_content: editState.content,
//         }, { headers: { "Content-Type": "application/json" } });
//         const updatedChatHistory = [...chatHistory];
//         updatedChatHistory[chatIndex].messages[messageIndex].content = editState.content;
//         setChatHistory(updatedChatHistory);
//         setEditState({ index: null, content: "" });
//         setError(null);
//       } catch (error) {
//         console.error("Edit error:", error);
//         setError(`Failed to edit message: ${error.message}`);
//       }
//     } else {
//       setError("Edited message cannot be empty");
//     }
//   };

//   const handleSendEditedQuery = async (chatIndex, messageIndex) => {
//     if (editState.index !== null && editState.content.trim()) {
//       try {
//         const response = await axios.post("/api/chat", {
//           prompt: editState.content,
//           user_id: user.id,
//         }, { headers: { "Content-Type": "application/json" } });
//         const assistantMessage = {
//           role: "assistant",
//           content: response.data.response || "No response received",
//         };
//         const updatedChatHistory = [...chatHistory];
//         updatedChatHistory[chatIndex].messages[messageIndex].content = editState.content;
//         updatedChatHistory[chatIndex].messages.push(assistantMessage);
//         setChatHistory(updatedChatHistory);
//         setEditState({ index: null, content: "" });
//         setError(null);
//       } catch (error) {
//         console.error("Send edited query error:", error);
//         setError(`Failed to send edited query: ${error.message}`);
//       }
//     } else {
//       setError("Edited message cannot be empty");
//     }
//   };

//   const handleDeleteMessage = async (chatIndex, messageIndex) => {
//     const messages = chatHistory[chatIndex].messages;
//     if (messages.length > 1 || (messages.length === 1 && messages[0].content.trim())) {
//       setShowDeleteConfirm({ visible: true, type: 'message', index: chatIndex, messageIndex });
//     } else {
//       try {
//         await axios.post("/api/delete_message", {
//           user_id: user.id,
//           chat_index: chatIndex,
//           message_index: messageIndex,
//         }, { headers: { "Content-Type": "application/json" } });
//         const updatedChatHistory = [...chatHistory];
//         updatedChatHistory[chatIndex].messages.splice(messageIndex, 1);
//         setChatHistory(updatedChatHistory);
//         setError(null);
//       } catch (error) {
//         console.error("Delete error:", error);
//         setError(`Failed to delete message: ${error.message}`);
//       }
//     }
//   };

//   const handleDeleteChat = async (chatIndex) => {
//     const messages = chatHistory[chatIndex].messages;
//     if (messages.length > 0 || (messages.length === 0 && chatHistory[chatIndex].topic.trim())) {
//       setShowDeleteConfirm({ visible: true, type: 'chat', index: chatIndex, messageIndex: null });
//     } else {
//       try {
//         await axios.post("/api/delete_chat", {
//           user_id: user.id,
//           chat_index: chatIndex,
//         }, { headers: { "Content-Type": "application/json" } });
//         const updatedChatHistory = [...chatHistory];
//         updatedChatHistory.splice(chatIndex, 1);
//         setChatHistory(updatedChatHistory);
//         setCurrentChatIndex(updatedChatHistory.length > 0 ? 0 : -1);
//         setError(null);
//       } catch (error) {
//         console.error("Delete chat error:", error);
//         setError(`Failed to delete chat: ${error.message}`);
//       }
//     }
//   };

//   const confirmDelete = async () => {
//     if (showDeleteConfirm.type === 'chat') {
//       try {
//         await axios.post("/api/delete_chat", {
//           user_id: user.id,
//           chat_index: showDeleteConfirm.index,
//         }, { headers: { "Content-Type": "application/json" } });
//         const updatedChatHistory = [...chatHistory];
//         updatedChatHistory.splice(showDeleteConfirm.index, 1);
//         setChatHistory(updatedChatHistory);
//         setCurrentChatIndex(updatedChatHistory.length > 0 ? 0 : -1);
//         setError(null);
//       } catch (error) {
//         console.error("Delete chat error:", error);
//         setError(`Failed to delete chat: ${error.message}`);
//       }
//     } else if (showDeleteConfirm.type === 'message') {
//       try {
//         await axios.post("/api/delete_message", {
//           user_id: user.id,
//           chat_index: showDeleteConfirm.index,
//           message_index: showDeleteConfirm.messageIndex,
//         }, { headers: { "Content-Type": "application/json" } });
//         const updatedChatHistory = [...chatHistory];
//         updatedChatHistory[showDeleteConfirm.index].messages.splice(showDeleteConfirm.messageIndex, 1);
//         setChatHistory(updatedChatHistory);
//         setError(null);
//       } catch (error) {
//         console.error("Delete error:", error);
//         setError(`Failed to delete message: ${error.message}`);
//       }
//     }
//     setShowDeleteConfirm({ visible: false, type: '', index: null, messageIndex: null });
//   };

//   const cancelDelete = () => {
//     setShowDeleteConfirm({ visible: false, type: '', index: null, messageIndex: null });
//   };

//   const formatResponse = (text) => {
//     if (!text) return <p className="response-text">No content available</p>;
//     const textStr = typeof text === "string" ? text : JSON.stringify(text);
//     const lines = textStr.split("\n").filter(line => line.trim());
//     let currentSection = "";
//     let formattedContent = [];

//     lines.forEach((line, index) => {
//       const trimmedLine = line.trim();
//       if (trimmedLine.startsWith("##")) {
//         currentSection = trimmedLine.replace("## ", "");
//         formattedContent.push(<h2 key={index} className="response-header">{currentSection}</h2>);
//       } else if (trimmedLine.startsWith("- ")) {
//         const content = trimmedLine.replace("- ", "");
//         if (content.includes(":")) {
//           formattedContent.push(<p key={index} className="response-subtext">{content}</p>);
//         } else {
//           formattedContent.push(<ul key={index} className="response-list"><li className="list-item">{content}</li></ul>);
//         }
//       } else if (trimmedLine.startsWith("+ ")) {
//         const content = trimmedLine.replace("+ ", "");
//         formattedContent.push(<ul key={index} className="response-list"><li className="list-subitem">{content}</li></ul>);
//       } else if (trimmedLine) {
//         formattedContent.push(<p key={index} className="response-subtext">{trimmedLine}</p>);
//       }
//     });

//     return formattedContent;
//   };

//   if (!isLoggedIn) return <Login onLogin={handleLogin} />;

//   return (
//     <div className="app-container">
//       <header className="app-header">
//         <div className="header-left">
//           <button className="sidebar-toggle" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
//             {isSidebarOpen ? "◄" : "►"}
//           </button>
//           <h1 className="app-title">Medical Chatbot</h1>
//         </div>
//         <div className="header-right">
//           <span className="user-name">{user.username}</span>
//           <button className="new-chat-btn" onClick={handleNewChat}>New Chat</button>
//           <button className="logout-btn" onClick={handleLogout}>Logout</button>
//         </div>
//       </header>
//       <div className="main-layout">
//         <aside className={`sidebar ${isSidebarOpen ? "open" : "closed"}`}>
//           <h2>Chat History</h2>
//           {chatHistory.length === 0 ? (
//             <p className="no-chats">No chats yet</p>
//           ) : (
//             chatHistory.map((chat, index) => (
//               <div
//                 key={index}
//                 className={`chat-item ${index === currentChatIndex ? "active" : ""}`}
//                 onClick={() => switchChat(index)}
//               >
//                 <span className="chat-topic">{chat.topic}</span>
//                 <button
//                   className="delete-chat-btn"
//                   onClick={(e) => {
//                     e.stopPropagation();
//                     handleDeleteChat(index);
//                   }}
//                 >
//                   Delete
//                 </button>
//               </div>
//             ))
//           )}
//         </aside>
//         <main className="chat-area">
//           <div className="feature-tabs">
//             {["chat", "general", "report", "prescription", "calendar"].map((feature) => (
//               <button
//                 key={feature}
//                 className={`tab-btn ${selectedFeature === feature ? "active" : ""}`}
//                 onClick={() => setSelectedFeature(feature)}
//               >
//                 {feature.charAt(0).toUpperCase() +
//                   feature
//                     .slice(1)
//                     .replace("general", "General Diagnosis")
//                     .replace("report", "Report Analyzer")
//                     .replace("prescription", "Prescription Reader")
//                     .replace("calendar", "Calendar Reminder")}
//               </button>
//             ))}
//           </div>
//           <div className="messages-container">
//             {currentChatIndex === -1 ? (
//               <div className="placeholder">Select or start a new conversation</div>
//             ) : (
//               chatHistory[currentChatIndex].messages.map((msg, index) => (
//                 <div key={index} className={`message ${msg.role}`}>
//                   {msg.role === "system" ? (
//                     <div className="system-message">{msg.content || "System message"}</div>
//                   ) : (
//                     <>
//                       <div className="message-content">
//                         {editState.index === index ? (
//                           <div className="edit-container">
//                             <input
//                               type="text"
//                               value={editState.content}
//                               onChange={(e) => setEditState({ ...editState, content: e.target.value })}
//                               autoFocus
//                               className="edit-input"
//                             />
//                             <div className="edit-actions">
//                               <button onClick={() => handleSaveEdit(currentChatIndex, index)}>Save</button>
//                               <button onClick={() => handleSendEditedQuery(currentChatIndex, index)}>Send</button>
//                               <button onClick={() => setEditState({ index: null, content: "" })}>Cancel</button>
//                             </div>
//                           </div>
//                         ) : (
//                           formatResponse(msg.content)
//                         )}
//                       </div>
//                       {editState.index !== index && (
//                         <div className="message-actions">
//                           <button onClick={() => handleEdit(currentChatIndex, index)}>Edit</button>
//                           <button onClick={() => handleDeleteMessage(currentChatIndex, index)}>Delete</button>
//                         </div>
//                       )}
//                     </>
//                   )}
//                 </div>
//               ))
//             )}
//             {error && <div className="error-message">{error}</div>}
//           </div>
//           <div className="input-section">
//             {selectedFeature === "chat" || selectedFeature === "general" ? (
//               <>
//                 <input
//                   type="text"
//                   value={input}
//                   onChange={(e) => setInput(e.target.value)}
//                   onKeyPress={(e) => e.key === "Enter" && handleSend(e)}
//                   placeholder={selectedFeature === "chat" ? "Ask a medical question..." : "Describe symptoms..."}
//                   className="input-field"
//                 />
//                 <button
//                   className={`mic-btn ${isRecording ? "recording" : ""}`}
//                   onClick={isRecording ? stopRecording : startRecording}
//                 >
//                   {isRecording ? "■" : "🎤"}
//                 </button>
//               </>
//             ) : selectedFeature === "report" || selectedFeature === "prescription" ? (
//               <input
//                 type="file"
//                 onChange={(e) => setFile(e.target.files[0] || null)}
//                 accept={selectedFeature === "report" ? ".pdf" : "image/*"}
//               />
//             ) : (
//               <div className="calendar-inputs">
//                 <input
//                   type="text"
//                   placeholder="Reminder (e.g., Take ibuprofen)"
//                   value={calendarEvent.summary}
//                   onChange={(e) => setCalendarEvent({ ...calendarEvent, summary: e.target.value })}
//                 />
//                 <input
//                   type="date"
//                   value={calendarEvent.date}
//                   onChange={(e) => setCalendarEvent({ ...calendarEvent, date: e.target.value })}
//                 />
//                 <input
//                   type="time"
//                   value={calendarEvent.time}
//                   onChange={(e) => setCalendarEvent({ ...calendarEvent, time: e.target.value })}
//                 />
//               </div>
//             )}
//             <button onClick={handleSend}>Send</button>
//           </div>
//         </main>
//       </div>
//       {showDeleteConfirm.visible && (
//         <div className="modal">
//           <div className="modal-content">
//             <h3>Confirm Deletion</h3>
//             <p>Are you sure you want to delete this {showDeleteConfirm.type}?</p>
//             <div className="modal-actions">
//               <button onClick={confirmDelete}>Yes</button>
//               <button onClick={cancelDelete}>No</button>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App; 

import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import Login from "./Login";
import "./App.css";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState({ id: "", username: "" });
  const [chatHistory, setChatHistory] = useState([]);
  const [currentChatIndex, setCurrentChatIndex] = useState(-1);
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);
  const [selectedFeature, setSelectedFeature] = useState("chat");
  const [error, setError] = useState(null);
  const [editState, setEditState] = useState({ index: null, content: "" });
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [calendarEvent, setCalendarEvent] = useState({ summary: "", date: "", time: "" });
  const [showDeleteConfirm, setShowDeleteConfirm] = useState({ visible: false, type: '', index: null, messageIndex: null });
  const audioChunksRef = useRef([]);

  const handleLogin = (userId, username, history) => {
    setUser({ id: userId, username });
    const formattedHistory = Array.isArray(history) && history.length > 0
      ? history.map((chat) => ({
          topic: chat.topic || `Chat ${history.length + 1}`,
          messages: Array.isArray(chat.messages)
            ? chat.messages.filter(
                (msg) => msg && typeof msg.content === "string" && msg.content.trim() !== ""
              )
            : [],
        }))
      : [{ topic: "Default Chat", messages: [] }];
    setChatHistory(formattedHistory);
    setCurrentChatIndex(formattedHistory.length > 0 ? 0 : -1);
    setIsLoggedIn(true);
  };

  const handleLogout = async () => {
    try {
      const flatHistory = chatHistory.flatMap((chat) => chat.messages);
      await axios.post("/api/logout", { user_id: user.id, chat_history: flatHistory }, {
        headers: { "Content-Type": "application/json" },
      });
    } catch (err) {
      console.error("Logout error:", err);
    }
    setIsLoggedIn(false);
    setUser({ id: "", username: "" });
    setChatHistory([]);
    setCurrentChatIndex(-1);
    setInput("");
    setFile(null);
    setSelectedFeature("chat");
    setError(null);
    setEditState({ index: null, content: "" });
    setCalendarEvent({ summary: "", date: "", time: "" });
    stopRecording();
  };

  const handleNewChat = () => {
    const newChat = { topic: `Chat ${chatHistory.length + 1}`, messages: [] };
    setChatHistory([...chatHistory, newChat]);
    setCurrentChatIndex(chatHistory.length);
    setInput("");
    setFile(null);
    setError(null);
    setCalendarEvent({ summary: "", date: "", time: "" });
  };

  const startRecording = async () => {
    if (currentChatIndex === -1) {
      setError("Please select or start a conversation");
      return;
    }
    if (selectedFeature !== "chat" && selectedFeature !== "general") {
      setError("Voice input is only available for Chat and General Diagnosis");
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
      setMediaRecorder(recorder);
      audioChunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
          sendAudioChunk(event.data);
        }
      };

      recorder.onstop = () => {
        stream.getTracks().forEach((track) => track.stop());
      };

      recorder.start(2000);
      setIsRecording(true);
      setError(null);
    } catch (err) {
      console.error("Recording error:", err);
      setError("Failed to access microphone. Please check permissions.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
      setIsRecording(false);
      setMediaRecorder(null);
      audioChunksRef.current = [];
    }
  };

  const sendAudioChunk = async (audioBlob) => {
    const formData = new FormData();
    formData.append("audio", audioBlob, "chunk.webm");
    formData.append("user_id", user.id);

    try {
      const response = await axios.post("/api/transcribe", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const transcription = response.data.transcription;
      if (transcription) {
        setInput(transcription);
        if (transcription.trim()) {
          await handleSend({ preventDefault: () => {} });
        }
      }
    } catch (error) {
      console.error("Transcription error:", error.response?.data || error.message);
      setError(`Failed to transcribe audio: ${error.response?.data?.error || error.message}`);
      stopRecording();
    }
  };

  const handleSend = async (e) => {
    e.preventDefault && e.preventDefault();
    if (currentChatIndex === -1) {
      setError("Please select or start a conversation");
      return;
    }

    let endpoint, data, headers = { "Content-Type": "application/json" };

    if (selectedFeature === "chat" || selectedFeature === "general") {
      if (!input.trim()) {
        setError("Please enter a message");
        return;
      }
      endpoint = selectedFeature === "chat" ? "/api/chat" : "/api/general_diagnosis";
      data = { prompt: input, user_id: user.id };
      const newMessage = { role: "user", content: input };
      updateChatHistory(newMessage);
    } else if (selectedFeature === "report" || selectedFeature === "prescription") {
      if (!file) {
        setError("Please select a file");
        return;
      }
      endpoint = selectedFeature === "report" ? "/api/report_analyzer" : "/api/prescription_reader";
      const formData = new FormData();
      formData.append(selectedFeature === "report" ? "file" : "image", file);
      formData.append("user_id", user.id);
      data = formData;
      headers = {};
      updateChatHistory({
        role: "system",
        content: `User requested ${selectedFeature} ${selectedFeature === "report" ? "analysis" : "reading"}`,
      });
    } else if (selectedFeature === "calendar") {
      if (!calendarEvent.summary || !calendarEvent.date || !calendarEvent.time) {
        setError("Please fill all calendar fields");
        return;
      }
      endpoint = "/api/calendar";
      const timeParts = calendarEvent.time.split(':');
      const formattedTime = `${timeParts[0].padStart(2, '0')}:${timeParts[1] || '00'}:00Z`;
      const startTime = `${calendarEvent.date}T${formattedTime}`;
      const endTime = new Date(new Date(startTime).getTime() + 30 * 60000).toISOString();
      data = {
        user_id: user.id,
        summary: calendarEvent.summary,
        start_time: startTime,
        end_time: endTime,
      };
      updateChatHistory({
        role: "user",
        content: `Set reminder: ${calendarEvent.summary} at ${calendarEvent.date} ${formattedTime}`,
      });
    }

    try {
      const response = await axios.post(endpoint, data, { headers });
      let responseText = response.data.response || response.data.message || "No response received";
      if (selectedFeature === "calendar") {
        responseText = `Reminder set: ${response.data.link}`;
        if (response.data.auth_url) {
          window.open(response.data.auth_url, "_blank");
          responseText = "Please authorize Google Calendar access in the new window.";
        }
      }
      updateChatHistory({ role: "assistant", content: responseText });
      setError(null);
      setInput("");
      setFile(null);
      setCalendarEvent({ summary: "", date: "", time: "" });
      if (e.target && e.target.querySelector('input[type="file"]')) {
        e.target.querySelector('input[type="file"]').value = "";
      }
    } catch (error) {
      console.error("Axios Error:", error);
      setError(`Failed to process: ${error.message}`);
      updateChatHistory({ role: "assistant", content: "Error occurred. Please try again." });
    }
  };

  const updateChatHistory = (message) => {
    const updatedChatHistory = [...chatHistory];
    updatedChatHistory[currentChatIndex].messages.push(message);
    setChatHistory(updatedChatHistory);
  };

  const switchChat = (index) => {
    setCurrentChatIndex(index);
    setError(null);
    setEditState({ index: null, content: "" });
    setCalendarEvent({ summary: "", date: "", time: "" });
    stopRecording();
  };

  const handleEdit = (chatIndex, messageIndex) => {
    const messageContent = chatHistory[chatIndex].messages[messageIndex].content || "";
    setEditState({ index: messageIndex, content: messageContent });
  };

  const handleSaveEdit = async (chatIndex, messageIndex) => {
    if (editState.index !== null && editState.content.trim()) {
      try {
        await axios.post("/api/edit_message", {
          user_id: user.id,
          chat_index: chatIndex,
          message_index: messageIndex,
          new_content: editState.content,
        }, { headers: { "Content-Type": "application/json" } });
        const updatedChatHistory = [...chatHistory];
        updatedChatHistory[chatIndex].messages[messageIndex].content = editState.content;
        setChatHistory(updatedChatHistory);
        setEditState({ index: null, content: "" });
        setError(null);
      } catch (error) {
        console.error("Edit error:", error);
        setError(`Failed to edit message: ${error.message}`);
      }
    } else {
      setError("Edited message cannot be empty");
    }
  };

  const handleSendEditedQuery = async (chatIndex, messageIndex) => {
    if (editState.index !== null && editState.content.trim()) {
      try {
        const response = await axios.post("/api/chat", {
          prompt: editState.content,
          user_id: user.id,
        }, { headers: { "Content-Type": "application/json" } });
        const assistantMessage = {
          role: "assistant",
          content: response.data.response || "No response received",
        };
        const updatedChatHistory = [...chatHistory];
        updatedChatHistory[chatIndex].messages[messageIndex].content = editState.content;
        updatedChatHistory[chatIndex].messages.push(assistantMessage);
        setChatHistory(updatedChatHistory);
        setEditState({ index: null, content: "" });
        setError(null);
      } catch (error) {
        console.error("Send edited query error:", error);
        setError(`Failed to send edited query: ${error.message}`);
      }
    } else {
      setError("Edited message cannot be empty");
    }
  };

  const handleDeleteMessage = async (chatIndex, messageIndex) => {
    const messages = chatHistory[chatIndex].messages;
    if (messages.length > 1 || (messages.length === 1 && messages[0].content.trim())) {
      setShowDeleteConfirm({ visible: true, type: 'message', index: chatIndex, messageIndex });
    } else {
      try {
        await axios.post("/api/delete_message", {
          user_id: user.id,
          chat_index: chatIndex,
          message_index: messageIndex,
        }, { headers: { "Content-Type": "application/json" } });
        const updatedChatHistory = [...chatHistory];
        updatedChatHistory[chatIndex].messages.splice(messageIndex, 1);
        setChatHistory(updatedChatHistory);
        setError(null);
      } catch (error) {
        console.error("Delete error:", error);
        setError(`Failed to delete message: {error.message}`);
      }
    }
  };

  const handleDeleteChat = async (chatIndex) => {
    const messages = chatHistory[chatIndex].messages;
    if (messages.length > 0 || (messages.length === 0 && chatHistory[chatIndex].topic.trim())) {
      setShowDeleteConfirm({ visible: true, type: 'chat', index: chatIndex, messageIndex: null });
    } else {
      try {
        await axios.post("/api/delete_chat", {
          user_id: user.id,
          chat_index: chatIndex,
        }, { headers: { "Content-Type": "application/json" } });
        const updatedChatHistory = [...chatHistory];
        updatedChatHistory.splice(chatIndex, 1);
        setChatHistory(updatedChatHistory);
        setCurrentChatIndex(updatedChatHistory.length > 0 ? 0 : -1);
        setError(null);
      } catch (error) {
        console.error("Delete chat error:", error);
        setError(`Failed to delete chat: {error.message}`);
      }
    }
  };

  const confirmDelete = async () => {
    if (showDeleteConfirm.type === 'chat') {
      try {
        await axios.post("/api/delete_chat", {
          user_id: user.id,
          chat_index: showDeleteConfirm.index,
        }, { headers: { "Content-Type": "application/json" } });
        const updatedChatHistory = [...chatHistory];
        updatedChatHistory.splice(showDeleteConfirm.index, 1);
        setChatHistory(updatedChatHistory);
        setCurrentChatIndex(updatedChatHistory.length > 0 ? 0 : -1);
        setError(null);
      } catch (error) {
        console.error("Delete chat error:", error);
        setError(`Failed to delete chat: {error.message}`);
      }
    } else if (showDeleteConfirm.type === 'message') {
      try {
        await axios.post("/api/delete_message", {
          user_id: user.id,
          chat_index: showDeleteConfirm.index,
          message_index: showDeleteConfirm.messageIndex,
        }, { headers: { "Content-Type": "application/json" } });
        const updatedChatHistory = [...chatHistory];
        updatedChatHistory[showDeleteConfirm.index].messages.splice(showDeleteConfirm.messageIndex, 1);
        setChatHistory(updatedChatHistory);
        setError(null);
      } catch (error) {
        console.error("Delete error:", error);
        setError(`Failed to delete message: {error.message}`);
      }
    }
    setShowDeleteConfirm({ visible: false, type: '', index: null, messageIndex: null });
  };

  const cancelDelete = () => {
    setShowDeleteConfirm({ visible: false, type: '', index: null, messageIndex: null });
  };

  const formatResponse = (text) => {
    if (!text) return <p className="response-text">No content available</p>;
    const textStr = typeof text === "string" ? text : JSON.stringify(text);
    const lines = textStr.split("\n").filter(line => line.trim());
    let currentSection = "";
    let formattedContent = [];
    let videoLink = null;

    console.log("Raw response text:", textStr); // Debug log

    lines.forEach((line, index) => {
      const trimmedLine = line.trim();
      if (trimmedLine.startsWith("##")) {
        currentSection = trimmedLine.replace("## ", "");
        formattedContent.push(<h2 key={index} className="response-header">{currentSection}</h2>);
      } else if (trimmedLine.startsWith("- ")) {
        const content = trimmedLine.replace("- ", "");
        if (content.includes(":")) {
          formattedContent.push(<p key={index} className="response-subtext">{content}</p>);
        } else {
          formattedContent.push(<ul key={index} className="response-list"><li className="list-item">{content}</li></ul>);
        }
      } else if (trimmedLine.startsWith("+ ")) {
        const content = trimmedLine.replace("+ ", "");
        formattedContent.push(<ul key={index} className="response-list"><li className="list-subitem">{content}</li></ul>);
      } else if (trimmedLine.startsWith("[Watch a video")) {
        console.log("Detected video link:", trimmedLine); // Debug log
        videoLink = <a key={index} href={trimmedLine.match(/\((.*?)\)/)[1]} target="_blank" rel="noopener noreferrer">{trimmedLine}</a>;
      } else if (trimmedLine) {
        formattedContent.push(<p key={index} className="response-subtext">{trimmedLine}</p>);
      }
    });

    return (
      <>
        {formattedContent}
        {videoLink && <div>{videoLink}</div>} {/* Ensure videoLink is rendered */}
      </>
    );
  };

  if (!isLoggedIn) return <Login onLogin={handleLogin} />;

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-left">
          <button className="sidebar-toggle" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
            {isSidebarOpen ? "◄" : "►"}
          </button>
          <h1 className="app-title">MedGenie</h1>
        </div>
        <div className="header-right">
          <span className="user-name">{user.username}</span>
          <button className="new-chat-btn" onClick={handleNewChat}>New Chat</button>
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        </div>
      </header>
      <div className="main-layout">
        <aside className={`sidebar ${isSidebarOpen ? "open" : "closed"}`}>
          <h2>Chat History</h2>
          {chatHistory.length === 0 ? (
            <p className="no-chats">No chats yet</p>
          ) : (
            chatHistory.map((chat, index) => (
              <div
                key={index}
                className={`chat-item ${index === currentChatIndex ? "active" : ""}`}
                onClick={() => switchChat(index)}
              >
                <span className="chat-topic">{chat.topic}</span>
                <button
                  className="delete-chat-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteChat(index);
                  }}
                >
                  Delete
                </button>
              </div>
            ))
          )}
        </aside>
        <main className="chat-area">
          <div className="feature-tabs">
            {["chat", "general", "report", "prescription", "calendar"].map((feature) => (
              <button
                key={feature}
                className={`tab-btn ${selectedFeature === feature ? "active" : ""}`}
                onClick={() => setSelectedFeature(feature)}
              >
                {feature.charAt(0).toUpperCase() +
                  feature
                    .slice(1)
                    .replace("general", "General Diagnosis")
                    .replace("report", "Report Analyzer")
                    .replace("prescription", "Prescription Reader")
                    .replace("calendar", "Calendar Reminder")}
              </button>
            ))}
          </div>
          <div className="messages-container">
            {currentChatIndex === -1 ? (
              <div className="placeholder">Select or start a new conversation</div>
            ) : (
              chatHistory[currentChatIndex].messages.map((msg, index) => (
                <div key={index} className={`message ${msg.role}`}>
                  {msg.role === "system" ? (
                    <div className="system-message">{msg.content || "System message"}</div>
                  ) : (
                    <>
                      <div className="message-content">
                        {editState.index === index ? (
                          <div className="edit-container">
                            <input
                              type="text"
                              value={editState.content}
                              onChange={(e) => setEditState({ ...editState, content: e.target.value })}
                              autoFocus
                              className="edit-input"
                            />
                            <div className="edit-actions">
                              <button onClick={() => handleSaveEdit(currentChatIndex, index)}>Save</button>
                              <button onClick={() => handleSendEditedQuery(currentChatIndex, index)}>Send</button>
                              <button onClick={() => setEditState({ index: null, content: "" })}>Cancel</button>
                            </div>
                          </div>
                        ) : (
                          formatResponse(msg.content)
                        )}
                      </div>
                      {editState.index !== index && (
                        <div className="message-actions">
                          <button onClick={() => handleEdit(currentChatIndex, index)}>Edit</button>
                          <button onClick={() => handleDeleteMessage(currentChatIndex, index)}>Delete</button>
                        </div>
                      )}
                    </>
                  )}
                </div>
              ))
            )}
            {error && <div className="error-message">{error}</div>}
          </div>
          <div className="input-section">
            {selectedFeature === "chat" || selectedFeature === "general" ? (
              <>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSend(e)}
                  placeholder={selectedFeature === "chat" ? "Ask a medical question..." : "Describe symptoms..."}
                  className="input-field"
                />
                <button
                  className={`mic-btn ${isRecording ? "recording" : ""}`}
                  onClick={isRecording ? stopRecording : startRecording}
                >
                  {isRecording ? "■" : "🎤"}
                </button>
              </>
            ) : selectedFeature === "report" || selectedFeature === "prescription" ? (
              <input
                type="file"
                onChange={(e) => setFile(e.target.files[0] || null)}
                accept={selectedFeature === "report" ? ".pdf" : "image/*"}
              />
            ) : (
              <div className="calendar-inputs">
                <input
                  type="text"
                  placeholder="Reminder (e.g., Take ibuprofen)"
                  value={calendarEvent.summary}
                  onChange={(e) => setCalendarEvent({ ...calendarEvent, summary: e.target.value })}
                />
                <input
                  type="date"
                  value={calendarEvent.date}
                  onChange={(e) => setCalendarEvent({ ...calendarEvent, date: e.target.value })}
                />
                <input
                  type="time"
                  value={calendarEvent.time}
                  onChange={(e) => setCalendarEvent({ ...calendarEvent, time: e.target.value })}
                />
              </div>
            )}
            <button onClick={handleSend}>Send</button>
          </div>
        </main>
      </div>
      {showDeleteConfirm.visible && (
        <div className="modal">
          <div className="modal-content">
            <h3>Confirm Deletion</h3>
            <p>Are you sure you want to delete this {showDeleteConfirm.type}?</p>
            <div className="modal-actions">
              <button onClick={confirmDelete}>Yes</button>
              <button onClick={cancelDelete}>No</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;