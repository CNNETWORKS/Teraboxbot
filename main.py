
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
            [InlineKeyboardButton("Link 1", url="https://t.me/link1"), InlineKeyboardButton("Link 2", url="https://t.me/link2"), InlineKeyboardButton("Link 3", url="https://t.me/link3")],
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

    # Placeholder for video download logic
    update.message.reply_text('Downloading video...')

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
