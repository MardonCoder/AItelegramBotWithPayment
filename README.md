# AItelegramBotWithPayment
This is AI telegram bot with implemented payment system based on Uzbekistan payment system CLICK. AI on opeanAI library and requires working api_key with balance on it. TG bot on aiogram

# Scoopy AI Bot for SMM Specialists

**Scoopy** is a Telegram bot built with Aiogram and OpenAI that helps SMM specialists:

- Design sales funnels  
- Write post descriptions  
- Analyze competitors  
- Manage balance and purchase additional “coins”

---

## 📋 Contents

1. [Features](#-features)  
2. [Requirements](#-requirements)  
3. [Installation](#-installation)  
4. [Configuration](#-configuration)  
5. [Running the Bot](#-running-the-bot)  
6. [Usage](#-usage)  
7. [Project Structure](#-project-structure)  
8. [Ignored Files](#-ignored-files)  
9. [License](#-license)

---

## 🚀 Features

- **User Registration** — grants starter coins on first `/start` and `/help`  
- **Balance Inquiry** — `/balance` shows current coin balance  
- **Top‑Up** — choose an amount to pay via Click invoice and receive coins  
- **AI Chat** — powered by OpenAI (`gpt-4o-mini`) with token‑based billing  
- **Token Accounting** — deducts coins based on input and output token usage  

---

## 🛠 Requirements

- Python ≥ 3.9  
- Dependencies: Aiogram, AiOSQLite, python-dotenv, openai, etc.  

---

## ⚙️ Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/your-username/Scoopy-bot.git
   cd Scoopy-bot
Create and activate a virtual environment

python -m venv .venv
source .venv/bin/activate    # Linux / macOS
.venv\Scripts\activate       # Windows



Install dependencies


pip install -r requirements.txt



🔧 Configuration
Copy .env.example to .env

Open .env and fill in your keys:


BOT_TOKEN=<your Telegram token>
OPENAI_API_KEY=<your OpenAI key>
CLICK_TEST_TOKEN=<your Click test token>



Ensure you have a config.py that reads these variables:

import os



from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLICK_TEST_TOKEN = os.getenv("CLICK_TEST_TOKEN")
DB_NAME = "users.db"



▶️ Running the Bot
In the project root, run:

python main.py
This will initialize the database and start polling with dp.start_polling().

💬 Usage
/start — register and receive a welcome message

/help — show instructions and get starter coins

/balance — check your coin balance

/pay — open the payment menu

Any text message (if you have ≥ 750 coins) is sent to GPT and billed accordingly

📁 Project Structure
.
├── .env.example
├── .gitignore
├── config.py
├── main.py
├── AIscript.py       # GPTChat class
├── database.py       # init_db, add_user, get_balance, update_balance, reset_balance
├── requirements.txt
└── users.db          # SQLite file (ignored by Git)



🚫 Ignored Files
Your .gitignore should include:

# Environment variables
.env

# Database files
*.db
users.db
