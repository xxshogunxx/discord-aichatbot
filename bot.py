
import discord
import requests
import os
import base64
import time
import yfinance as yf
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv
from googlesearch import search

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

if not TOKEN:
    raise ValueError("❌ DISCORD_TOKEN not found or invalid in .env file.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

COMPANY_ALIASES = {
    "apple": "AAPL",
    "amazon": "AMZN",
    "google": "GOOG",
    "alphabet": "GOOG",
    "meta": "META",
    "facebook": "META",
    "tesla": "TSLA",
    "microsoft": "MSFT",
    "nvidia": "NVDA",
    "netflix": "NFLX",
    "intel": "INTC",
    "amd": "AMD"
}

def query_ollama(prompt: str, model="mistral"):
    try:
        start = time.time()
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=180
        )
        res.raise_for_status()
        print(f"🧠 Ollama responded in {time.time() - start:.2f}s")
        return res.json().get("response", "⚠️ No response from Ollama.")
    except Exception as e:
        return f"⚠️ Ollama error: {e}"

def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        price = info.get("regularMarketPrice")
        change = info.get("regularMarketChangePercent", 0)
        return f"💹 {symbol.upper()} is trading at ${price:.2f} ({change:.2f}%)"
    except:
        return "⚠️ Could not retrieve stock price."

def google_search_summary(query):
    try:
        urls = list(search(query, num_results=2))
        summaries = []
        for url in urls:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            text = " ".join(p.get_text() for p in soup.find_all("p"))
            if len(text) > 2000:
                text = text[:2000]
            prompt = f"Summarize this news article in 3-4 lines:\n\n{text}"
            answer = query_ollama(prompt)
            summaries.append(f"🔗 {url}\n{answer}")
        return "\n\n".join(summaries)
    except Exception as e:
        return f"⚠️ Web scraping failed: {e}"

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return

    user_input = msg.content.strip().lower()
    found_symbols = []

    tokens = user_input.split()
    for token in tokens:
        if token.startswith("$") and len(token) <= 6:
            found_symbols.append(token[1:].upper())

    for company, symbol in COMPANY_ALIASES.items():
        if company in user_input:
            found_symbols.append(symbol)

    found_symbols = list(set(found_symbols))

    if found_symbols:
        for symbol in found_symbols:
            price = get_stock_price(symbol)
            scraped = google_search_summary(f"{symbol} stock news site:cnbc.com OR site:bloomberg.com OR site:marketwatch.com")
            await msg.channel.send(f"{price}\n\n{scraped}")
        return

    if msg.attachments:
        for a in msg.attachments:
            if a.content_type and a.content_type.startswith("image/"):
                image_bytes = await a.read()
                encoded = base64.b64encode(image_bytes).decode("utf-8")
                res = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "llava", "prompt": "Describe this image.", "images": [encoded], "stream": False},
                    timeout=300
                )
                result = res.json().get("response", "⚠️ Couldn't analyze the image.")
                await msg.channel.send(result[:2000])
                return

    response = query_ollama(f"You are a financial chatbot. Answer naturally:\n\n{msg.content}")
    await msg.channel.send(response[:2000])

@bot.event
async def on_ready():
    print(f"✅ DisGoat ChatBot is live as {bot.user.name}")

bot.run(TOKEN)
