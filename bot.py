import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Get bot token from environment variable
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Dictionary to store user's text temporarily
user_texts = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "📝 *Welcome to WordConvertBot!*\n\n"
        "I can help you analyze and convert text.\n\n"
        "*Send me any text* and I'll show you:\n"
        "• Word count\n"
        "• Character count\n"
        "• Sentence count\n"
        "• Paragraph count\n\n"
        "You can also convert text to different cases using the buttons below!"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    
    # Store the text for this user
    user_texts[user_id] = text
    
    # Calculate statistics
    word_count = len(text.split())
    char_count = len(text)
    char_count_no_space = len(text.replace(" ", ""))
    sentence_count = len(re.split(r'[.!?]+', text)) - 1
    paragraph_count = len(text.split('\n\n'))
    
    # Build response
    stats = (
        f"📊 *Text Analysis*\n\n"
        f"📝 Words: *{word_count}*\n"
        f"🔤 Characters (with spaces): *{char_count}*\n"
        f"🔤 Characters (no spaces): *{char_count_no_space}*\n"
        f"📖 Sentences: *{sentence_count}*\n"
        f"📄 Paragraphs: *{paragraph_count}*\n\n"
        f"*What would you like to do next?*"
    )
    
    # Create inline keyboard for conversion options
    keyboard = [
        [
            InlineKeyboardButton("🔠 UPPERCASE", callback_data="uppercase"),
            InlineKeyboardButton("🔡 lowercase", callback_data="lowercase")
        ],
        [
            InlineKeyboardButton("📗 Title Case", callback_data="titlecase"),
            InlineKeyboardButton("📘 Sentence case", callback_data="sentencecase")
        ],
        [
            InlineKeyboardButton("🔄 Show Stats Again", callback_data="stats")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(stats, parse_mode="Markdown", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    text = user_texts.get(user_id)
    
    if not text:
        await query.edit_message_text("⚠️ Please send me some text first!")
        return
    
    if query.data == "uppercase":
        converted = text.upper()
        label = "UPPERCASE"
    elif query.data == "lowercase":
        converted = text.lower()
        label = "lowercase"
    elif query.data == "titlecase":
        converted = text.title()
        label = "Title Case"
    elif query.data == "sentencecase":
        # Convert to sentence case (first letter of each sentence capitalized)
        sentences = re.split(r'([.!?] +)', text)
        converted = ''.join([sentences[i].capitalize() if i % 2 == 0 else sentences[i] for i in range(len(sentences))])
        label = "Sentence case"
    elif query.data == "stats":
        # Recalculate and show stats
        word_count = len(text.split())
        char_count = len(text)
        char_count_no_space = len(text.replace(" ", ""))
        sentence_count = len(re.split(r'[.!?]+', text)) - 1
        paragraph_count = len(text.split('\n\n'))
        
        stats = (
            f"📊 *Text Analysis*\n\n"
            f"📝 Words: *{word_count}*\n"
            f"🔤 Characters (with spaces): *{char_count}*\n"
            f"🔤 Characters (no spaces): *{char_count_no_space}*\n"
            f"📖 Sentences: *{sentence_count}*\n"
            f"📄 Paragraphs: *{paragraph_count}*\n\n"
            f"*Choose an option below:*"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("🔠 UPPERCASE", callback_data="uppercase"),
                InlineKeyboardButton("🔡 lowercase", callback_data="lowercase")
            ],
            [
                InlineKeyboardButton("📗 Title Case", callback_data="titlecase"),
                InlineKeyboardButton("📘 Sentence case", callback_data="sentencecase")
            ],
            [
                InlineKeyboardButton("🔄 Refresh Stats", callback_data="stats")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(stats, parse_mode="Markdown", reply_markup=reply_markup)
        return
    
    # Show the converted text
    result = f"📝 *{label}*\n\n```\n{converted}\n```\n\n🔄 *Send new text or click below for stats*"
    
    keyboard = [
        [InlineKeyboardButton("📊 Show Stats", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(result, parse_mode="Markdown", reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *How to use WordConvertBot*\n\n"
        "1️⃣ Send me *any text*\n"
        "2️⃣ I'll show you detailed statistics\n"
        "3️⃣ Use the buttons to convert your text\n\n"
        "*Commands:*\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/stats - Analyze the last text again"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = user_texts.get(user_id)
    
    if not text:
        await update.message.reply_text("⚠️ You haven't sent any text yet. Send me a text first!")
        return
    
    # Recalculate stats
    word_count = len(text.split())
    char_count = len(text)
    char_count_no_space = len(text.replace(" ", ""))
    sentence_count = len(re.split(r'[.!?]+', text)) - 1
    paragraph_count = len(text.split('\n\n'))
    
    stats = (
        f"📊 *Text Analysis*\n\n"
        f"📝 Words: *{word_count}*\n"
        f"🔤 Characters (with spaces): *{char_count}*\n"
        f"🔤 Characters (no spaces): *{char_count_no_space}*\n"
        f"📖 Sentences: *{sentence_count}*\n"
        f"📄 Paragraphs: *{paragraph_count}*"
    )
    
    await update.message.reply_text(stats, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 WordConvertBot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
