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
PTB 13.7 Comming Soon
```
