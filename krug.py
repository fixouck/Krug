from .. import loader
from moviepy.editor import *
import os
import tempfile
import math


#  __ _                      _
# / _(_)                    | |
# | |_ ___  _____  _   _  ___| | __
# |  _| \ \/ / _ \| | | |/ __| |/ /
# | | | |>  < (_) | |_| | (__|   <
# |_| |_/_/\_\___/ \__,_|\___|_|\_\

# Licensed under the GNU GPLv3
# meta developer: @fix_mods

@loader.tds
class KrugMod(loader.Module):
    """Превращает видео в видеосообщение"""
    strings = {"name": "Krug"}

    async def krugcmd(self, message):
        """Превращает видео размером не больше 8 МБ и форматом 1:1 в видеосообщение"""
        reply = await message.get_reply_message()
        if not reply or not reply.file or reply.file.mime_type.split("/")[0] != "video":
            await message.edit("❌ Ответьте на видео размером не больше 8 МБ и форматом 1:1.")
            return

        if reply.file.size > 8 * 1024 * 1024:
            await message.edit("❌ Размер видео должен быть не больше 8 МБ.")
            return

        await message.edit("⏳ Обработка видео...")

        video_path = await reply.download_media()
        video = VideoFileClip(video_path)

        if not math.isclose(video.aspect_ratio, 1, rel_tol=1e-2):
            video.close()
            os.remove(video_path)
            await message.edit("❌ Формат видео должен быть 1:1.")
            return

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
            video.write_videofile(temp_video.name, codec="libx264", threads=4)

        video.close()
        os.remove(video_path)

        await message.delete()
        await message.client.send_file(
            message.to_id,
            temp_video.name,
            reply_to=reply.id,
            video_note=True
        )
        os.remove(temp_video.name)

async def kruggcmd(self, message):
    """Сжимает видео до 1:1"""
    reply = await message.get_reply_message()
    if not reply or not reply.file or reply.file.mime_type.split("/")[0] != "video":
        await message.edit("❌ Ответьте на видео размером не больше 8 МБ.")
        return

    if reply.file.size > 8 * 1024 * 1024:
        await message.edit("❌ Размер видео должен быть не больше 8 МБ.")
        return

    await message.edit("⏳ Обработка видео...")

    video_path = await reply.download_media()
    video = VideoFileClip(video_path)

    max_dimension = max(video.size)
    resized_video = video.resize((max_dimension, max_dimension))

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
        resized_video.write_videofile(temp_video.name, codec="libx264", threads=4)

    video.close()
    resized_video.close()
    os.remove(video_path)

    await message.delete()
    await message.client.send_file(
        message.to_id,
        temp_video.name,
        reply_to=reply.id,
        video_note=True
    )
    os.remove(temp_video.name)
