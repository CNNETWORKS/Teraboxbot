
import os
import random
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Load environment variables from .env file
load_dotenv()

# Initialize the bot with the token
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
print(f"Bot Token: {bot_token}")
bot = Bot(token=bot_token)

def start(update: Update, context: CallbackContext) -> None:
    # Fetch welcome images from environment variable and select one randomly
    welcome_images = os.getenv("WELCOME_IMAGES").split(',')
    welcome_image_url = random.choice(welcome_images)
    
    user_name = update.message.from_user.first_name
    bot_name = context.bot.username
    start_text = f"<b>hello {user_name}.\n\nMy name is {bot_name}.\n\nI can Provide You Terabox Videos \n<blockquote>owned by  : <a href=\"https://t.me/xaekks\">kissu</a>\n</blockquote></b>"
    welcome_image_url = random.choice(welcome_images)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Channel 1", url="https://t.me/kissubots"), InlineKeyboardButton("Channel 2", url="https://t.me/kissuxbots"), InlineKeyboardButton("Channel 3", url="https://t.me/kissudev")],
        [InlineKeyboardButton("Help", callback_data='help'), InlineKeyboardButton("About", callback_data='about')]
    ])
    update.message.reply_photo(photo=welcome_image_url, caption=start_text, parse_mode='HTML', reply_markup=reply_markup)


def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'about':
        welcome_images = os.getenv("WELCOME_IMAGES").split(',')
        bot_name = context.bot.username
        about_txt = f"<b>✯ Mʏ ɴᴀᴍᴇ: {bot_name}\n✯ Oᴡɴᴇʀ: <a href=\"https://t.me/xaekks\">𓆩•𝐊𝐢𝐬𝐬𝐮 💞•𓆪</a>\n✯ Cᴏᴅᴇᴅ Oɴ: ᴩʏᴛʜᴏɴ/ᴩʏʀᴏɢʀᴀᴍ\n✯ Mʏ DᴀᴛᴀBᴀꜱᴇ: ᴍᴏɴɢᴏ-ᴅʙ\n✯ Mʏ Sᴇʀᴠᴇʀ: ᴀɴʏᴡʜᴇʀᴇ\n✯ Mʏ Vᴇʀꜱɪᴏɴ: ᴠ4.5.0</b>"
        welcome_image_url = random.choice(welcome_images)
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Help", callback_data='help'), InlineKeyboardButton("Back", callback_data='start')]
        ])
        query.edit_message_media(media=InputMediaPhoto(media=welcome_image_url, caption=about_txt, parse_mode='HTML'), reply_markup=reply_markup)
    elif query.data == 'help':
        welcome_images = os.getenv("WELCOME_IMAGES").split(',')
        help_txt = "Hello, welcome to the help section."
        welcome_image_url = random.choice(welcome_images)
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Premium", callback_data='buy'), InlineKeyboardButton("Back", callback_data='start')]
        ])
        query.edit_message_media(media=InputMediaPhoto(media=welcome_image_url, caption=help_txt, parse_mode='HTML'), reply_markup=reply_markup)
    elif query.data == 'start':
        welcome_images = os.getenv("WELCOME_IMAGES").split(',')
        user_name = query.from_user.first_name
        bot_name = context.bot.username
        start_text = f"<b>hello {user_name}.\n\nMy name is {bot_name}.\n\nI can Provide You Terabox Videos \n<blockquote>owned by  : <a href=\"https://t.me/xaekks\">kissu</a>\n</blockquote></b>"
        welcome_image_url = random.choice(welcome_images)
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Link 1", url="https://t.me/kissubots"), InlineKeyboardButton("Link 2", url="https://t.me/kissuxbots"), InlineKeyboardButton("Link 3", url="https://t.me/kissudev")],
            [InlineKeyboardButton("Help", callback_data='help'), InlineKeyboardButton("About", callback_data='about')]
        ])
        query.edit_message_media(media=InputMediaPhoto(media=welcome_image_url, caption=start_text, parse_mode='HTML'), reply_markup=reply_markup)
        query.edit_message_text(text=f"You clicked: {query.data}")

def check_user_joined_channels(user_id: int) -> bool:
    channels = ["@kissubots", "@kissuxbots", "@kissudev"]
    for channel in channels:
        try:
            member = bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

def is_valid_domain(url: str) -> bool:
    valid_domains = os.getenv("VALID_DOMAINS").split(',')
    domain = url.split('/')[2]
    return domain in valid_domains

def download_video(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not check_user_joined_channels(user_id):
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Channel 1", url="https://t.me/kissubots")],
            [InlineKeyboardButton("Channel 2", url="https://t.me/kissuxbots")],
            [InlineKeyboardButton("Channel 3", url="https://t.me/kissudev")]
        ])
        update.message.reply_text('Join all channels to use me', reply_markup=reply_markup)
        return

    url = update.message.text
    if not is_valid_domain(url):
        update.message.reply_text('Invalid domain. Please provide a valid Terabox link.')
        return

    import requests
    from telegram import InputFile
    from time import time
    from pymongo import MongoClient

    # Connect to MongoDB
    mongodb_uri = os.getenv("MONGODB_URI")
    mongodb_db_name = os.getenv("MONGODB_DB_NAME")
    client = MongoClient(mongodb_uri)
    db = client[mongodb_db_name]
    downloads_collection = db.downloads

    # Load environment variables
    log_channel_id = int(os.getenv("LOG_CHANNEL_ID"))
    api_url = os.getenv("API_URL").format(url=url)

    # Log the start of the download
    download_log = {
        "user_id": user_id,
        "url": url,
        "status": "started",
        "timestamp": time()
    }
    downloads_collection.insert_one(download_log)

    # Download video
    update.message.reply_text('Starting video download...')
    response = requests.get(api_url, stream=True)
    update.message.reply_text('Video download request sent...')
    if response.status_code == 200:
        update.message.reply_text('Video download started...')
    else:
        update.message.reply_text(f'Failed to start video download. Status code: {response.status_code}')
        return
    update.message.reply_text('Video download in progress...')

    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress = 0
    start_time = time()

    with open('video.mp4', 'wb') as file:
        for data in response.iter_content(block_size):
            progress += len(data)
            file.write(data)
            done = int(50 * progress / total_size)
            speed = progress / (time() - start_time)
            eta = (total_size - progress) / speed
            progress_bar = f"\n<b>╭━━━━❰progress bar❱➜\n➜ 🗃️ size: {total_size} | {progress}\n➜ ⏳️ done: {done}%\n➜ 🚀 speed: {speed:.2f}/s\n➜ ⏰️ eta: {eta:.2f}s\n╰━━━━━━━━━━━━━━━➜ </b>"
            update.message.reply_text(progress_bar, parse_mode='HTML')

    # Log the completion of the download
    download_log["status"] = "completed"
    download_log["timestamp"] = time()
    downloads_collection.insert_one(download_log)

    # Log the completion of the download
    download_log["status"] = "completed"
    download_log["timestamp"] = time()
    downloads_collection.insert_one(download_log)

    # Send video to log channel with filename
    filename = 'video.mp4'
    with open(filename, 'rb') as file:
        bot.send_video(chat_id=log_channel_id, video=InputFile(file, filename=filename), caption="Downloaded video")

    # Send video to user
    with open(filename, 'rb') as file:
        update.message.reply_video(video=InputFile(file, filename=filename), caption="Here is your video")

    # Send video to user
    with open('video.mp4', 'rb') as file:
        update.message.reply_video(video=InputFile(file), caption="Here is your video")

def main() -> None:
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
