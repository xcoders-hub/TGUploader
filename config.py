import os
class Config(object):
    # get a token from https://chatbase.com
    CHAT_BASE_TOKEN = "11315729-822c-4ef1-a4bf-fe9b073787e9"
    # get a token from @BotFather
    TG_BOT_TOKEN = "1261526770:AAF2yUcExV3O1POnD2ydcKz5XmOEKaxtPWg"
    # The Telegram API things
    APP_ID = 1064864
    API_HASH = "5f3eeab0e6108731551e6a93598b654c"
    # Get these values from my.telegram.org
    # Array to store users who are authorized to use the bot
    AUTH_USERS = [1023178134]
    # Banned Unwanted Members..
    BANNED_USERS = []
    # the download location, where the HTTP Server runs
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    # Telegram maximum file upload size
    MAX_FILE_SIZE = 1572864000
    TG_MAX_FILE_SIZE = 1572864000
    FREE_USER_MAX_FILE_SIZE = 1572864000
    # chunk size that should be used with requests
    CHUNK_SIZE = 128
    # proxy for accessing youtube-dl in GeoRestricted Areas
    # Get your own proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    # https://t.me/hevcbay/951
    OUO_IO_API_KEY = ""
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # set timeout for subprocess
    PROCESS_MAX_TIMEOUT = 3600
    # watermark file
    DEF_WATER_MARK_FILE = ""
