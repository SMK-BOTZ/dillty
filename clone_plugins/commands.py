# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import logging
import random
import asyncio
from Script import script
from validators import domain
from clone_plugins.dbusers import db
from clone_plugins.users_api import get_user, update_user_info
from pyrogram import Client, filters, enums
from plugins.database import get_file_details
from pyrogram.errors import ChatAdminRequired, FloodWait
from config import BOT_USERNAME, ADMINS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, InputMediaPhoto
from config import PICS, CUSTOM_FILE_CAPTION, AUTO_DELETE_TIME, AUTO_DELETE
import re
import json
import base64
from config import DB_URI as MONGO_URL
from pymongo import MongoClient

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vjbotz"]

logger = logging.getLogger(__name__)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Command to send start message with dynamic start text
@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    # Retrieve the bot's unique ID
    bot_id = str(client.me.id)
    
    # Get custom start text or default
    start_text = load_start_text() if os.path.exists(START_TEXT_FILE) else CLONE_START_TXT
    
    # Prepare buttons
    buttons = [[
        InlineKeyboardButton('💝 sᴜʙsᴄʀɪʙᴇ ᴍʏ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ', url='https://youtube.com/@Tech_VJ')
    ], [
        InlineKeyboardButton('🤖 ᴄʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ᴄʟᴏɴᴇ ʙᴏᴛ', url=f'https://t.me/{BOT_USERNAME}?start=clone')
    ], [
        InlineKeyboardButton('💁‍♀️ ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('ᴀʙᴏᴜᴛ 🔻', callback_data='about')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)

    # Get the bot's mention
    me2 = (await client.get_me()).mention

    # Send the start message
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=start_text.format(message.from_user.mention, me2),
        reply_markup=reply_markup
    )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""   

    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                )
            filetype = msg.media
            file = getattr(msg, filetype.value)
            title = '@VJ_Botz  ' + ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), file.file_name.split()))
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            k = await msg.reply(f"<b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\nThis Movie File/Video will be deleted in <b><u>{AUTO_DELETE} mins</u> 🫥 <i></b>(Due to Copyright Issues)</i>.\n\n<b><i>Please forward this File/Video to your Saved Messages and Start Download there</i></b>",quote=True)
            await asyncio.sleep(AUTO_DELETE_TIME)
            await msg.delete()
            await k.edit_text("<b>Your File/Video is successfully deleted!!!</b>")
            return
        except:
            pass
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if pre == 'filep' else False,
        )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01


# Default start text
CLONE_START_TXT = """<b>Hᴇʟʟᴏ {}, ᴍʏ ɴᴀᴍᴇ {}, 【ɪ ᴀᴍ ʟᴀᴛᴇꜱᴛ ᴀᴀᴅᴠᴀɴᴄᴇᴅ】ᴀɴᴅ ᴘᴏᴡᴡᴇʀꜰᴜʟ ꜰɪʟᴇ ꜱᴛᴏʀᴇ ʙᴏᴛ +├ᴄᴜꜱᴛᴏᴍ ᴜʀʟ ꜱʜᴏʀᴛɴᴇʀ ꜱᴜᴘᴘᴏʀᴛ┤+  ᢵᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ sᴜᴘᴘᴏʀᴛ ᢴ ᢾᴀɴᴅ ʙᴇꜱᴛ ᴜɪ ᴘᴇʀꜰᴏʀᴍᴀɴᴄᴇᢿ

ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ᴛʜᴇɴ ᴄʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ᴄʟᴏɴᴇ ʙᴏᴛ ғʀᴏᴍ ᴍʏ <a href=https://t.me/vj_botz>ᴘᴀʀᴇɴᴛ</a></b>"""

# File to store custom start text
START_TEXT_FILE = "start_text.json"

# Load start text from file or return default
def load_start_text():
    if os.path.exists(START_TEXT_FILE):
        with open(START_TEXT_FILE, "r") as file:
            data = json.load(file)
            return data.get("start_text", CLONE_START_TXT)
    return CLONE_START_TXT

# Save custom start text to file
def save_start_text(text):
    with open(START_TEXT_FILE, "w") as file:
        json.dump({"start_text": text}, file)

# Retrieve the owner of the bot
async def get_bot_owner(bot_id):
    owner = await db.db.bots.find_one({'bot_id': bot_id})
    return owner['user_id'] if owner else None

