import logging
import os
import sys
import time
import spamwatch
import httpx
import aiohttp
import telegram.ext as tg
import psycopg2

from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.sessions import StringSession
from motor import motor_asyncio
from odmantic import AIOEngine
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from redis import StrictRedis
from Python_ARQ import ARQ
from aiohttp import ClientSession
from telegraph import Telegraph
from telegram import Chat

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.",
    )
    sys.exit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", "2142595466"))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get("EVENT_LOGS", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "CoderX")

    try:
        DRAGONS = {int(x) for x in os.environ.get("DRAGONS", "").split()}
        DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = {int(x) for x in os.environ.get("DEMONS", "").split()}
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WOLVES = {int(x) for x in os.environ.get("WOLVES", "").split()}
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = {int(x) for x in os.environ.get("TIGERS", "").split()}
    except ValueError:
        raise Exception("Your scout users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get("INFOPIC", True)) or "https://telegra.ph/file/a9ec99487ecd550460309.jpg"
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    ERROR_LOGS = os.environ.get("ERROR_LOGS", None)
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # If You Deploy On Heroku. [URL PERTEN:- https://{appname}.herokuapp.com/ || EXP:- https://scenario.herokuapp.com/]
    PORT = int(os.environ.get("PORT", 8443)) 
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get("API_ID", None) # Bot Owner's API_ID (From:- https://my.telegram.org/apps)
    API_HASH = os.environ.get("API_HASH", None) # Bot Owner's API_HASH (From:- https://my.telegram.org/apps)
    DB_URL = os.environ.get("DATABASE_URL") # Any SQL Database Link (RECOMMENDED:- PostgreSQL & https://www.elephantsql.com)
    connection_db = psycopg2.connect(DB_URL, sslmode="require")
    DB_URL = DB_URL.replace(
        "postgres://", "postgresql://", 1
    )  # rest of connection code using the connection string `uri`

    DONATION_LINK = os.environ.get("https://t.me/i_14344") # Donation Link (ANY)
    LOAD = os.environ.get("LOAD", "").split() # Don't Change
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split() # Don't Change
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False)) # Don't Change
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False)) or "True"
    WORKERS = int(os.environ.get("WORKERS", 8)) # Don't Change
    BAN_STICKER = os.environ.get("BAN_STICKER",None) # Don't Change
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False) # Don't Change
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./") # Don't Change
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None) or "70F3DVSKF6RUAHQV"
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None) or "K5PTMFOEC82M"
    WALL_API = os.environ.get("WALL_API", None) # From:- https://wall.alphacoders.com/api.php
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None) # From:- https://www.remove.bg/
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", "") # From:- https://openweathermap.org/api
    GENIUS_API_TOKEN = os.environ.get("GENIUS_API_TOKEN", None) # From:- http://genius.com/api-clients
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL", "mongodb+srv://Cluster006:600510@cluster006.ootpa.mongodb.net/Cluster006?retryWrites=true&w=majority")
    REDIS_URL = os.environ.get("REDIS_URL", "redis://Madharjoot:GuKhao123_@redis-12276.c275.us-east-1-4.ec2.cloud.redislabs.com:12276/Madharjoot")
    BOT_ID = int(os.environ.get("BOT_ID", None)) # Telegram Bot ID (EXP:- 1241223850)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None) # Support Chat Group Link (Use @ScenarioXSupport || Dont Use https://t.me/ScenarioXSupport)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", None) # Use @SpamWatchSupport
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None) # From https://t.me/SpamWatchBot 
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "") # Bot Username
    STRING_SESSION = os.environ.get("STRING_SESSION", None) # Telethon Based String Session (2nd ID) [ From https://repl.it/@SpEcHiDe/GenerateStringSession ]
    REPO = "TeamScenario/Scenario"
    DEVELOPER = "TeamScenario"
    APP_ID = API_ID
    APP_HASH = API_HASH
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", True) # Heroku App Name 
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", True) # Heroku API [From https://dashboard.heroku.com/account]
    UPSTREAM_BRANCH = os.environ.get("UPSTREAM_BRANCH", True)
    UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", True)
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", True)
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True) # Don't Change
    BOT_NAME = os.environ.get("BOT_NAME", True) # Name Of your Bot.
    MONGO_DB = "scenario" # Don't change else errors.
    ARQ_API_URL = "https://arq.hamker.in"
    GOOGLE_CHROME_BIN = "/usr/bin/google-chrome"
    CHROME_DRIVER = "/usr/bin/chromedriver"
    SUDO_USERS = "2142595466"
    WHITELIST_USERS = "2142595466"
    BOT_API_URL = os.environ.get('BOT_API_URL', "https://api.telegram.org/bot")
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "TeamScenario")

    HELP_IMG = os.environ.get("HELP_IMG", True) or "https://telegra.ph/file/a9ec99487ecd550460309.jpg"
    GROUP_START_IMG = os.environ.get("GROUP_START_IMG", True) or "https://telegra.ph/file/a9ec99487ecd550460309.jpg"
    scenario_pic = os.environ.get("scenario_pic", True) or "https://telegra.ph/file/a9ec99487ecd550460309.jpg"
    
    try:
        BL_CHATS = {int(x) for x in os.environ.get("BL_CHATS", "").split()}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

