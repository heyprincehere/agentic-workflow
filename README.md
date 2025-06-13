# Agentic Workflow with LangGraph + Claude + Streamlit

### This project demonstrates an AI agentic workflow using LangGraph, Claude 3 via OpenRouter, and Streamlit — capable of planning, refining, executing, and reflecting on tasks.

### Built for intelligent task execution with retry logic, autonomy, and an interactive web UI.

### 📚 Table of Contents

- ✨ Features
- 🧠 Architecture
- 🖥️ Demo (Streamlit)
- ⚙️ Setup Instructions
- 📦 Requirements
- 📸 Screenshot (Optional)
- 👨‍💻 Author

### Features

- 🧠 Planner Agent – Breaks your task into 3–5 subtasks  
- 🔧 Refiner Agent – Cleans and improves subtasks  
- 🤖 Tool Agent – Completes each task using Claude 3  
- 🔁 Reflection Agent – Evaluates and retries if needed  
- 🖥️ Streamlit Web UI – Clean interface for interaction  
- ✅ OpenRouter Integration – Fast Claude 3 Haiku access  

### Architecture

User Input → Planner Agent → Refiner Agent → Tool Agent → Reflection Agent  
If good → Done  
If retry → Loop back to Tool Agent

### Demo (Streamlit)

Start the interactive agent web UI:

    streamlit run streamlit_app.py

Try a task like:

    Plan a sustainability campaign for high school students

The app will return a complete multi-step plan, reviewed and improved using agent feedback loops.

### Setup Instructions

1. Clone this repository:

    git clone https://github.com/your-username/agentic-workflow.git
    cd agentic-workflow

2. Install dependencies:

    pip install -r requirements.txt

3. Create a .env file with your API key:

    OPENROUTER_API_KEY=your_openrouter_key_here

4. Run it:

    streamlit run streamlit_app.py

### Requirements

Make sure these libraries are installed:

    langgraph
    langchain
    openai
    python-dotenv
    streamlit

Generate requirements.txt:

    pip freeze > requirements.txt

👨‍💻 Author

Prince Janiya  
Powered by Claude 3 Haiku + LangGraph + OpenRouter  
Built with curiosity

