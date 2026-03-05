import os
import re
import sys
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
from pyromod import listen

# ── Bot Initialize ──────────────────────────────────────────────
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("""
╔══════════════════════════════════════╗
║      TEXT LEECH BOT - Starting...   ║
║         By WD ZONE @Opleech_WD      ║
╚══════════════════════════════════════╝
""")


# ── /start Command ──────────────────────────────────────────────
@bot.on_message(filters.command(["start"]))
async def start_handler(bot: Client, m: Message):
    await m.reply_text(
        "**𝐇𝐞𝐥𝐥𝐨 ❤️**\n\n"
        "◆〓◆ ❖ 𝐖𝐃 𝐙𝐎𝐍𝐄 ❖ ™ ◆〓◆\n\n"
        "❈ Main ek bot hoon jo tumhari **.TXT** file ke links\n"
        "download karke Telegram pe upload karta hoon!\n\n"
        "📌 **Shuru karne ke liye:** /upload bhejo",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✜ Join Update Channel ✜", url="https://t.me/Opleech_WD")],
            [InlineKeyboardButton("🦋 Follow Me 🦋", url="https://t.me/Opleech_WD")]
        ])
    )


# ── /stop Command ───────────────────────────────────────────────
@bot.on_message(filters.command(["stop"]))
async def stop_handler(_, m: Message):
    await m.reply_text("♦ 𝐒𝐭𝐨𝐩𝐩𝐞𝐝 ♦")
    os.execl(sys.executable, sys.executable, *sys.argv)