else:
    import config

    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    OWNER_USERNAME = Config.OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        DRAGONS = {int(x) for x in Config.DRAGONS or []}
        DEV_USERS = {int(x) for x in Config.DEV_USERS or []}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = {int(x) for x in Config.DEMONS or []}
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WOLVES = {int(x) for x in Config.WOLVES or []}
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = {int(x) for x in Config.TIGERS or []}
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")


    INFOPIC = Config.INFOPIC
    EVENT_LOGS = Config.EVENT_LOGS 
    ERROR_LOGS = Config.ERROR_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    DB_URL = Config.DB_URL
    DONATION_LINK = Config.DONATION_LINK
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    WALL_API = Config.WALL_API
    MONGO_DB_URL = Config.MONGO_DB_URL
    REDIS_URL = Config.REDIS_URL
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    APP_ID = Config.APP_ID
    APP_HASH = Config.APP_HASH
    BOT_ID = Config.BOT_ID
    BOT_USERNAME = Config.BOT_USERNAME
    STRING_SESSION = Config.STRING_SESSION
    GENIUS_API_TOKEN = Config.GENIUS_API_TOKEN
    YOUTUBE_API_KEY = Config.YOUTUBE_API_KEY
    ALLOW_EXCL = Config.ALLOW_EXCL
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    ARQ_API_URL = Config.ARQ_API_URL
    GOOGLE_CHROME_BIN = Config.GOOGLE_CHROME_BIN
    CHROME_DRIVER = Config.CHROME_DRIVER
    BOT_NAME = Config.BOT_NAME
    DEL_CMDS = Config.DEL_CMDS
    BOT_API_URL = Config.BOT_API_URL
    MONGO_DB_URL = Config.MONGO_DB_URL
    MONGO_DB = Config.MONGO_DB
    HELP_IMG = Config.HELP_IMG
    START_IMG = Config.START_IMG
    scenario_pic = Config.scenario_pic

    try:
        BL_CHATS = {int(x) for x in Config.BL_CHATS or []}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")
        

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
# add your I'd here if you want to !
# DEV_USERS.add(yourid)
DEV_USERS.add(2032894605)
DEV_USERS.add(1356469075)
DEV_USERS.add(2142595466)

REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)

try:

    REDIS.ping()

    LOGGER.info("[Scenario]: Connecting to redis")
except BaseException:

    raise Exception("[Scenario ERROR]: Redis Database Is Not Alive, Please Check Again.")

finally:

   REDIS.ping()

   LOGGER.info("[Scenario]: Connection to Redis Database Established Successfully!")
    

if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("[Scenario ERROR]: SpamWatch API key Is Missing! Recheck Your Config.")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except:
        sw = None
        LOGGER.warning("[scenario ERROR]: Can't connect to SpamWatch!")


# Credits Logger
print("[Scenario] is Starting. | Scenraio • An Arc Project | Licensed Under GPLv3.")
print("[Scenario] Successfully Connected.")
print("[Scenario] Project Maintained By: https://github.com/TeamScenario (https://t.me/TeamScenario)")


telegraph = Telegraph()
telegraph.create_account(short_name='Scenario')
updater = tg.Updater(token=TOKEN, base_url=BOT_API_URL, workers=WORKERS, request_kwargs={"read_timeout": 10, "connect_timeout": 10}, use_context=True)
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
dispatcher = updater.dispatcher
session_name = TOKEN.split(":")[0]
pgram = Client(
    session_name,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
)
print("[Scenario]: Connecting to MongoDB")
mongodb = MongoClient(MONGO_DB_URL, 27017)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
db = motor[MONGO_DB]
engine = AIOEngine(motor, MONGO_DB)
print("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ("https://arq.hamker.in", "WAYBIT-TMRYKK-YUHERI-RLDXRI-ARQ", aiohttpsession)
print("[Scenario]: Initialising string session...")
ubot = TelegramClient(StringSession(STRING_SESSION), APP_ID, APP_HASH)
timeout = httpx.Timeout(40)
http = httpx.AsyncClient(http2=True, timeout=timeout)

async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for pgram in apps:
                if pgram != client:
                    try:
                        entity = await pgram.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = pgram
                        break
            else:
                entity = await pgram.get_chat(entity)
                entity_client = pgram
    return entity, entity_client

apps = [pgram]
DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from scenario.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
