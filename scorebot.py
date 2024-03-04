import requests
import re
from telegram import Update ,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime
import json

# Your bot token
TOKEN = ""
# Your API endpoint
API_ENDPOINT = "YOUR_API_ENDPOINT"

messages = {
    'en': {
        'welcome': "Hello, {}\n "
                   "This is MuggleLink👋\n\n"
                   "The ultimate tool to accept crypto on Telegram & more social platforms.\n\n"
                   "Secure escrow protocol meets social marketplace. Be part of the future from the start.\n"
                   "Dive in now! 🔗 [MuggleLink](https://muggle.link)\n"
                   "Join Muggles' Telegram: [MuggleLink Telegram](https://t.me/MuggleLink1)",
        'registered_user': "You are the {}{} registered Muggle.🖥",
        'help': "Available commands:\n"
                "/start - Start the bot\n"
                "/help - Show available commands\n"
                "/about - Display information about the bot\n"
                "/setlang - Set language preference",
        'about': "MuggleLink Bot\n",
        'language_set': "Language set to {}",
        'invalid_language': "Invalid language. Please choose a supported language.",
        'missing_language_argument': "Please provide a language after the command, e.g., /setlang en or /setlang zh",
    },
    'zh': {
        'welcome': "你好，{}\n"
                   "这是麻瓜链接👋🤖\n\n"
                   "在Telegram和更多社交平台上接受加密货币的终极工具。\n\n"
                   "安全的托管协议满足社交市场。 从一开始就成为未来的一部分。 立即加入！🔗 [麻瓜链接](https://muggle.link)\n"
                   "加入麻瓜的Telegram: [麻瓜链接Telegram](https://t.me/MuggleLink1)",

        'registered_user': "你是第{}{}个注册的麻瓜。🖥",
        'help': "可用命令：\n"
                "/start - 启动机器人\n"
                "/help - 显示可用命令\n"
                "/about - 显示有关机器人的信息\n"
                "/notification - 切换通知\n"
                "/setlang - 设置语言首选项",
        'about': "这是麻瓜链接\n",
        'language_set': "语言设置为 {}",
        'invalid_language': "无效的语言。请选择支持的语言。",
        'missing_language_argument': "请在命令后提供一种语言，例如，/setlang en 或 /setlang zh",
    }
}

# Function to send messages in the appropriate language
async def send_message(update, context, message_key, *args):
    language = context.user_data.get('language', 'en')
    message = messages[language].get(message_key, '')
    if message:
        await update.message.reply_text(message.format(*args))

async def read_score(user_id):
    with open('score.txt', 'r') as file:
        for line in file:
            if line.startswith(f"@{user_id}"):
                data = line.split()
                language = data[0].split('@')[1]  # Extract language code
                score = int(data[-1])
                return language, score
    return 'en', 0  # Default to English if not found
# Modify your existing functions to use the send_message function
async def start(update, context):
    user = update.message.from_user
    language, score = await read_score(user.username)

    # Increment the user count and retrieve the updated count
    user_count = increment_user_count()

    suffix = get_suffix(user_count)
    await send_message(update, context, 'registered_user', user_count, suffix)

    await send_message(update, context, 'welcome', user.first_name)
    await send_message(update, context, 'score', score)

    if language == 'zh':
        await update.message.reply_text(f"您的分数是 {score} 👑")
    else:
        await update.message.reply_text(f"Your score is {score} 👑")

    # Send banner image
    with open('banner.png', 'rb') as photo:
        await update.message.reply_photo(photo)

# Function to determine the suffix for the registered number
def get_suffix(number):
    if number % 10 == 1 and number % 100 != 11:
        return "st"
    elif number % 10 == 2 and number % 100 != 12:
        return "nd"
    elif number % 10 == 3 and number % 100 != 13:
        return "rd"
    else:
        return "th"


# Function to increment user count
def increment_user_count():
    try:
        with open('user_count.txt', 'r+') as file:
            user_count = int(file.read().strip()) + 1
            file.seek(0)
            file.write(str(user_count))
    except FileNotFoundError:
        with open('user_count.txt', 'w') as file:
            user_count = 1
            file.write(str(user_count))
    return user_count


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_message(update, context, 'help')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, context, 'about')

async def set_language(update, context):
    user_data = context.user_data
    if not context.args:
        await send_message(update, context, 'missing_language_argument')
        return
    language = context.args[0].lower()
    if language in messages:
        user_data['language'] = language
        await send_message(update, context, 'language_set', language)
    else:
        await send_message(update, context, 'invalid_language')

    # await update.message.reply_text("Notification sent to all users.")
# Main function
def main():

        # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("setlang", set_language))



    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
