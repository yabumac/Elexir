import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- CONFIGURATION ---
# Use an environment variable for security!
BOT_TOKEN = os.getenv("BOT_TOKEN")

COURSES = [
    {"name": "Edify Ethiopia Overview ", "url": "https://app.mindsmith.ai/learn/cmg7jrxkv01bvlb04ses7x8i6"},
    {"name": "Discovering Your Values: A Guide to Good Choices", "url": "https://app.mindsmith.ai/learn/cmffk2f3303ubk104jqghqex2"},
    {"name": "Effective Teaching Methodologies for Early Childhood Education in Ethiopia", "url": "https://app.mindsmith.ai/learn/cmmduqj3i03gsl504srt6078y"},
    {"name": "Assessment & Classroom Management for Ethiopian Primary Teachers", "url": "https://app.mindsmith.ai/learn/cmo4cwxj4003p04l5gp140980"},
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