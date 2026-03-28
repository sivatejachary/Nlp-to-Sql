---
license: mit
title: Nlp-to-Sql
sdk: docker
emoji: 🚀
colorFrom: green
colorTo: red
---
# 🧠 NL-to-SQL Chatbot (Clinic Database)

## 📌 Project Description

This project is a Natural Language to SQL (NL-to-SQL) system that allows users to ask questions in plain English and retrieve data from a structured database.

This project is fully containerized using Docker and can run without manual setup.

---

## ⚙️ Tech Stack

- Python
- FastAPI
- SQLite
- Google Gemini (LLM)
- Vanna (for architecture)

---

## 🏗️ Project Structure

├── main.py              # FastAPI application  
├── setup_database.py   # Create DB + insert dummy data  
├── seed_memory.py      # Memory seeding script  
├── vanna_setup.py      # Agent setup     
├── sql_validator.py    # SQL validation  
├── requirements.txt  
└── clinic.db  

---

## 🚀 Setup Instructions

### 1. Get the project

Download the project from Hugging Face:

https://huggingface.co/spaces/Ai-Thalli/vanna

Or use:

git clone https://github.com/sivatejachary/Nlp-to-Sql
cd Nlp-to-sql

---

### 2. Install dependencies

pip install -r requirements.txt  

---

### 3. Configure environment variables

Create a `.env` file:

GOOGLE_API_KEY=your_gemini_api_key  

---

## 🗄️ Create Database

python setup_database.py  

This will:
- Create all tables  
- Insert dummy data:
  - 200 patients  
  - 15 doctors  
  - 500 appointments  
  - 350 treatments  
  - 300 invoices  

---

## 🧠 Seed Memory

python seed_memory.py  

---

## ▶️ Run API Server

uvicorn main:app --reload  

Server runs at:  
http://127.0.0.1:8000  

---

## 📡 API Documentation

### 🔹 Health Check

GET /health  

Response:

{
  "status": "ok"
}

---

### 🔹 Chat Endpoint

POST /chat  

Request:

{
  "question": "How many patients are there?"
}

Response:

{
  "sql": "SELECT COUNT(*) FROM patients",
  "rows": [[200]]
}

---

## 🏗️ Architecture Overview

 User Question (Natural Language)
         ↓
 FastAPI Backend
         ↓
 Vanna 2.0 Agent
 (Gemini LLM Service + Run SQL Tool + Demo Agent Memory)
         ↓
 SQL Validator
 (Only SELECT queries allowed, no dangerous operations)
         ↓
 SQLite Database Execution
 (Using built-in SqliteRunner)
         ↓
 Response to User
 (Results + Summary + Charts)  

---

## 📊 Features

- Natural language to SQL conversion  
- Uses Gemini for query generation  
- SQL validation (only SELECT queries allowed)  
- Realistic dummy dataset  
- REST API interface  

---

## ⚠️ Limitations

- Complex queries may not always work  
- Depends on LLM accuracy  
- SQLite has limited date functions  

---

## 🎯 Future Improvements

- Improve prompt engineering  
- Add charts / visualization  
- Better handling of complex queries  

---

## 🎉 Conclusion

This project demonstrates how natural language queries can be converted into SQL using Google Gemini and executed on a structured database.

By combining FastAPI, Vanna 2.0, and SQLite, the system provides a simple and efficient way for users to interact with data without writing SQL queries.

The use of SQL validation ensures safe database operations, while Docker support makes the application easy to deploy and run in any environment.
