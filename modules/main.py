import os
import sys

# ✅ Fix: sys.path set karo taaki modules imports kaam karein
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ✅ Fix: /tmp mein session save karo (Render pe write permission)
os.makedirs("/tmp/bot", exist_ok=True)

import re
import time
import asyncio
import requests
import subprocess

import core as helper
from vars import API_ID, API_HASH, BOT_TOKEN, WEBHOOK, PORT
from utils import progress_bar
from aiohttp import ClientSession
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait

# ✅ Fixed: Removed invalid imports:
# - from pyrogram.types.messages_and_media import message  ← INVALID
# - from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid  ← INVALID
# - from pyromod import listen  ← causes handler blocking

# ── Bot Initialize ──────────────────────────────────────────────
bot = Client(
    "/tmp/bot/bot",   # ✅ Fix: /tmp mein session — Render pe write permission hai
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("""
█░█░█ █▀█ █▀█ █▀▄ █▀▀ █▀█ ▄▀█ █▀▀ ▀█▀
▀▄▀▄▀ █▄█ █▄█ █▄▀ █▄▄ █▀▄ █▀█ █▀░ ░█░
✅ Bot Starting...
""")


# ── /start Command ──────────────────────────────────────────────
# ✅ Fixed: Renamed from account_login to start_handler (duplicate name fix)
@bot.on_message(filters.command(["start"]))
async def start_handler(bot: Client, m: Message):
    await m.reply_text(
        "𝐇𝐞𝐥𝐥𝐨 ❤️\n\n"
        "◆〓◆ ❖ 𝐖𝐃 𝐙𝐎𝐍𝐄 ❖ ™ ◆〓◆\n\n"
        "❈ I Am A Bot For Download Links From Your **.TXT** File "
        "And Then Upload That File On Telegram.\n\n"
        "📌 Send /upload Command And Then Follow Few Steps..",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✜ 𝐉𝐨𝐢𝐧 𝐔𝐩𝐃𝐚𝐭𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 ✜", url="https://t.me/Opleech_WD")],
            [InlineKeyboardButton("✜ 𝗔𝘀𝗵𝘂𝘁𝗼𝘀𝗵𝗚𝗼𝘀𝘄𝗮𝗺𝗶𝟮𝟰 ✜", url="https://t.me/AshutoshGoswami24")],
            [InlineKeyboardButton("🦋 𝐅𝐨𝐥𝐥𝐨𝐰 𝐌𝐞 🦋", url="https://t.me/Opleech_WD")],
        ])
    )


