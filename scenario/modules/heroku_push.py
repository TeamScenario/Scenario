import asyncio
import math
import os
import dotenv
import random
import shutil
from datetime import datetime
from time import strftime, time

import heroku3
import requests
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import Client, filters
from pyrogram.types import Message

from scenario import (HEROKU_API_KEY, HEROKU_APP_NAME, UPSTREAM_BRANCH,
                    UPSTREAM_REPO)
from scenario import JOIN_LOGGER
from scenario import pgram, DEV_USERS
from scenario.utils.heroku import is_heroku, user_input
from scenario.utils.paste import isPreviewUp, paste_queue

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


BOT_NAME = "Scenario"


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(HEROKU_API_KEY),
    "https",
    str(HEROKU_APP_NAME),
    "HEAD",
    "main",
]


@pgram.on_message(filters.command(["set_var", "setvar"]) & filters.user(DEV_USERS))
async def set_var(client, message):
    usage = "**ᴇxᴀᴍᴩʟᴇ :**\n/set_var [ᴠᴀʀɪᴀʙʟᴇ ɴᴀᴍᴇ] [ᴠᴀʟᴜᴇ]"
    if len(message.command) < 3:
        return await message.reply_text(usage)
    to_set = message.text.split(None, 2)[1].strip()
    value = message.text.split(None, 2)[2].strip()
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "» ғɪʟʟ ᴛʜᴇ `HEROKU_API_KEY` ᴀɴᴅ `HEROKU_APP_NAME` ᴠᴀʀɪᴀʙʟᴇ "
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "» ᴩʟᴇᴀsᴇ ᴀᴅᴅ `HEROKU_API_KEY` ᴀɴᴅ `HEROKU_APP_NAME` ᴠᴀʀɪᴀʙʟᴇs !"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                "» ʏᴏᴜʀ **ʜᴇʀᴏᴋᴜ ᴀᴩɪ ᴋᴇʏ** ᴀɴᴅ **ʜᴇʀᴏᴋᴜ ᴀᴩᴩ ɴᴀᴍᴇ** ɪs ᴡʀᴏɴɢ.\n\nᴩʟᴇᴀsᴇ ɢᴏ ᴀɴᴅ ᴄʜᴇᴄᴋ !"
            )
        heroku_config = happ.config()
        if to_set in heroku_config:
            await message.reply_text(
                f"`{to_set}` ʜᴀs ʙᴇᴇɴ ᴜᴩᴅᴀᴛᴇs sᴜᴄᴄᴇssғᴜʟʟʏ."
            )
        else:
            await message.reply_text(
                f"`{to_set}` ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ."
            )
        heroku_config[to_set] = value
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(".env not found.")
        output = dotenv.set_key(path, to_set, value)
        if dotenv.get_key(path, to_set):
            return await message.reply_text(f"`{to_set}` ʜᴀs ʙᴇᴇɴ ᴜᴩᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ, ᴩʟᴇᴀsᴇ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ʙʏ /restart ᴄᴏᴍᴍᴀɴᴅ.")
        else:
            return await message.reply_text(f"`{to_set}` ʜᴀs ʙᴇᴇɴ ᴜᴩᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ, ᴩʟᴇᴀsᴇ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ʙʏ /restart ᴄᴏᴍᴍᴀɴᴅ.")


