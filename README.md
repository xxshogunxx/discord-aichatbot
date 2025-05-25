# discord-aichatbot
This is ai chatbot installed locally on your computer and will connect to Discord acting as your AI chatbot.

🧠 DisGoat AI Discord Bot Setup Guide
Turn any computer into a financial AI assistant that:

Analyzes stocks like a pro 🧾

Summarizes news in real time 📰

Responds to questions and images 📷

Uses local AI models (Ollama + Mistral + LLaVA) — no OpenAI keys required

✅ 1. Prerequisites
Make sure the following software is installed on the system:

🧱 System Requirements
Windows 10/11, macOS, or Linux
At least 8–16 GB RAM (more for LLaVA)
10–20 GB disk space
(Optional but recommended) NVIDIA GPU for Ollama acceleration

📦 Required Tools
Tool	Purpose	Install Command / Link
Python 3.10+	Run the bot	https://www.python.org/downloads/
Git	Clone repo from GitHub	https://git-scm.com/downloads
Node.js + npm	Needed by Ollama	https://nodejs.org
Ollama	Run local AI models	https://ollama.com/download
Discord account	Register the bot	https://discord.com/developers/applications
NewsAPI key	Pull financial headlines	https://newsapi.org (free sign-up)

✅ 2. Install Required Python Packages
After cloning the bot repo, run:

bash
Copy
Edit
pip install -r requirements.txt
If you don’t have a requirements.txt, install them manually:

bash
Copy
Edit
pip install discord.py requests yfinance python-dotenv
✅ 3. Setup Ollama + Models
🧠 Install Ollama
Download and install from:
👉 https://ollama.com/download

🧠 Pull Required Models
After installing Ollama, open a terminal and run:

bash
Copy
Edit
ollama pull mistral
ollama pull llava
Start the local model server:

bash
Copy
Edit
ollama serve
✅ 4. Configure Environment Variables
Create a .env file in the same folder as bot.py:

ini
Copy
Edit
DISCORD_TOKEN=your_discord_bot_token_here
NEWSAPI_KEY=your_newsapi_key_here
To create your bot token:

Go to Discord Developer Portal

Create a new bot

Copy the token and paste it into .env

To get a free NewsAPI key:
👉 https://newsapi.org/register

✅ 5. Run the Bot
Make sure Ollama is running (ollama serve), then run the bot:

bash
Copy
Edit
python bot.py
If successful, you’ll see:

pgsql
Copy
Edit
✅ Logged in as DisGoat
✅ 6. Available Commands
Command	Function
!finance analyze AAPL	Full stock analysis (live data + news)
!finance <question>	Ask any financial or economic question
!price <symbol>	Get current stock price
!news <symbol>	Summarized news + link
!compare TSLA vs GM	Compares 2 stocks
(Upload image)	LLaVA analyzes the content
!help	Show all commands

🛠️ Optional: Run Automatically on Boot (Windows)
Create a .bat file with:

bat
Copy
Edit
start /min cmd /k "cd C:\\path\\to\\bot && ollama serve"
start /min cmd /k "cd C:\\path\\to\\bot && python bot.py"
Place it in your Startup folder:
C:\Users\<yourname>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

🧪 Troubleshooting
Problem	Fix
Bot doesn’t respond	Check .env tokens and permissions
“Ollama not ready”	Wait a few seconds after launching
Mistral too slow	Use smaller models (e.g., gemma:2b)
LLaVA missing image reply	Ensure image is JPG/PNG and model is pulled
