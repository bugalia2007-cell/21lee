import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Render pe session file /tmp mein save karo
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

bot = Client(
    "/tmp/bot/bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@bot.on_message(filters.command(["start"]))
async def start_handler(bot: Client, m: Message):
    await m.reply_text(
        "**𝐇𝐞𝐥𝐥𝐨 ❤️**\n\n"
        "◆〓◆ ❖ 𝐖𝐃 𝐙𝐎𝐍𝐄 ❖ ™ ◆〓◆\n\n"
        "❈ Main ek bot hoon jo tumhari **.TXT** file ke links\n"
        "download karke Telegram pe upload karta hoon!\n\n"
        "📌 **Shuru karne ke liye:** /upload bhejo",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✜ Join Channel ✜", url="https://t.me/Opleech_WD")],
        ])
    )


@bot.on_message(filters.command(["stop"]))
async def stop_handler(_, m: Message):
    await m.reply_text("♦ Stopped ♦")
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["upload"]))
async def upload_handler(bot: Client, m: Message):
    editable = await m.reply_text("📂 **Apni .TXT file bhejo**")
    input_msg = await bot.listen(editable.chat.id)
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
        await editable.edit(f"❌ Error: `{str(e)}`")
        if os.path.exists(x):
            os.remove(x)
        return

    if not links:
        await editable.edit("❌ Koi valid link nahi mila!\nFormat: `Name://https://link`")
        return

    await editable.edit(f"✅ **{len(links)} links mile!**\n\nKis number se start karein? (default: 1)")
    input0 = await bot.listen(editable.chat.id)
    try:
        start_from = max(1, int(input0.text.strip()))
    except:
        start_from = 1
    await input0.delete(True)

    await editable.edit("✏️ **Batch ka naam bhejo:**")
    input1 = await bot.listen(editable.chat.id)
    batch_name = input1.text.strip()
    await input1.delete(True)

    await editable.edit("🎬 **Quality:** 144 | 240 | 360 | 480 | 720 | 1080")
    input2 = await bot.listen(editable.chat.id)
    quality = input2.text.strip()
    await input2.delete(True)
    if quality not in ["144", "240", "360", "480", "720", "1080"]:
        quality = "720"

    await editable.edit("📝 **Caption bhejo:**")
    input3 = await bot.listen(editable.chat.id)
    caption_text = input3.text.strip()
    await input3.delete(True)

    await editable.edit("🖼️ **Thumbnail URL** (ya **no**):")
    input6 = await bot.listen(editable.chat.id)
    thumb_input = input6.text.strip() if input6.text else "no"
    await input6.delete(True)
    await editable.delete()

    thumb = "no"
    if thumb_input.startswith("http://") or thumb_input.startswith("https://"):
        try:
            getstatusoutput(f"wget '{thumb_input}' -O '/tmp/bot/thumb.jpg'")
            if os.path.exists("/tmp/bot/thumb.jpg"):
                thumb = "/tmp/bot/thumb.jpg"
        except:
            pass

    count = start_from
    total = len(links)

    for i in range(start_from - 1, total):
        if len(links[i]) < 2:
            count += 1
            continue

        name1 = (links[i][0]
                 .replace("\t","").replace(":","").replace("/","")
                 .replace("+","").replace("#","").replace("|","")
                 .replace("@","").replace("*","").replace(".","")
                 .replace("https","").replace("http","").strip())
        name = f"/tmp/bot/{str(count).zfill(3)}) {name1[:50]}"
        url = "https://" + (links[i][1].strip()
                            .replace("file/d/","uc?export=download&id=")
                            .replace("www.youtube-nocookie.com/embed","youtu.be")
                            .replace("?modestbranding=1","")
                            .replace("/view?usp=sharing",""))

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
                            await m.reply_text(f"⚠️ VisionIAS fail: `{name1}`")
                            count += 1
                            continue

            elif "/master.mpd" in url:
                id_ = url.split("/")[-2]
                url = f"https://d26g5bnklkwsh4.cloudfront.net/{id_}/master.m3u8"

            if "drive.google" in url:
                ka = await helper.download_pdf(url, name)
                await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                count += 1
                if os.path.exists(ka):
                    os.remove(ka)
                await asyncio.sleep(1)

            elif ".pdf" in url.lower():
                os.system(f'yt-dlp -o "{name}.pdf" "{url}" -R 25')
                if os.path.exists(f"{name}.pdf"):
                    await bot.send_document(chat_id=m.chat.id, document=f"{name}.pdf", caption=cc1)
                    os.remove(f"{name}.pdf")
                count += 1

            else:
                ytf = (f"b[height<={quality}][ext=mp4]/bv[height<={quality}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
                       if "youtu" in url else
                       f"b[height<={quality}]/bv[height<={quality}]+ba/b/bv+ba")
                cmd = (f'yt-dlp -o "{name}.mp4" "{url}"' if "jw-prod" in url
                       else f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"')

                prog = await m.reply_text(
                    f"⬇️ **Downloading...**\n\n"
                    f"📝 `{name1}`\n🎬 {quality}p | 🔢 {count}/{total}")
                res_file = await helper.download_video(url, cmd, name)
                await helper.send_vid(bot, m, cc, res_file, thumb, name1, prog)
                count += 1
                await asyncio.sleep(1)

        except FloodWait as e:
            await asyncio.sleep(e.value)
            continue
        except Exception as e:
            await m.reply_text(f"❌ `{str(e)}`\n📝 `{name1}`")
            count += 1
            continue

    if thumb != "no" and os.path.exists("/tmp/bot/thumb.jpg"):
        os.remove("/tmp/bot/thumb.jpg")

    await m.reply_text(f"✅ **Done!**\n📦 {batch_name} | 🔢 {total} files")


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
        except:
            pass


if __name__ == "__main__":
    asyncio.run(main())
