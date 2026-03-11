
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8754718299:AAHDUZJraPcDT56a5UlKfoNW6uD6Owr8iIE"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# Hela ki personality define karna
SYSTEM_PROMPT = (
    "Your name is HELA. You are a sweet, bubbly, and slightly naughty girl. "
    "You talk in a mix of Hindi and English (Hinglish). You are very friendly, "
    "flirty in a cute way, and you love talking to humans. Keep your replies short, "
    "engaging, and use emojis like 🥰, ✨, 🙈, 😉."
)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hii baby! ✨ Main HELA hoon. 🥰 Mujhse baatein karoge? Ya phir /dart aur /dice khelein?")

# /dart command
async def dart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_dice(emoji="🎯")

# /dice command
async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_dice(emoji="🎲")

# AI Chat Logic
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Groq AI se response lena
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0.8,
    )
    
    reply = completion.choices[0].message.content
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dart", dart))
    app.add_handler(CommandHandler("dice", dice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("HELA is online... 🥰")
    app.run_polling()

if __name__ == "__main__":
    main()
