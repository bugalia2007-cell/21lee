import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, WEBHOOK, PORT
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from aiohttp import web

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
# BUG FIX: StickerEmojiInvalid import galat module se tha aur use nahi ho raha tha → ImportError
# BUG FIX: `from pyrogram.types.messages_and_media import message` → unused + wrong casing → remove kiya

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://text-leech-bot-for-render.onrender.com/")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app


# BUG FIX: /start handler ka naam `account_login` tha aur /upload ka bhi → dono same naam hone se
# /start wala handler overwrite ho jaata tha, /start kaam nahi karta tha
@bot.on_message(filters.command(["start"]))
async def start_handler(bot: Client, m: Message):
    await m.reply_text(
        f"𝐇𝐞𝐥𝐥𝐨 ❤️\n\n◆〓◆ ❖ 𝐖𝐃 𝐙𝐎𝐍𝐄 ❖ ™ ◆〓◆\n\n"
        f"❈ I Am A Bot For Download Links From Your **.TXT** File And Then Upload That File On Telegram. "
        f"Send ⟰ /upload Command And Then Follow Few Steps..",
        reply_markup=None
    )


@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("♦ 𝐒𝐭𝐨𝐩𝐩𝐞𝐝 ♦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["upload"]))
async def upload_handler(bot: Client, m: Message):
    editable = await m.reply_text('𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀 𝐓𝐱𝐭 𝐅𝐢𝐥𝐞 𝐒𝐞𝐧𝐝 𝐇𝐞𝐫𝐞 ⏍')
    input_msg: Message = await bot.listen(editable.chat.id)
    x = await input_msg.download()
    await input_msg.delete(True)

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            i = i.strip()
            if i:
                links.append(i.split("://", 1))
        os.remove(x)
    except Exception:
        await m.reply_text("∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.")
        if os.path.exists(x):
            os.remove(x)
        return

    # BUG FIX: agar koi bhi valid link nahi hai to crash hota tha
    if not links:
        await editable.edit("∝ 𝐅𝐢𝐥𝐞 𝐦𝐞𝐢𝐧 𝐤𝐨𝐢 𝐥𝐢𝐧𝐤 𝐧𝐚𝐡𝐢𝐧 𝐦𝐢𝐥𝐚.")
        return

    await editable.edit(
        f"∝ 𝐓𝐨𝐭𝐚𝐥 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 🔗** **{len(links)}**\n\n"
        f"𝐒𝐞𝐧𝐝 𝐅𝐫𝐨𝐦 𝐖𝐡𝐞𝐫𝐞 𝐘𝐨𝐮 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐈𝐧𝐢𝐭𝐚𝐥 𝐢𝐬 **1**"
    )
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("∝ 𝐍𝐨𝐰 𝐏𝐥𝐞𝐚𝐬𝐞 𝐒𝐞𝐧𝐝 𝐌𝐞 𝐘𝐨𝐮𝐫 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    await editable.edit("∝ 𝐄𝐧𝐭𝐞𝐫 𝐑𝐞𝐬𝐨𝐥𝐮𝐭𝐢𝐨𝐧 🎬\n☞ 144,240,360,480,720,1080\nPlease Choose Quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)

    res_map = {
        "144": "256x144", "240": "426x240", "360": "640x360",
        "480": "854x480", "720": "1280x720", "1080": "1920x1080"
    }
    res = res_map.get(raw_text2, "UN")

    await editable.edit("✏️ Now Enter A Caption to add on your uploaded file")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)

    highlighter = "️ ⁪⁬⁮⁮⁮"
    MR = highlighter if raw_text3 == 'Robin' else raw_text3

    await editable.edit(
        "🌄 Now send the Thumb url\nEg » https://graph.org/file/419c60736fbac058c9e50.jpg\n\n"
        "Or if don't want thumbnail send = no"
    )
    input6: Message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = raw_text6.strip()
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        # BUG FIX: pehle `thumb == "no"` tha yani comparison tha, assignment nahi tha
        # isliye thumb kabhi "no" set nahi hota tha → thumbnail logic galat tha
        thumb = "no"

    count = 1 if len(links) == 1 else int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            # BUG FIX: agar link split se sirf ek part mile (protocol missing) to crash hota tha
            if len(links[i]) < 2:
                await m.reply_text(f"⚠️ Invalid link at line {i+1}, skipping...")
                count += 1
                continue

            V = (links[i][1]
                 .replace("file/d/", "uc?export=download&id=")
                 .replace("www.youtube-nocookie.com/embed", "youtu.be")
                 .replace("?modestbranding=1", "")
                 .replace("/view?usp=sharing", ""))
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Pragma': 'no-cache',
                        'Referer': 'http://www.visionias.in/',
                        'Sec-Fetch-Dest': 'iframe',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'cross-site',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36',
                    }) as resp:
                        text = await resp.text()
                        match = re.search(r"(https://.*?playlist.m3u8.*?)\"", text)
                        if match:
                            url = match.group(1)
                        else:
                            await m.reply_text(f"⚠️ VisionIAS URL parse fail: {url}")
                            count += 1
                            continue

            elif 'videos.classplusapp' in url:
                url = requests.get(
                    f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}',
                    headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9...'}
                ).json()['url']

            elif '/master.mpd' in url:
                id_ = url.split("/")[-2]
                url = "https://d26g5bnklkwsh4.cloudfront.net/" + id_ + "/master.m3u8"

            # BUG FIX: `𝗻𝗮𝗺𝗲𝟭` Unicode bold variable tha jo defined nahi tha → NameError
            # Sahi variable naam `name1` hai
            name1 = (links[i][0]
                     .replace("\t", "").replace(":", "").replace("/", "")
                     .replace("+", "").replace("#", "").replace("|", "")
                     .replace("@", "").replace("*", "").replace(".", "")
                     .replace("https", "").replace("http", "").strip())
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            # BUG FIX: cc aur cc1 mein `𝗻𝗮𝗺𝗲𝟭` Unicode variable tha → NameError
            cc  = f'**[ 🎥 ] Vid_ID:** {str(count).zfill(3)}. **{name1}** {MR}\n✉️ 𝐁𝐚𝐭𝐜𝐡 » **{raw_text0}**'
            cc1 = f'**[ 📁 ] Pdf_ID:** {str(count).zfill(3)}. **{name1}** {MR}\n✉️ 𝐁𝐚𝐭𝐜𝐡 » **{raw_text0}**'

            try:
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                        count += 1
                        os.remove(ka)
                        await asyncio.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        # BUG FIX: time.sleep() async context mein event loop block karta tha
                        await asyncio.sleep(e.value)
                        continue

                elif ".pdf" in url:
                    try:
                        cmd_pdf = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd_pdf} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        if os.path.exists(f'{name}.pdf'):
                            os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        await asyncio.sleep(e.value)
                        continue

                else:
                    Show = (
                        f"❊⟱ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 ⟱❊ »\n\n"
                        f"📝 𝐍𝐚𝐦𝐞 » `{name}`\n"
                        f"⌨ 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {raw_text2}`\n\n"
                        f"**🔗 𝐔𝐑𝐋 »** `{url}`"
                    )
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    await asyncio.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"⌘ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n{str(e)}\n⌘ 𝐍𝐚𝐦𝐞 » {name}\n⌘ 𝐋𝐢𝐧𝐤 » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(str(e))

    await m.reply_text("✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞")


print("""
█░█░█ █▀█ █▀█ █▀▄ █▀▀ █▀█ ▄▀█ █▀▀ ▀█▀     ▄▀█ █▀ █░█ █░█ ▀█▀ █▀█ █▀█ █▀█   ░ █▀▀
▀▄▀▄▀ █▄█ █▄█ █▄▀ █▄▄ █▀▄ █▀█ █▀░ ░█░     █▀█ ▄█ █▀█ █▄█ ░█░ █▄█ ▄█ █▀█   ▄ █▄▄""")
print("✅ 𝐃𝐞𝐩𝐥𝐨𝐲 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 ✅")
print("✅ 𝐁𝐨𝐭 𝐖𝐨𝐫𝐤𝐢𝐧𝐠 ✅")


async def main():
    if WEBHOOK:
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    await bot.start()
    print("Bot is up and running")

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        await bot.stop()


# BUG FIX: pehle `bot.run()` aur `asyncio.run(main())` dono saath the
# bot.run() blocking call hai → main() kabhi execute nahi hota tha
# Ab sirf asyncio.run(main()) use kiya jo sahi hai
if __name__ == "__main__":
    asyncio.run(main())