@pgram.on_message(filters.command(["usage", "dynos"]) & filters.user(DEV_USERS))
async def usage_dynos(client, message):
    ### Credits CatUserbot
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "» ғɪʟʟ ᴛʜᴇ `HEROKU_API_KEY` ᴀɴᴅ `HEROKU_APP_NAME` ᴠᴀʀɪᴀʙʟᴇ "
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "» ᴩʟᴇᴀsᴇ ᴀᴅᴅ `HEROKU_API_KEY` ᴀɴᴅ `HEROKU_APP_NAME` ᴠᴀʀɪᴀʙʟᴇs !"
            )
    else:
        return await message.reply_text("**» ᴏɴʟʏ ғᴏʀ ʜᴇʀᴏᴋᴜ ᴀᴩᴩʟɪᴄᴀᴛɪᴏɴs.**")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(
            "» ʏᴏᴜʀ **ʜᴇʀᴏᴋᴜ ᴀᴩɪ ᴋᴇʏ** ᴀɴᴅ **ʜᴇʀᴏᴋᴜ ᴀᴩᴩ ɴᴀᴍᴇ** ɪs ᴡʀᴏɴɢ.\n\nᴩʟᴇᴀsᴇ ɢᴏ ᴀɴᴅ ᴄʜᴇᴄᴋ !"
        )
    dyno = await message.reply_text("**» ɢᴇᴛᴛɪɴɢ ᴅʏɴᴏs ᴜsᴀɢᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ғʀᴏᴍ ʜᴇʀᴏᴋᴜ.**")
    account_id = Heroku.account().id
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get("https://api.heroku.com" + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("**» ғᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴅʏɴᴏs ᴜsᴀɢᴇ ғʀᴏᴍ ʜᴇʀᴏᴋᴜ.**")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    text = f"""
**ᴅʏɴᴏ ᴜsᴀɢᴇ**

<u>ᴜsᴀɢᴇ :</u>
ᴛᴏᴛᴀʟ ᴜsᴇᴅ : `{AppHours}`**ʜ**  `{AppMinutes}`**ᴍ**  [`{AppPercentage}`**%**]

<u>ʀᴇᴍᴀɪɴɪɴɢ ᴅʏɴᴏs :</u>
ᴛᴏᴛᴀʟ ʟᴇғᴛ : `{hours}`**ʜ**  `{minutes}`**ᴍ**  [`{percentage}`**%**]"""
    return await dyno.edit(text)


@pgram.on_message(filters.command(["update", "gitpull"]) & filters.user(DEV_USERS))
async def update_(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "» ғɪʟʟ ᴛʜᴇ `HEROKU_API_KEY` ᴀɴᴅ `HEROKU_APP_NAME` ᴠᴀʀɪᴀʙʟᴇ "
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "» ᴩʟᴇᴀsᴇ ᴀᴅᴅ `HEROKU_API_KEY` ᴀɴᴅ `HEROKU_APP_NAME` ᴠᴀʀɪᴀʙʟᴇs !"
            )
    response = await message.reply_text("**» sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴜᴩᴅᴀᴛᴇs ᴏɴ ᴜᴩsᴛʀᴇᴀᴍ ʀᴇᴩᴏ...**")
    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit("**» ɢɪᴛ ᴄᴏᴍᴍᴀɴᴅ ᴇʀʀᴏʀ.**")
    except InvalidGitRepositoryError:
        return await response.edit("**» ɪɴᴠᴀʟɪᴅ ᴜᴩsᴛʀᴇᴀᴍ ʀᴇᴩᴏ.**")
    to_exc = f"git fetch origin {UPSTREAM_BRANCH} &> /dev/null"
    os.system(to_exc)
    await asyncio.sleep(7)
    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]  # main git repository
    for checks in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        verification = str(checks.count())
    if verification == "":
        return await response.edit(f"**» {BOT_NAME} ɪs ᴜᴩ-ᴛᴏ-ᴅᴀᴛᴇ ᴡɪᴛʜ ᴜᴩsᴛʀᴇᴀᴍ ʀᴇᴩᴏ !**")
    updates = ""
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[
            (format // 10 % 10 != 1) * (format % 10 < 4) * format % 10 :: 4
        ],
    )
    for info in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        updates += f"<b>⇆ #{info.count()}: [{info.summary}]({REPO_}/commit/{info}) by -> {info.author}</b>\n\t\t\t\t<b>➥ ᴄᴏᴍᴍɪᴛᴇᴅ ᴏɴ :</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
    _update_response_ = "<b>ɴᴇᴡ ᴜᴩᴅᴀᴛᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ʙᴏᴛ !</b>\n\n➣ ᴩᴜsʜɪɴɢ ᴜᴩᴅᴀᴛᴇs ɴᴏᴡ...</code>\n\n**<u>ᴜᴩᴅᴀᴛᴇs :</u>**\n\n"
    _final_updates_ = _update_response_ + updates
    if len(_final_updates_) > 4096:
        link = await paste_queue(updates)
        url = link + "/index.txt"
        nrs = await response.edit(
            f"<b>ɴᴇᴡ ᴜᴩᴅᴀᴛᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ʙᴏᴛ !</b>\n\n➣ ᴩᴜsʜɪɴɢ ᴜᴩᴅᴀᴛᴇs ɴᴏᴡ...</code>\n\n**<u>ᴜᴩᴅᴀᴛᴇs :</u>**\n\n[ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴄʜᴇᴄᴋ ᴄᴏᴍᴍɪᴛs]({url})"
        )
    else:
        nrs = await response.edit(
            _final_updates_, disable_web_page_preview=True
        )
    os.system("git stash &> /dev/null && git pull")
    if await is_heroku():
        try:
            await response.edit(
                f"{nrs.text}\n\nʙᴏᴛ ᴜᴩᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.\n\nɴᴏᴡ ʟᴇᴛ ᴍᴇ ʀᴇsᴛᴀʀᴛ ᴛᴏ ᴩᴜsʜ ᴛʜᴇ ᴄʜᴀɴɢᴇs !"
            )
            os.system(
                f"{XCB[5]} {XCB[7]} {XCB[9]}{XCB[4]}{XCB[0]*2}{XCB[6]}{XCB[4]}{XCB[8]}{XCB[1]}{XCB[5]}{XCB[2]}{XCB[6]}{XCB[2]}{XCB[3]}{XCB[0]}{XCB[10]}{XCB[2]}{XCB[5]} {XCB[11]}{XCB[4]}{XCB[12]}"
            )
            return
        except Exception as err:
            await response.edit(
                f"{nrs.text}\n\nsᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜᴇɴ ᴛʀɪᴇᴅ ᴛᴏ ʀᴇsᴛᴀʀᴛ, ᴩʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ʟᴏɢs."
            )
            return await pgram.send_message(
                JOIN_LOGGER,
                f"AN EXCEPTION OCCURRED AT #UPDATER DUE TO: <code>{err}</code>",
            )
    else:
        await response.edit(
            f"{nrs.text}\n\nʙᴏᴛ ᴜᴩᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.\n\nɴᴏᴡ ʟᴇᴛ ᴍᴇ ʀᴇsᴛᴀʀᴛ ᴛᴏ ᴩᴜsʜ ᴛʜᴇ ᴄʜᴀɴɢᴇs !"
        )
        os.system("pip3 install -r requirements.txt")
        os.system(f"kill -9 {os.getpid()} && bash start")
        exit()
    return
