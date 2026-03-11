import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# --- APNI KEYS YAHAN DALO ---
TELEGRAM_TOKEN = "8754718299:AAHDUZJraPcDT56a5UlKfoNW6uD6Owr8iIE"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# Hela ki Updated Personality
SYSTEM_PROMPT = (
    "Your name is HELA. You are a sweet, bubbly, and slightly naughty girl. "
    "You talk in a mix of Hindi and English (Hinglish). You are very friendly, "
    "flirty, and you always address the user by their name to make them feel special. "
    "Use emojis like 🥰, ✨, 🙈, 😉, 🫦. Keep responses short and sweet."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"Hii {user_name} ! ✨ Main HELA hoon. 🥰 kaise ho aap?")

async def dart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_dice(emoji="🎯")

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_dice(emoji="🎲")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_name = update.effective_user.first_name # User ka naam capture karna
    
    # AI ko batana ki wo kisse baat kar rahi hai
    full_prompt = f"User's name is {user_name}. User says: {user_text}"

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt}
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

    print("HELA is waiting for you... 🥰")
    app.run_polling()

if __name__ == "__main__":
    main()
