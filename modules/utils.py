import os
import sys
import time
import asyncio
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pyrogram.errors import FloodWait


class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False


def hrb(value, digits=2, delim="", postfix=""):
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}{delim}{chosen_unit}{postfix}"


def hrt(seconds, precision=0):
    pieces = []
    value = timedelta(seconds=seconds)
    if value.days:
        pieces.append(f"{value.days}d")
    secs = value.seconds
    if secs >= 3600:
        h = int(secs / 3600)
        pieces.append(f"{h}h")
        secs -= h * 3600
    if secs >= 60:
        m = int(secs / 60)
        pieces.append(f"{m}m")
        secs -= m * 60
    if secs > 0 or not pieces:
        pieces.append(f"{secs}s")
    return "".join(pieces[:precision] if precision else pieces)


timer = Timer()


async def progress_bar(current, total, reply, start):
    if not timer.can_send():
        return
    diff = time.time() - start
    if diff < 1:
        return
    speed = current / diff
    eta = hrt(((total - current) / speed) if speed > 0 else 0, precision=1)
    done = int(current * 11 / total)
    bar = "◆" * done + "◇" * (11 - done)
    try:
        await reply.edit(
            f"<b>\n"
            f" ╭─⌯══⟰ 𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 ⟰══⌯──★\n"
            f"├⚡ {bar} ﹝{current * 100 / total:.1f}%﹞\n"
            f"├🚀 Speed » {hrb(speed)}/s\n"
            f"├📟 Done » {hrb(current)} / {hrb(total)}\n"
            f"├⏱ ETA » {eta}\n"
            f"╰─══ ✪ @Opleech_WD ✪ ══─★\n</b>"
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception:
        pass
