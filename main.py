
import os
import random
import logging
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db_name = os.getenv("MONGODB_DB_NAME")
print(f"MongoDB Database Name: {db_name}")
mongo_db = mongo_client[db_name]
video_collection = mongo_db["videos"]

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize the bot with the token
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
print(f"Bot Token: {bot_token}")
bot = Bot(token=bot_token)

def start(update: Update, context: CallbackContext) -> None:
    logger.info(f"Received /start command from user: {update.message.from_user.id}")
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
    update.message.reply_photo(photo=welcome_image_url, caption=start_text, parse_mode='HTML', reply_markup=reply_markup.to_dict())


def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    logger.info(f"Button callback received with data: {query.data} from user: {query.from_user.id}")
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
    logger.info(f"Checking if user {user_id} has joined required channels")
    channels = ["@kissubots", "@kissuxbots", "@kissudev"]
    for channel in channels:
        try:
            member = bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                logger.info(f"User {user_id} has not joined channel {channel}")
                return False
        except Exception as e:
            logger.error(f"Error checking user {user_id} in channel {channel}: {e}")
            return False
    return True

def is_valid_domain(url: str) -> bool:
    logger.info(f"Validating domain for URL: {url}")
    valid_domains = os.getenv("VALID_DOMAINS").split(',')
    domain = url.split('/')[2]
    is_valid = domain in valid_domains
    if not is_valid:
        logger.warning(f"Invalid domain: {domain}")
    return is_valid

import requests

import requests
import aria2p
from datetime import datetime
from status import format_progress_bar
import asyncio
import os, time
import logging
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret=""
    )
)
options = {
    "max-tries": "50",
    "retry-wait": "3",
    "continue": "true"
}

aria2.set_global_options(options)

