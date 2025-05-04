# Masterblog-API – A Modern Blog with Flask & REST API

This is a learning project built with Python and Flask, featuring a REST API backend and a modern frontend.  
It demonstrates the implementation of a blog system with complete CRUD functionality and API documentation.

## 🔧 Features

- RESTful API with Swagger documentation
- Modern frontend with real-time updates
- Complete CRUD operations for blog posts
- Advanced error handling and validation
- Data stored in JSON file
- CORS support for cross-origin requests
- Clean, responsive styling with CSS
- No database required

## 🛠️ Installation & Running

### Requirements

- Python 3.x
- Flask and extensions (see `requirements.txt`)

### Run Locally

```bash
git clone https://github.com/Rei1000/Masterblog-API.git
cd Masterblog-API
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Start the backend:
```bash
python backend/backend_app.py
```

Start the frontend:
```bash
python frontend/frontend_app.py
```

Then open in your browser:  
Frontend: [http://localhost:5001](http://localhost:5001)  
Backend API: [http://localhost:5002/api](http://localhost:5002/api)  
API Documentation: [http://localhost:5002/api/docs](http://localhost:5002/api/docs)

## 📁 Project Structure

```
Masterblog-API/
│
├── backend/
│   ├── backend_app.py    # Main Flask API
│   └── static/          # API documentation
│       └── swagger.json
│
├── frontend/
│   ├── frontend_app.py   # Frontend server
│   ├── static/
│   │   ├── main.js      # Frontend logic
│   │   └── styles.css   # Styling
│   └── templates/
│       └── index.html   # Main page
│
├── posts.json           # Data storage
└── requirements.txt     # Dependencies
```

## 🧠 Purpose

This project demonstrates modern web development concepts:
- RESTful API design
- Frontend-Backend separation
- API documentation with Swagger
- CORS handling
- JSON data processing
- Comprehensive error handling
- Modern JavaScript fetch API
- Real-time UI updates

## 📌 Note

This project focuses on clean API design and modern frontend-backend interaction.  
It uses a JSON file for simplicity but could be easily extended to use a database.

---
**Happy coding with Flask and REST APIs!** 