## Codalyze
AI-Powered Code Review Assistant
Codalyze is an intelligent code review platform that uses AI to analyze, review, and automatically fix code.
It helps developers catch mistakes, improve code quality, and generate suggestions for better coding practices in real-time.

## 📸 Screenshots

### Home Page

![Login Screen](static\images\Home.png)

### AI Suggestions

![Suggestions](static\images\Suggestion.png)



🚀 Features
🧠 AI-Powered Code Review
Analyzes code using AI to detect errors, bad practices, and improvements.

Provides detailed suggestions to enhance code quality.

🔧 AI Auto-Fix
Automatically generates corrected versions of the input code.

Helps beginners learn better coding patterns.

📝 Multiple Input Methods
Text Input: Paste code directly into the interface.

File Upload: Upload .py files for review.

📄 PDF Export
Download the AI-generated review and corrections as a professional PDF report.

🔐 User Authentication
Register and log in securely using encrypted passwords with Flask-Bcrypt.

🖥️ Modern UI
Clean and intuitive interface inspired by professional code analyzers like Codacy or SonarQube.

🔁 Refresh Button
Clear previous code, suggestions, and fixed code with a single click.

🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Python (Flask)
Database: PostgreSQL (via SQLAlchemy)
AI Model: Google Gemini 2.0 Flash Lite (via API)
Deployment: Render

⚙️ Installation Guide
Step 1️⃣: Clone the Repository
```bash
git clone https://github.com/yourusername/codalyze.git
cd codalyze
```
Step 2️⃣: Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   
```
Step 3️⃣: Install Dependencies
```bash
pip install -r requirements.txt
```
Step 4️⃣: Configure Environment Variables
Create a .env file in the root directory and add:
```bash
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_flask_secret_key
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=codalyze_db
POSTGRES_USER=your_postgres_username
POSTGRES_PASSWORD=your_postgres_password
```
⚠️ Note: Replace these values with your actual API keys and database credentials.

Step 5️⃣: Run the Application
```bash
flask run
```