# ── /upload Command ─────────────────────────────────────────────
@bot.on_message(filters.command(["upload"]))
async def upload_handler(bot: Client, m: Message):

    editable = await m.reply_text("📂 **Apni .TXT file bhejo** ⏍")
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
        await editable.edit(f"❌ **File read nahi hui:**\n`{str(e)}`")
        if os.path.exists(x):
            os.remove(x)
        return

    if not links:
        await editable.edit("❌ **File mein koi valid link nahi mila!**\n\nFormat:\n`Video Name://https://link`")
        return

    await editable.edit(
        f"✅ **{len(links)} links mile!**\n\n"
        f"📌 Kis number se start karein? (default: **1**)"
    )
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text.strip()
    await input0.delete(True)
    try:
        start_from = max(1, int(raw_text))
    except Exception:
        start_from = 1

    await editable.edit("✏️ **Batch ka naam bhejo:**")
    input1: Message = await bot.listen(editable.chat.id)
    batch_name = input1.text.strip()
    await input1.delete(True)

    await editable.edit(
        "🎬 **Video Quality chunno:**\n\n"
        "144 | 240 | 360 | 480 | 720 | 1080"
    )
    input2: Message = await bot.listen(editable.chat.id)
    quality = input2.text.strip()
    await input2.delete(True)

    res_map = {
        "144": "256x144", "240": "426x240", "360": "640x360",
        "480": "854x480", "720": "1280x720", "1080": "1920x1080"
    }
    if quality not in res_map:
        quality = "720"

    await editable.edit("📝 **Caption bhejo:**")
    input3: Message = await bot.listen(editable.chat.id)
    caption_text = input3.text.strip()
    await input3.delete(True)

    await editable.edit(
        "🖼️ **Thumbnail URL bhejo:**\n"
        "Ya thumbnail nahi chahiye to **no** bhejo"
    )
    input6: Message = await bot.listen(editable.chat.id)
    thumb_input = input6.text.strip() if input6.text else "no"
    await input6.delete(True)
    await editable.delete()

    thumb = "no"
    if thumb_input.startswith("http://") or thumb_input.startswith("https://"):
        try:
            getstatusoutput(f"wget '{thumb_input}' -O 'thumb.jpg'")
            if os.path.exists("thumb.jpg"):
                thumb = "thumb.jpg"
        except Exception:
            thumb = "no"

    count = start_from
    total = len(links)

    for i in range(start_from - 1, total):
        if len(links[i]) < 2:
            count += 1
            continue

        name1 = (links[i][0]
                 .replace("\t", "").replace(":", "").replace("/", "")
                 .replace("+", "").replace("#", "").replace("|", "")
                 .replace("@", "").replace("*", "").replace(".", "")
                 .replace("https", "").replace("http", "").strip())
        name = f"{str(count).zfill(3)}) {name1[:55]}"

        raw_url = links[i][1].strip()
        V = (raw_url
             .replace("file/d/", "uc?export=download&id=")
             .replace("www.youtube-nocookie.com/embed", "youtu.be")
             .replace("?modestbranding=1", "")
             .replace("/view?usp=sharing", ""))
        url = "https://" + V

        cc  = f"**[ 🎥 ] {str(count).zfill(3)}. {name1}**\n{caption_text}\n✉️ Batch » **{batch_name}**"
        cc1 = f"**[ 📁 ] {str(count).zfill(3)}. {name1}**\n{caption_text}\n✉️ Batch » **{batch_name}**"

        try:
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36',
                        'Referer': 'http://www.visionias.in/',
                    }) as resp:
                        text = await resp.text()
                        match = re.search(r"(https://.*?playlist.m3u8.*?)\"", text)
                        if match:
                            url = match.group(1)
                        else:
                            await m.reply_text(f"⚠️ VisionIAS link fail: `{name}`")
                            count += 1
                            continue

            elif "videos.classplusapp" in url:
                try:
                    resp = requests.get(
                        f"https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}",
                        headers={"x-access-token": "your_token_here"}, timeout=10
                    )
                    url = resp.json().get("url", url)
                except Exception:
                    pass

            elif "/master.mpd" in url:
                id_ = url.split("/")[-2]
                url = f"https://d26g5bnklkwsh4.cloudfront.net/{id_}/master.m3u8"

            if "drive.google" in url or "drive" in url:
                try:
                    ka = await helper.download_pdf(url, name)
                    await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                    count += 1
                    if os.path.exists(ka):
                        os.remove(ka)
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    continue

            elif ".pdf" in url.lower():
                try:
                    cmd_pdf = f'yt-dlp -o "{name}.pdf" "{url}" -R 25 --fragment-retries 25'
                    os.system(cmd_pdf)
                    pdf_file = f"{name}.pdf"
                    if os.path.exists(pdf_file):
                        await bot.send_document(chat_id=m.chat.id, document=pdf_file, caption=cc1)
                        os.remove(pdf_file)
                    count += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    continue

            else:
                if "youtu" in url:
                    ytf = f"b[height<={quality}][ext=mp4]/bv[height<={quality}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
                else:
                    ytf = f"b[height<={quality}]/bv[height<={quality}]+ba/b/bv+ba"

                if "jw-prod" in url:
                    cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                else:
                    cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

                prog = await m.reply_text(
                    f"⬇️ **Downloading...**\n\n"
                    f"📝 **Name:** `{name}`\n"
                    f"🎬 **Quality:** {quality}p\n"
                    f"🔢 **Progress:** {count}/{total}\n"
                    f"🔗 **URL:** `{url}`"
                )
                res_file = await helper.download_video(url, cmd, name)
                await helper.send_vid(bot, m, cc, res_file, thumb, name, prog)
                count += 1
                await asyncio.sleep(1)

        except FloodWait as e:
            await asyncio.sleep(e.value)
            continue
        except Exception as e:
            await m.reply_text(
                f"❌ **Error:**\n`{str(e)}`\n\n"
                f"📝 Name: `{name}`\n🔗 URL: `{url}`"
            )
            count += 1
            continue

    if thumb != "no" and os.path.exists("thumb.jpg"):
        os.remove("thumb.jpg")

    await m.reply_text(
        f"✅ **Kaam Poora!**\n\n"
        f"📦 Batch: **{batch_name}**\n"
        f"🔢 Total: **{total}** files"
    )


# ── Main ─────────────────────────────────────────────────────────
async def main():
    await bot.start()
    print("✅ Bot is Running!")
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