# Command to set custom start text (Owner only)
@Client.on_message(filters.command("start_text") & filters.private)
async def set_start_text(client, message):
    # Retrieve bot's unique ID
    bot_id = str(client.me.id)
    
    # Get the bot owner
    bot_owner_id = await get_bot_owner(bot_id)
    
    # Check if the user is the bot owner
    if message.from_user.id != bot_owner_id:
        await message.reply("You are not authorized to use this command.")
        return

    # Ensure that the user provided a new start text
    if len(message.command) < 2:
        await message.reply("Please provide the new start text. Usage: `/start_text <new_text>`")
        return

    new_text = " ".join(message.command[1:])
    
    # Save the new custom start text for this bot
    save_start_text(new_text)
    
    # Reply to confirm the change
    await message.reply(f"Start text updated to:\n\n{new_text}")

@Client.on_message(filters.command('api') & filters.private)
async def shortener_api_handler(client, m: Message):
    user_id = m.from_user.id
    user = await get_user(user_id)
    cmd = m.command

    if len(cmd) == 1:
        s = script.SHORTENER_API_MESSAGE.format(base_site=user["base_site"], shortener_api=user["shortener_api"])
        return await m.reply(s)

    elif len(cmd) == 2:    
        api = cmd[1].strip()
        await update_user_info(user_id, {"shortener_api": api})
        await m.reply("Shortener API updated successfully to " + api)
    else:
        await m.reply("You are not authorized to use this command.")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command("base_site") & filters.private)
async def base_site_handler(client, m: Message):
    user_id = m.from_user.id
    user = await get_user(user_id)
    cmd = m.command
    text = f"/base_site (base_site)\n\nCurrent base site: None\n\n EX: /base_site shortnerdomain.com\n\nIf You Want To Remove Base Site Then Copy This And Send To Bot - `/base_site None`"
    
    if len(cmd) == 1:
        return await m.reply(text=text, disable_web_page_preview=True)
    elif len(cmd) == 2:
        base_site = cmd[1].strip()
        if not domain(base_site):
            return await m.reply(text=text, disable_web_page_preview=True)
        await update_user_info(user_id, {"base_site": base_site})
        await m.reply("Base Site updated successfully")
    else:
        await m.reply("You are not authorized to use this command.")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01


@Client.on_callback_query()
def load_start_text(bot_id):
    # Check if custom start text exists for this bot
    start_text_file = f"start_text_{bot_id}.json"
    
    if os.path.exists(start_text_file):
        with open(start_text_file, "r") as file:
            data = json.load(file)
            return data.get("start_text", CLONE_START_TXT)
    
    return CLONE_START_TXT

# Function to handle callback query
async def cb_handler(client: Client, query: CallbackQuery):
    try:
        if query.data == "close_data":
            await query.message.delete()
        
        elif query.data == "start":
            # Get the bot's ID and load its custom start text if available
            bot_id = str(client.me.id)
            custom_start_text = load_start_text(bot_id)
            
            buttons = [
                [
                    InlineKeyboardButton('💝 sᴜʙsᴄʀɪʙᴇ ᴍʏ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ', url='https://youtube.com/@Tech_VJ')
                ],
                [
                    InlineKeyboardButton('🤖 ᴄʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ᴄʟᴏɴᴇ ʙᴏᴛ', url=f'https://t.me/{BOT_USERNAME}?start=clone')
                ],
                [
                    InlineKeyboardButton('💁‍♀️ ʜᴇʟᴘ', callback_data='help'),
                    InlineKeyboardButton('ᴀʙᴏᴜᴛ 🔻', callback_data='about')
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(buttons)
            
            # Change the media of the message to a random image
            await client.edit_message_media(
                query.message.chat.id,
                query.message.id,
                InputMediaPhoto(random.choice(PICS))
            )

            # Get bot's mention for the start text
            me2 = (await client.get_me()).mention
            
            # Send the start message text using the custom start text or default
            start_text = custom_start_text.format(query.from_user.mention, me2)
            
            await query.message.edit_text(
                text=start_text,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    
    except Exception as e:
        # Log the error or handle it
        print(f"Error in cb_handler: {e}")
        await query.message.reply("An error occurred while processing your request.")


# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔒 Cʟᴏsᴇ', callback_data='close_data')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CHELP_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )  

    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔒 Cʟᴏsᴇ', callback_data='close_data')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        me2 = (await client.get_me()).mention
        id = client.me.id
        owner = mongo_db.bots.find_one({'bot_id': id})
        ownerid = int(owner['user_id'])
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CABOUT_TXT.format(me2, ownerid),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )  

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
