# 🥑 TastyTalk - AI Food & Nutrition Assistant

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **TastyTalk** is a modern, interactive, AI-driven nutrition & dietetics assistant. Built with Streamlit, Google Gemini multimodal AI models, and MongoDB, it provides personalized dietary analysis, food plate photo scanner, conversational coaching, and clinic-ready PDF report generation.

---

## ✨ Features

- 💬 **Interactive AI Dietitian Chat**: Real-time streaming consultation powered by Gemini with customizable tone presets (Encouraging, Strict Clinical, Fitness Coach, Culinary Chef).
- 📸 **Vision Food Plate Scanner**: Upload meal photos to analyze ingredients, portion estimates, calories, macro splits (Proteins/Carbs/Fats), and actionable health advice.
- 🎨 **Luxury Glassmorphism UI**: High-end dark aesthetic, Bento grid feature cards, 3D animated NutriBot mascot, and a modern floating dock navigation.
- 📊 **Clinic-Ready PDF & Report Export**: Export structured dietary consultations with summary metric badges and formatted data tables.
- 💾 **MongoDB Multi-Session Persistence**: Store, retrieve, rename, and manage multiple consultation sessions seamlessly.
- ⚡ **Auto-Fallback Engine**: Multi-tiered resilience with support for Gemini 3.6 Flash, Gemini 3.5 Flash Lite, and latest models.

---

## 🗂️ Project Structure

```text
TastyTalk/
├── assets/
│   └── mascot.jpg               # 3D NutriBot Chef mascot image
├── backend/
│   ├── ai_service.py            # Gemini text streaming and dietitian persona
│   ├── export_service.py        # Magazine-style PDF & structured text export
│   └── vision_service.py        # Food plate image scanner & nutrition analyzer
├── config/
│   └── settings.py              # Centralized environment, model, & theme configurations
├── database/
│   ├── connection.py            # MongoDB singleton connection pool
│   └── session_repo.py          # Session and message CRUD operations
├── frontend/
│   ├── components/
│   │   ├── chat_view.py         # AI consultation stream & chat interface
│   │   ├── header.py            # App top branding & status indicators
│   │   ├── home_view.py         # Bento grid home view & quick action chips
│   │   ├── sidebar.py           # Session history, settings, & tone controls
│   │   └── vision_view.py       # Food plate photo scanner interface
│   └── styles.py                # Luxury CSS theme, animations, and glassmorphism styles
├── .env.example                 # Environment variables template
├── .gitignore                   # Ignore sensitive keys and virtual envs
├── Food.py                      # Main entrypoint and navigation router
└── requirements.txt             # Project dependencies
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Google Gemini API Key** (Get free at [Google AI Studio](https://aistudio.google.com/apikey))
- **MongoDB** (Local instance or [MongoDB Atlas](https://www.mongodb.com/atlas))

### 2. Clone the Repository
```bash
git clone https://github.com/honeyp11/TastyTalk-.git
cd TastyTalk-
```

### 3. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory (or copy from `.env.example`):
```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=food_nutrition_db
```

### 6. Run the Application
```bash
streamlit run Food.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) with Custom Glassmorphism CSS & SVG Icons
- **AI Brain**: [Google Gemini GenAI SDK](https://github.com/google/google-genai) (`gemini-3.6-flash`, `gemini-3.5-flash-lite`)
- **Database**: [MongoDB](https://www.mongodb.com/) via `pymongo`
- **PDF Generation**: [FPDF2](https://pyfpdf.github.io/fpdf2/)
- **Image Processing**: [Pillow](https://python-pillow.org/)

---

## 🔒 Security Notice
Make sure never to commit your actual `.env` file containing API keys. A pre-configured `.gitignore` is included in this repository to prevent accidental leaks.

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
