import os
import sys
import time
import asyncio
import logging
import requests
import subprocess
import concurrent.futures

import aiohttp
import aiofiles

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pyrogram import Client
from pyrogram.types import Message
from utils import progress_bar

failed_counter = 0


def duration(filename):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    try:
        return float(result.stdout)
    except Exception:
        return 0


async def download_pdf(url, name):
    filename = f"{name}.pdf"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(filename, mode='wb') as f:
                    await f.write(await resp.read())
    return filename


async def download_video(url, cmd, name):
    global failed_counter
    download_cmd = (
        f'{cmd} -R 25 --fragment-retries 25 '
        f'--external-downloader aria2c '
        f'--downloader-args "aria2c: -x 16 -j 32"'
    )
    print(f"[CMD] {download_cmd}")
    k = subprocess.run(download_cmd, shell=True)
    if "visionias" in cmd and k.returncode != 0 and failed_counter <= 10:
        failed_counter += 1
        await asyncio.sleep(5)
        return await download_video(url, cmd, name)
    failed_counter = 0
    for ext in ["", ".webm", ".mp4", ".mkv"]:
        check = name if not ext else (os.path.splitext(name)[0] + ext)
        if os.path.isfile(check):
            return check
    return os.path.splitext(name)[0] + ".mp4"


async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog):
    thumb_file = f"{filename}.jpg"
    subprocess.run(
        f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{thumb_file}" -y',
        shell=True, stderr=subprocess.DEVNULL
    )
    try:
        await prog.delete(True)
    except Exception:
        pass
    reply = await m.reply_text(f"**⥣ Uploading...** » `{name}`")
    thumbnail = (thumb if thumb and thumb != "no" and os.path.exists(thumb)
                 else thumb_file if os.path.exists(thumb_file) else None)
    dur = int(duration(filename))
    start_time = time.time()
    try:
        await m.reply_video(
            filename, caption=cc,
            supports_streaming=True,
            height=720, width=1280,
            thumb=thumbnail, duration=dur,
            progress=progress_bar,
            progress_args=(reply, start_time)
        )
    except Exception:
        await m.reply_document(
            filename, caption=cc,
            progress=progress_bar,
            progress_args=(reply, start_time)
        )
    if os.path.exists(filename):
        os.remove(filename)
    if os.path.exists(thumb_file):
        os.remove(thumb_file)
    await reply.delete(True)
