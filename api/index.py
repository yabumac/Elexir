import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- CONFIGURATION ---
# Use an environment variable for security!
BOT_TOKEN = os.getenv("BOT_TOKEN")

COURSES = [
    {"name": "Classroom Management in Crisis Affected Settings", "url": "https://app.mindsmith.ai/learn/cmni0my3602i8jf0488x6j9ji"},
    {"name": "Career Employability Skills", "url": "https://app.mindsmith.ai/learn/cmorfejgl00cw04jrtcc8wjbq"},
    {"name": "Digital Literacy Training", "url": "https://app.mindsmith.ai/learn/cmosgw5g5041j04ldxw0ngcbl"},
]

app = FastAPI()

# Initialize the Telegram Application
# Note: We initialize it globally so it's reused across requests
ptb_app = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for course in COURSES:
        keyboard.append([InlineKeyboardButton(text=f"{course['name']}", web_app=WebAppInfo(url=course['url']))])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome! Select a course to begin:", reply_markup=reply_markup)

# Register handlers
ptb_app.add_handler(CommandHandler("start", start))

@app.post("/api/webhook")
async def webhook_handler(request: Request):
    """Handles incoming updates from Telegram"""
    data = await request.json()
    update = Update.de_json(data, ptb_app.bot)
    
    # Run the update through the PTB application logic
    async with ptb_app:
        await ptb_app.process_update(update)
    
    return {"status": "ok"}

@app.get("/")
def index():
    return {"message": "Mindsmith Bot is running!"}