# 💬 SAB-IA — Your Smart Banking Assistant  
**Innovation Banking Hack Fest 2025**  
🚀 *Making financial management as easy as talking.*

---

## 🧠 Overview
**SAB-IA** (short for *Sabadell Intelligent Assistant*) is a multimodal AI-powered banking assistant designed to make digital banking **inclusive, accessible, and secure** for everyone — especially for people with visual or cognitive disabilities.  

💡 Our goal: make managing your money as simple as having a conversation.

---

## 🌍 Key Features

### ♿ Inclusive Design
- Fully voice-driven interface with **speech-to-text** and **text-to-speech** support.  
- Simplified, intuitive navigation through natural spoken commands.  
- Multilingual accessibility with automatic **Spanish ↔ Valencian translation** using **ALIA**.  

### 🤖 Artificial Intelligence
- Intent recognition system that classifies user messages as:
  - 🗣️ *Message* – general inquiries  
  - ⚙️ *Action* – in-app navigation or transactions  
  - 🚨 *Fraud* – suspicious activity detection  
- Dynamic and adaptive conversation flow via **n8n AI workflows**.  
- Natural interaction through integrated **Gemini** and **ALIA** APIs.  

### 🔒 Cybersecurity
- Secure authentication and operation confirmation.  
- Built-in **fraud detection agent**.  
- Safe handling of user data through **FastAPI** backend endpoints.  

---

## 🧩 System Architecture

### 🖥️ Frontend
- Developed with **HTML**, **CSS**, **JavaScript**, **XML**, and **Kotlin**.  
- Replicates Banco Sabadell’s interface with a **custom AI assistant**.  
- Allows users to chat or speak directly to SAB-IA for navigation and financial actions.  

### ⚙️ AI Flow (n8n Cloud)
- Core logic flow hosted in **n8n Cloud**.  
- Classifies input messages and routes them to specialized agents:
  - Message agent → informative responses  
  - Action agent → in-app navigation  
  - Fraud agent → alert detection  
- Each agent executes autonomous and context-aware actions.  

### 🧠 Backend (FastAPI)
- Serves as the communication bridge between the frontend and AI flow.  
- Manages:
  - 🗣️ **STT (Speech-to-Text)** via Gemini API  
  - 🔊 **TTS (Text-to-Speech)** via Gemini TTS model  
  - 🌐 **ALIA Translation** for accessibility  
- Implemented with **Python**, modular and easy to expand.  

---

## 🧠 AI Models Used

| Model | Description | Platform |
|:------|:-------------|:----------|
| **Gemini 2.5 Flash** | Converts voice ↔ text in real time | Google GenAI |
| **ALIA (Aitana-TA-2B-S)** | Translates Spanish ↔ Valencian for accessibility | Hugging Face |
| **n8n Agent Flow** | Manages message classification & responses | n8n Cloud |

---

## 🧑‍💻 Implementation Highlights

### 🧩 Backend Components
```bash
📦 Backend/
├── main.py            # Orchestrates the full backend workflow
├── server.py          # Handles API communication between modules
├── stt.py             # Speech-to-Text conversion using Gemini
├── tts.py             # Text-to-Speech synthesis
├── ALIA.py            # Spanish ↔ Valencian translation via Hugging Face
└── n8n_connector.py   # Connects FastAPI backend with n8n flow
