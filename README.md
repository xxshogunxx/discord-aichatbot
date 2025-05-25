
# 🧠 DisGoat AI Discord Bot

An intelligent Discord bot that:
- Analyzes stocks using Yahoo Finance
- Summarizes breaking financial news
- Accepts images and interprets them using LLaVA
- Runs locally via Ollama (no OpenAI key required)

## ✅ Installation

### 1. Requirements
- Python 3.10+
- Git
- Node.js + npm
- [Ollama](https://ollama.com/download) (with `mistral` and `llava` models)

### 2. Install Python Packages

```bash
pip install -r requirements.txt
```

### 3. Set Your `.env` File

```bash
DISCORD_TOKEN=your_discord_token_here
NEWSAPI_KEY=your_newsapi_key_here
```

### 4. Pull Ollama Models

```bash
ollama pull mistral
ollama pull llava
ollama serve
```

### 5. Run the Bot

```bash
python bot.py
```

## ✅ Commands

- `!finance analyze <symbol>` – Full stock analysis
- `!finance <question>` – Ask a financial question
- `!price <symbol>` – Current stock price
- `!news <symbol>` – Recent news + summary
- `!compare <symbol1 vs symbol2>` – Compare two stocks
- *(Upload image)* – LLaVA will describe it

## ✅ Troubleshooting

If you see "Ollama timed out", make sure:
- Ollama is running (`ollama serve`)
- Models are pulled
- Network requests are not blocked by firewall