async def download_video(url, reply_msg, user_mention, user_id):
    response = requests.get(f"https://teraboxvideodownloader.nepcoderdevs.workers.dev/?url={url}")
    response.raise_for_status()
    data = response.json()

    resolutions = data["response"][0]["resolutions"]
    fast_download_link = resolutions["Fast Download"]
    hd_download_link = resolutions["HD Video"]
    thumbnail_url = data["response"][0]["thumbnail"]
    video_title = data["response"][0]["title"]

    try:
        download = aria2.add_uris([fast_download_link])
        start_time = datetime.now()

        while not download.is_complete:
            download.update()
            percentage = download.progress
            done = download.completed_length
            total_size = download.total_length
            speed = download.download_speed
            eta = download.eta
            elapsed_time_seconds = (datetime.now() - start_time).total_seconds()
            progress_text = format_progress_bar(
                filename=video_title,
                percentage=percentage,
                done=done,
                total_size=total_size,
                status="Downloading",
                eta=eta,
                speed=speed,
                elapsed=elapsed_time_seconds,
                user_mention=user_mention,
                user_id=user_id,
                aria2p_gid=download.gid
            )
            await reply_msg.edit_text(progress_text)
            await asyncio.sleep(2)

        if download.is_complete:
            file_path = download.files[0].path

            thumbnail_path = "thumbnail.jpg"
            thumbnail_response = requests.get(thumbnail_url)
            with open(thumbnail_path, "wb") as thumb_file:
                thumb_file.write(thumbnail_response.content)

            await reply_msg.edit_text("ᴜᴘʟᴏᴀᴅɪɴɢ...")

            return file_path, thumbnail_path, video_title
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        buttons = [
            [InlineKeyboardButton("🚀 HD Video", url=hd_download_link)],
            [InlineKeyboardButton("⚡ Fast Download", url=fast_download_link)]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await reply_msg.reply_text(
            "Fast Download Link For this Video is Broken, Download manually using the Link Below.",
            reply_markup=reply_markup
        )
        return None, None, None
    from time import time
    from time import time
    try:
        logger.info(f"Sending request to download video from URL: {url}")
        response = requests.get(f"https://teraboxvideodownloader.nepcoderdevs.workers.dev/?url={url}")
        response.raise_for_status()
        data = response.json()
        logger.info(f"Received response: {data}")
 
        resolutions = data["response"][0]["resolutions"]
        fast_download_link = resolutions["Fast Download"]
        hd_download_link = resolutions["HD Video"]
        thumbnail_url = data["response"][0]["thumbnail"]
        video_title = data["response"][0]["title"]
        logger.info(f"Video details - Title: {video_title}, Fast Download: {fast_download_link}, HD Download: {hd_download_link}, Thumbnail: {thumbnail_url}")
 
        # Save video details and file in MongoDB
        video_details = {
            "user_id": user_id,
            "url": url,
            "video_title": video_title,
            "fast_download_link": fast_download_link,
            "hd_download_link": hd_download_link,
            "thumbnail_url": thumbnail_url,
            "timestamp": time(),
            "video_file": response.content  # Save the video file content
        }
        video_collection.insert_one(video_details)
        logger.info(f"Video details saved in MongoDB for user: {user_id}")
 
        reply_msg.reply_text(f"Video Title: {video_title}\nFast Download: {fast_download_link}\nHD Download: {hd_download_link}\nThumbnail: {thumbnail_url}")
        logger.info(f"Video details sent to user: {user_id}")
 
        # Retrieve video details from MongoDB
        video_details = video_collection.find_one({"user_id": user_id, "url": url})
        if video_details:
            video_file = video_details["video_file"]
            video_title = video_details["video_title"]
            reply_msg.reply_video(video=video_file, filename=f"{video_title}.mp4")
            logger.info(f"Video sent to user: {user_id}")

            # Delete video details from MongoDB after sending
            video_collection.delete_one({"user_id": user_id, "url": url})
            logger.info(f"Video details deleted from MongoDB for user: {user_id}")
        else:
            logger.error(f"Video details not found in MongoDB for user: {user_id}")
            reply_msg.reply_text('Failed to retrieve video details. Please try again later.')
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        reply_msg.reply_text('An error occurred while downloading the video. Please try again later.')

def handle_download_video(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    logger.info(f"Received video download request from user: {user_id}")
    if not check_user_joined_channels(user_id):
        logger.info(f"User {user_id} has not joined required channels")
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Channel 1", url="https://t.me/kissubots")],
            [InlineKeyboardButton("Channel 2", url="https://t.me/kissuxbots")],
            [InlineKeyboardButton("Channel 3", url="https://t.me/kissudev")]
        ])
        update.message.reply_text('Join all channels to use me', reply_markup=reply_markup)
        return
    url = update.message.text
    if not is_valid_domain(url):
        logger.warning(f"Invalid domain for URL: {url}")
        update.message.reply_text('Invalid domain. Please provide a valid Terabox link.')
        return
    reply_msg = update.message.reply_text('Downloading video...')
    user_mention = update.message.from_user.mention_html()
    context.bot.loop.create_task(download_video(url, reply_msg, user_mention, user_id))

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

    # Send video to log channel with filename
    filename = 'video.mp4'
    with open(filename, 'rb') as file:
        bot.send_video(chat_id=log_channel_id, video=InputFile(file, filename=filename), caption="Downloaded video")

    # Send video to user
    with open(filename, 'rb') as file:
        update.message.reply_video(video=InputFile(file, filename=filename), caption="Here is your video")



def main() -> None:
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_download_video))

    updater.start_polling()
    updater.idle()

async def upload_video(client, file_path, thumbnail_path, video_title, reply_msg, collection_channel_id, user_mention, user_id, message):
    file_size = os.path.getsize(file_path)
    uploaded = 0
    start_time = datetime.now()
    last_update_time = time.time()

    async def progress(current, total):
        nonlocal uploaded, last_update_time
        uploaded = current
        percentage = (current / total) * 100
        elapsed_time_seconds = (datetime.now() - start_time).total_seconds()
        
        if time.time() - last_update_time > 2:
            progress_text = format_progress_bar(
                filename=video_title,
                percentage=percentage,
                done=current,
                total_size=total,
                status="Uploading",
                eta=(total - current) / (current / elapsed_time_seconds) if current > 0 else 0,
                speed=current / elapsed_time_seconds if current > 0 else 0,
                elapsed=elapsed_time_seconds,
                user_mention=user_mention,
                user_id=user_id,
                aria2p_gid=""
            )
            try:
                await reply_msg.edit_text(progress_text)
                last_update_time = time.time()
            except Exception as e:
                logging.warning(f"Error updating progress message: {e}")

    with open(file_path, 'rb') as file:
        collection_message = await client.send_video(
            chat_id=collection_channel_id,
            video=file,
            thumb=thumbnail_path,
            caption=video_title,
            supports_streaming=True,
            progress=progress
        )

    await reply_msg.edit_text(f"Video uploaded successfully to {collection_channel_id}!")
    return collection_message

if __name__ == '__main__':
    main()
