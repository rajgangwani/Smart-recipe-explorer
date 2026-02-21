# 🍲 Smart Recipe Explorer

Smart Recipe Explorer is a full-stack web application that allows users to manage recipes, perform smart searches, and generate cooking suggestions using an integrated generative AI service.

The application is built using **FastAPI** for the backend and a modern dashboard-style frontend using **HTML, CSS, and JavaScript**.

---

## ✨ Features

### 📌 Recipe Management
- Add new recipes
- View all recipes
- Delete recipes
- Structured storage using SQLAlchemy ORM

### 🔎 Smart Search
- Search recipes by name
- Real-time result count
- Clean and responsive layout

### 🤖 AI Recipe Assistant
- Sidebar chatbot-style assistant
- Generate recipe suggestions based on ingredients
- Fixed assistant panel for seamless experience

### 🎨 Modern UI
- Fixed header navigation
- Scrollable main content
- Fixed AI sidebar
- Glassmorphism dashboard design
- Fully responsive layout

---

## 🛠 Tech Stack

### Backend
- FastAPI
- SQLAlchemy (ORM)
- Pydantic (Data validation)
- SQLite (Database)
- Uvicorn (ASGI Server)

### Frontend
- HTML5
- CSS3 (Custom dashboard styling)
- Vanilla JavaScript (Fetch API)

### AI Integration
- Groq AI API for high-performance LLM-based recipe generation
- Ingredient-driven dynamic recipe suggestions
- Backend-to-AI REST API integration
- Environment-based API key configuration

---

## 📁 Project Structure

```
Smart-Recipe-Explorer/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── services/
│   │   └── ai_service.py
│   └── recipes.db
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
└── README.md
```

---

# ⚙️ Installation & Setup Guide

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/smart-recipe-explorer.git
cd smart-recipe-explorer
```

---

## 2️⃣ Backend Setup

Navigate to backend directory:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv requests
```

Run the server:

```bash
uvicorn main:app --reload
```

Backend will run at:

```
http://127.0.0.1:8000
```

API documentation available at:

```
http://127.0.0.1:8000/docs
```

---

## 3️⃣ AI API Configuration

Open:

```
backend/services/ai_service.py
```

Add your API key:

```python
API_KEY = "your_api_key_here"
```

Or create a `.env` file inside backend:

```
AI_API_KEY=your_api_key_here
```

Load using `python-dotenv` if required.

---

## 4️⃣ Frontend Setup

Navigate to frontend folder.

You can:

- Open `index.html` directly in browser  
OR  
- Use VS Code Live Server extension  

Ensure backend is running before using frontend.

---

# 📡 API Endpoints

### Create Recipe
```
POST /recipes
```

### Get All Recipes
```
GET /recipes
```

### Search Recipes
```
GET /recipes?search=recipe_name
```

### Delete Recipe
```
DELETE /recipes/{id}
```

### Generate AI Suggestion
```
POST /ai/suggest
```

---

# 🧪 How to Test

1. Start backend server  
2. Open frontend  
3. Add a recipe  
4. Search by name  
5. Use AI assistant for suggestions  

---

# 🎯 Design Approach

The application follows a dashboard layout:

- Fixed top navigation
- Scrollable content section
- Fixed AI assistant panel
- Clean and minimal UI
- Modern glass design theme

The structure ensures smooth interaction and clear separation between recipe management and AI assistance.

---

# 🚀 Future Enhancements

- Update recipe functionality
- Category filtering
- Pagination
- Authentication system
- Database upgrade to PostgreSQL
- Deployment on cloud platforms
- Docker support

---

# 👨‍💻 Author

**Raj Gangwani**  
MCA (AI & Data Science)  
Full Stack Developer | Python | FastAPI | AI Integration
