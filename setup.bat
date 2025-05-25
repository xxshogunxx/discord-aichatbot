@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo.
echo 🧠 Setting up DisGoat AI Discord Bot...
echo =======================================
echo.

:: Step 1: Check Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed. Please install Python 3.10 or later from https://python.org
    pause
    exit /b
)

:: Step 2: Install Python dependencies
echo 🔄 Installing Python libraries...
pip install -r requirements.txt

:: Step 3: Check if Ollama is installed
where ollama >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Ollama not found. Please install it from https://ollama.com/download
    pause
    exit /b
)

:: Step 4: Start Ollama server (background)
echo 🚀 Starting Ollama server...
start /min cmd /k "ollama serve"

:: Step 5: Pull required models
echo 🧠 Pulling LLMs: mistral and llava...
ollama pull mistral
ollama pull llava

:: Step 6: Prompt for .env configuration
IF NOT EXIST .env (
    echo DISCORD_TOKEN=your_token_here> .env
    echo NEWSAPI_KEY=your_newsapi_key_here>> .env
    echo ⚠️  Please update your .env file with your real Discord token and NewsAPI key.
    pause
    exit /b
)

:: Step 7: Run the bot
echo ✅ Launching the DisGoat bot...
python bot.py