# ── /stop Command ───────────────────────────────────────────────
@bot.on_message(filters.command(["stop"]))
async def stop_handler(_, m: Message):
    await m.reply_text("♦ 𝐒𝐭𝐨𝐩𝐩𝐞𝐝 ♦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


# ── /upload Command ─────────────────────────────────────────────
# ✅ Fixed: Renamed from account_login to upload_handler (duplicate name fix)
@bot.on_message(filters.command(["upload"]))
async def upload_handler(bot: Client, m: Message):

    # Step 1: TXT file lo
    editable = await m.reply_text("𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀 𝐓𝐱𝐭 𝐅𝐢𝐥𝐞 𝐒𝐞𝐧𝐝 𝐇𝐞𝐫𝐞 ⏍")
    input_msg: Message = await bot.listen(editable.chat.id)
    x = await input_msg.download()
    await input_msg.delete(True)

    try:
        with open(x, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        links = []
        for line in content.split("\n"):
            line = line.strip()
            if line and "://" in line:
                parts = line.split("://", 1)
                if len(parts) == 2:
                    links.append(parts)
        os.remove(x)
    except Exception as e:
        await editable.edit(f"∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.\n`{str(e)}`")
        if os.path.exists(x):
            os.remove(x)
        return

    if not links:
        await editable.edit("❌ Koi valid link nahi mila!\nFormat: `Name://https://link`")
        return

    # Step 2: Starting number
    await editable.edit(
        f"∝ 𝐓𝐨𝐭𝐚𝐥 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 𝐀𝐫𝐞 🔗 **{len(links)}**\n\n"
        f"𝐒𝐞𝐧𝐝 𝐅𝐫𝐨𝐦 𝐖𝐡𝐞𝐫𝐞 𝐘𝐨𝐮 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐒𝐭𝐚𝐫𝐭 (default: **1**)"
    )
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text.strip()
    await input0.delete(True)
    try:
        count = max(1, int(raw_text))
    except Exception:
        count = 1

    # Step 3: Batch name
    await editable.edit("∝ 𝐍𝐨𝐰 𝐏𝐥𝐞𝐚𝐬𝐞 𝐒𝐞𝐧𝐝 𝐌𝐞 𝐘𝐨𝐮𝐫 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞")
    input1: Message = await bot.listen(editable.chat.id)
    batch_name = input1.text.strip()
    await input1.delete(True)

    # Step 4: Quality
    await editable.edit(
        "∝ 𝐄𝐧𝐭𝐞𝐫 𝐑𝐞𝐬𝐨𝐥𝐮𝐭𝐢𝐨𝐧 🎬\n"
        "☞ 144 | 240 | 360 | 480 | 720 | 1080\n"
        "Please Choose Quality"
    )
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text.strip()
    await input2.delete(True)

    res_map = {
        "144": "256x144", "240": "426x240", "360": "640x360",
        "480": "854x480", "720": "1280x720", "1080": "1920x1080"
    }
    res = res_map.get(raw_text2, "1280x720")
    if raw_text2 not in res_map:
        raw_text2 = "720"

    # Step 5: Caption
    await editable.edit("✏️ Now Enter A Caption to add on your uploaded file")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text.strip()
    await input3.delete(True)

    highlighter = "️ ⁪⁬⁮⁮⁮"
    MR = highlighter if raw_text3 == "Robin" else raw_text3

    # Step 6: Thumbnail
    await editable.edit(
        "🌄 Now send the Thumb URL\n"
        "Eg » https://graph.org/file/xxx.jpg\n\n"
        "Or if don't want thumbnail send = **no**"
    )
    input6: Message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text.strip() if input6.text else "no"
    await input6.delete(True)
    await editable.delete()

    # ✅ Fixed: thumb == "no" was comparison not assignment, now proper logic
    thumb = "no"
    if raw_text6.startswith("http://") or raw_text6.startswith("https://"):
        try:
            getstatusoutput(f"wget '{raw_text6}' -O '/tmp/bot/thumb.jpg'")
            if os.path.exists("/tmp/bot/thumb.jpg"):
                thumb = "/tmp/bot/thumb.jpg"
        except Exception:
            thumb = "no"

    total = len(links)

    # ── Download Loop ────────────────────────────────────────────
    try:
        for i in range(count - 1, total):
            if len(links[i]) < 2:
                count += 1
                continue

            # ✅ Fixed: 𝗻𝗮𝗺𝗲𝟭 Unicode variable → name1 (normal variable)
            name1 = (links[i][0]
                     .replace("\t", "").replace(":", "").replace("/", "")
                     .replace("+", "").replace("#", "").replace("|", "")
                     .replace("@", "").replace("*", "").replace(".", "")
                     .replace("https", "").replace("http", "").strip())
            name = f"/tmp/bot/{str(count).zfill(3)}) {name1[:60]}"

            V = (links[i][1].strip()
                 .replace("file/d/", "uc?export=download&id=")
                 .replace("www.youtube-nocookie.com/embed", "youtu.be")
                 .replace("?modestbranding=1", "")
                 .replace("/view?usp=sharing", ""))
            url = "https://" + V

            cc  = f"**[ 🎥 ] Vid_ID:** {str(count).zfill(3)}. **{name1}** {MR}\n✉️ 𝐁𝐚𝐭𝐜𝐡 » **{batch_name}**"
            cc1 = f"**[ 📁 ] Pdf_ID:** {str(count).zfill(3)}. **{name1}** {MR}\n✉️ 𝐁𝐚𝐭𝐜𝐡 » **{batch_name}**"

            try:
                # VisionIAS
                if "visionias" in url:
                    async with ClientSession() as session:
                        async with session.get(url, headers={
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Language": "en-US,en;q=0.9",
                            "Cache-Control": "no-cache",
                            "Connection": "keep-alive",
                            "Pragma": "no-cache",
                            "Referer": "http://www.visionias.in/",
                            "Upgrade-Insecure-Requests": "1",
                            "User-Agent": "Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
                        }) as resp:
                            text = await resp.text()
                            match = re.search(r"(https://.*?playlist.m3u8.*?)\"", text)
                            if match:
                                url = match.group(1)
                            else:
                                await m.reply_text(f"⚠️ VisionIAS link fail: `{name1}`")
                                count += 1
                                continue

                # ClassPlus
                elif "videos.classplusapp" in url:
                    try:
                        resp = requests.get(
                            f"https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}",
                            headers={"x-access-token": "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0"},
                            timeout=10
                        )
                        url = resp.json().get("url", url)
                    except Exception:
                        pass

                # MPD to M3U8
                elif "/master.mpd" in url:
                    id_ = url.split("/")[-2]
                    url = f"https://d26g5bnklkwsh4.cloudfront.net/{id_}/master.m3u8"

                # ── Google Drive ──
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                        count += 1
                        if os.path.exists(ka):
                            os.remove(ka)
                        await asyncio.sleep(1)   # ✅ Fixed: time.sleep → await asyncio.sleep
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        continue

                # ── PDF ──
                elif ".pdf" in url.lower():
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}" -R 25 --fragment-retries 25'
                        os.system(cmd)
                        if os.path.exists(f"{name}.pdf"):
                            await bot.send_document(chat_id=m.chat.id, document=f"{name}.pdf", caption=cc1)
                            os.remove(f"{name}.pdf")
                        count += 1
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        continue

                # ── Video ──
                else:
                    if "youtu" in url:
                        ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
                    else:
                        ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

                    if "jw-prod" in url:
                        cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                    else:
                        cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

                    Show = (
                        f"❊⟱ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 ⟱❊ »\n\n"
                        f"📝 𝐍𝐚𝐦𝐞 » `{name1}`\n"
                        f"⌨ 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {raw_text2}p\n"
                        f"🔢 Progress » {count}/{total}\n"
                        f"**🔗 𝐔𝐑𝐋 »** `{url}`"
                    )
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    await helper.send_vid(bot, m, cc, res_file, thumb, name1, prog)
                    count += 1
                    await asyncio.sleep(1)   # ✅ Fixed: time.sleep → await asyncio.sleep

            except FloodWait as e:
                await asyncio.sleep(e.value)
                continue
            except Exception as e:
                await m.reply_text(
                    f"⌘ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n"
                    f"`{str(e)}`\n"
                    f"⌘ 𝐍𝐚𝐦𝐞 » {name1}\n"
                    f"⌘ 𝐋𝐢𝐧𝐤 » `{url}`"
                )
                count += 1
                continue

    except Exception as e:
        await m.reply_text(f"❌ Error: `{str(e)}`")

    # Cleanup thumbnail
    if thumb != "no" and os.path.exists("/tmp/bot/thumb.jpg"):
        os.remove("/tmp/bot/thumb.jpg")

    await m.reply_text(
        f"✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞\n\n"
        f"📦 Batch: **{batch_name}**\n"
        f"🔢 Total: **{total}** files"
    )


# ── Main ─────────────────────────────────────────────────────────
# ✅ Fixed: bot.run() + asyncio.run(main()) conflict removed
#           bot.run() blocked execution, now using asyncio properly
async def main():
    try:
        print("==> Bot connecting...")
        await bot.start()
        print("==> ✅ Bot connected successfully!")
        await asyncio.Event().wait()
    except Exception as e:
        print(f"==> ❌ Bot ERROR: {e}")
        raise
    finally:
        try:
            await bot.stop()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
