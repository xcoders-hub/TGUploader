import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import asyncio
import json
import math
import os
import time
from config import Config
from translation import Translation
import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import humanbytes
from helper_funcs.help_uploadbot import DownLoadFile
@pyrogram.Client.on_message(pyrogram.Filters.regex(pattern=".*http.*"))
async def echo(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return
    TRChatBase(update.from_user.id, update.text, "/echo")
    logger.info(update.from_user)
    url = update.text
    youtube_dl_username = None
    youtube_dl_password = None
    file_name = None
    if "|" in url:
        url_parts = url.split("|")
        if len(url_parts) == 2:
            url = url_parts[0]
            file_name = url_parts[1]
        else:
            for entity in update.entities:
                if entity.type == "text_link":
                    url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    url = url[o:o + l]
        if url is not None:
            url = url.strip()
        if file_name is not None:
            file_name = file_name.strip()
    else:
        for entity in update.entities:
            if entity.type == "text_link":
                url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                url = url[o:o + l]
    command_to_exec = [
        "youtube-dl",
        "--no-warnings",
        "--youtube-skip-dash-manifest",
        "-j",
        url
    ]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    logger.info(e_response)
    t_response = stdout.decode().strip()
    logger.info(t_response)
    if e_response and "nonnumeric port" not in e_response:
        error_message = e_response.replace("please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.", "")
        if "This video is only available for registered users." in error_message:
            error_message += Translation.SET_CUSTOM_USERNAME_PASSWORD
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.NO_VOID_FORMAT_FOUND.format(str(error_message)),
            reply_to_message_id=update.message_id,
            parse_mode="html",
            disable_web_page_preview=True
        )
        return False
    if t_response:
        x_reponse = t_response
        if "\n" in x_reponse:
            x_reponse, _ = x_reponse.split("\n")
        response_json = json.loads(x_reponse)
        save_ytdl_json_path = Config.DOWNLOAD_LOCATION + \
            "/" + str(update.from_user.id) + ".json"
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        format_id = response_json["format_id"]
        format_ext = response_json["ext"]
        inline_keyboard = []
        cb_string_file = "{}={}={}".format(
            "file", format_id, format_ext)
        inline_keyboard.append([
            pyrogram.InlineKeyboardButton(
                "File",
                callback_data=(cb_string_file).encode("UTF-8")
            )
        ])
        reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FORMAT_SELECTION,
            reply_markup=reply_markup,
            parse_mode="html",
            reply_to_message_id=update.message_id
        )
    else:
        inline_keyboard = []
        cb_string_file = "{}={}={}".format(
            "file", "LFO", "NONE")
        inline_keyboard.append([
            pyrogram.InlineKeyboardButton(
                "DFile",
                callback_data=(cb_string_file).encode("UTF-8")
            )
        ])
        reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FORMAT_SELECTION,
            reply_markup=reply_markup,
            parse_mode="html",
            reply_to_message_id=update.message_id
        )