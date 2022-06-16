from datetime import datetime

from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message,
)

from scenario import pgram as Client
from scenario import (
    OWNER_ID as owner_id,
    OWNER_USERNAME as owner_usn,
    SUPPORT_CHAT as log,
)
from scenario.utils.errors import capture_err


"""
    |----╒════════════╕----|
          |  Kang with credits |
          |----- Coded by: ----|
          |       @CoderX      |
          |----(2142595466)----|
          |      on telegram   |
    |----╘════════════╛----|
"""

def content(msg: Message) -> [None, str]:
    text_to_return = msg.text

    if msg.text is None:
        return None
    if " " in text_to_return:
        try:
            return msg.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@Client.on_message(filters.command("feedback"))
@capture_err
async def feedback(_, msg: Message):
    if msg.chat.username:
        chat_username = (f"@{msg.chat.username}/`{msg.chat.id}`")
    else:
        chat_username = (f"ᴩʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴩ/`{msg.chat.id}`")

    feedback = content(msg)
    user_id = msg.from_user.id
    mention = "["+msg.from_user.first_name+"](tg://user?id="+str(msg.from_user.id)+")"
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    thumb = "https://telegra.ph/file/9674161b0ce0b3911b830.jpg"
    
    feedback_report = f"""
**#Feedback : ** **@{owner_usn}**
**Feedback by : ** **{mention}**
**User id: ** **{user_id}**
**Chat : ** **{chat_username}**
**Feedback : ** **{feedback}**
**Feedback time : ** **{datetimes}**"""

    
    if msg.chat.type == "private":
        await msg.reply_text("<b>» This command is only for groups.</b>")
        return

    if user_id == owner_id:
        if feedback:
            await msg.reply_text(
                "<b>» You ediot you're the owner of bot !.</b>",
            )
            return
        else:
            await msg.reply_text(
                "Dumb owner"
            )
    elif user_id != owner_id:
        if feedback:
            await msg.reply_text(
                f"<b>Feedback : {feedback}</b>\n\n"
                "<b>Successfully sent feedback to the Developer</b>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Close", callback_data=f"close_reply")
                        ]
                    ]
                )
            )
            await Client.send_photo(
                log,
                photo=thumb,
                caption=f"{feedback_report}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "• Feedback •", url=f"{msg.link}")
                        ],
                        [
                            InlineKeyboardButton(
                                "• Close •", callback_data="close_send_photo")
                        ]
                    ]
                )
            )
        else:
            await msg.reply_text(
                f"<b>» No new feedbacks !</b>",
            )
        

@Client.on_callback_query(filters.regex("close_reply"))
async def close_reply(msg, CallbackQuery):
    await CallbackQuery.message.delete()

@Client.on_callback_query(filters.regex("close_send_photo"))
async def close_send_photo(_, CallbackQuery):
    is_Admin = await Client.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not is_Admin.can_delete_messages:
        return await CallbackQuery.answer(
            "You can't delete this message", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()


    
__help__ = """
 ❍ /feedback <text> *:* Your feedback to the Developer.
"""
__mod_name__ = "Fᴇᴇᴅʙᴀᴄᴋ"
