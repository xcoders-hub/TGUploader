import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import json
import math
import os
import shutil
import subprocess
import time
from config import Config
from translation import Translation
import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram, humanbytes
from plugins.dl_button import ddl_call_back
@pyrogram.Client.on_callback_query()
async def button(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.message.chat.id,
            message_ids=update.message.message_id,
            revoke=True
        )
        return
    cb_data = update.data
    if "=" in cb_data:
        await ddl_call_back(bot, update)
