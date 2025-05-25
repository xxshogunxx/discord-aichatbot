
import discord
import requests
import os
import time
import base64
import yfinance as yf
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

def query_ollama(prompt: str, model="mistral"):
    try:
        start = time.time()
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=180
        )
        res.raise_for_status()
        print(f"⏱️ Mistral responded in {time.time() - start:.2f}s")
        return res.json().get("response", "⚠️ No response from Ollama.")
    except Exception as e:
        return f"⚠️ Ollama error: {e}"

def query_ollama_with_image(prompt, image_bytes, model="llava"):
    try:
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "images": [encoded], "stream": False},
            timeout=300
        )
        res.raise_for_status()
        return res.json().get("response", "⚠️ No visual response.")
    except Exception as e:
        return f"⚠️ LLaVA error: {e}"

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if msg.attachments:
        for a in msg.attachments:
            if a.content_type and a.content_type.startswith("image/"):
                await msg.channel.send("📷 Analyzing image with LLaVA...")
                image = await a.read()
                result = query_ollama_with_image("Describe this image in detail.", image)
                await msg.channel.send(result[:2000])
                return
    await bot.process_commands(msg)

@bot.command()
async def finance(ctx, *, query):
    if query.lower().startswith("analyze "):
        symbol = query.split("analyze ")[-1].strip().upper()
        await ctx.send(f"📊 Analyzing **{symbol}** as a stock...")

        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price = info.get("regularMarketPrice", "N/A")
            pe = info.get("trailingPE", "N/A")
            eps = info.get("trailingEps", "N/A")
            market_cap = info.get("marketCap", "N/A")
            summary = info.get("longBusinessSummary", "")

            stock_summary = (
                f"Company: {info.get('shortName', symbol)}\n"
                f"Price: ${price} | P/E Ratio: {pe} | EPS: {eps}\n"
                f"Market Cap: {market_cap}\n\n"
                f"Business Summary: {summary[:500]}..."
            )
        except Exception as e:
            await ctx.send(f"❌ Could not fetch stock data: {e}")
            return

        try:
            query_str = f"{symbol} stock OR {symbol} earnings OR {symbol} market"
            url = f"https://newsapi.org/v2/everything?q={query_str}&sortBy=publishedAt&pageSize=3&language=en&domains=cnbc.com,bloomberg.com,marketwatch.com&apiKey={NEWSAPI_KEY}"
            res = requests.get(url)
            articles = res.json().get("articles", [])
            if not articles:
                news_summary = "No news found."
            else:
                headlines = "\n".join([f"{i+1}. {a['title']} - {a['url']}" for i, a in enumerate(articles)])
                news_summary = f"Top News Headlines:\n{headlines}"
        except Exception as e:
            news_summary = f"❌ Could not fetch news: {e}"

        final_prompt = (
            f"Analyze the stock {symbol} based on the following data:\n\n"
            f"{stock_summary}\n\n{news_summary}\n\n"
            f"Give a 3–5 sentence investment summary. Be objective."
        )
        response = query_ollama(final_prompt)
        await ctx.send(f"**📈 Investment Analysis:**\n{response[:2000]}")
    else:
        prompt = f"You are a financial expert. Answer this question:\n\n{query}"
        result = query_ollama(prompt)
        await ctx.send(result[:2000])

@bot.command()
async def news(ctx, *, symbol):
    await ctx.send(f"📰 Getting news for {symbol.upper()}...")
    query = f"{symbol.upper()} stock OR {symbol.upper()} earnings OR {symbol.upper()} market"
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize=1&sortBy=publishedAt&language=en&domains=cnbc.com,bloomberg.com,marketwatch.com&apiKey={NEWSAPI_KEY}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        articles = res.json().get("articles", [])
        if not articles:
            await ctx.send("⚠️ No financial news found.")
            return
        a = articles[0]
        title, desc, link = a["title"], a["description"], a["url"]
        prompt = f"Summarize the following financial news in 3–5 short sentences:\n\nTitle: {title}\nDescription: {desc}"
        summary = query_ollama(prompt)
        await ctx.send(f"**🧠 Summary:**\n{summary}\n\n🔗 {link}")
    except Exception as e:
        await ctx.send(f"❌ Error fetching news: {e}")

@bot.command()
async def price(ctx, *, symbol):
    try:
        ticker = yf.Ticker(symbol.upper())
        price = ticker.info.get("regularMarketPrice", "N/A")
        change = ticker.info.get("regularMarketChangePercent", 0.0)
        await ctx.send(f"💹 {symbol.upper()} is at **${price}** ({change:.2f}%)")
    except Exception as e:
        await ctx.send(f"❌ Price lookup failed: {e}")

@bot.command()
async def compare(ctx, *, symbols):
    await ctx.send(f"📊 Comparing: {symbols}")
    prompt = f"Compare these two assets in terms of growth, risk, valuation, and investment potential: {symbols}"
    result = query_ollama(prompt)
    await ctx.send(result[:2000])

@bot.command()
async def help(ctx):
    await ctx.send(
        "**🤖 DisGoat Commands:**\n"
        "`!finance analyze <symbol>` – Analyze stock with live data + news\n"
        "`!finance <question>` – Ask a finance question\n"
        "`!price <symbol>` – Get real-time stock price\n"
        "`!news <symbol>` – Get latest financial news\n"
        "`!compare <stock1 vs stock2>` – Compare 2 assets\n"
        "`(Upload image)` – I'll analyze and describe it"
    )

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")

bot.run(TOKEN)
