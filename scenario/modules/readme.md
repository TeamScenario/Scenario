# Scenario Example plugin format

## Advanced: Pyrogram
```python3
from pyrogram import filters
from scenario import pgram

@pgram.on_message(filters.command("kick"))
async def hmm(_, message):
    await message.reply_text(
        "Kicked"
    )
    
__mod_name__ = "Kick"
__help__ = """
*Hi*
- /kick: Kicked !
"""
```

## Advanced: Telethon
```python3
from scenario import telethn
from scenario.events import register

@register(pattern="^/ban$")
async def _(event):
    j = "BANNED ONE"
    await event.reply(j)
    
__mod_name__ = "ban"
__help__ = """
*Ban user*
- /ban - Banned!
"""
```

## Advanced: PTB
```
from scenario import dispatcher
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler

def adv(update: Update, context: CallbackContext):
    m = update.effective_message
    text="*Hello world*"
    m.reply_text(text, parse_mode=ParseMode.MARKDOWN)

dispatcher.add_handler(CommandHandler("ok", adv, run_async=True))

# Command = ok

```
