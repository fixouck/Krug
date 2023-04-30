 #  __ _                      _    
#  / _(_)                    | |   
# | |_ ___  _____  _   _  ___| | __
# |  _| \ \/ / _ \| | | |/ __| |/ /
# | | | |>  < (_) | |_| | (__|   < 
# |_| |_/_/\_\___/ \__,_|\___|_|\_\
                                  
# Licensed under the GNU GPLv3

# meta developer: @fixouckkk

from .. import loader, utils
from asyncio import sleep


class krugMod(loader.Module):
    """Модуль который превращает видео в кружки"""
    strings = {"name": "krug"}

    async def krugcmd(self, message):
        """Видео"""
        args = utils.get_args_raw(message)

        if not args and not message.is_reply:
            await utils.answer(message, "Ошибка: сообщение или ответ на сообщение должны содержать видео.")
            return

        if not args and message.is_reply:
            reply = await message.get_reply_message()
            if not reply.media:
                await utils.answer(message, "Ошибка: в ответе нет видео.")
                return
            else:
                media = reply.media
        else:
            try:
                first_arg = args.split()[0]
                media = await message.client.download_media(await message.get_reply_message(), bytes)
            except IndexError:
                await utils.answer(message, "Ошибка: в сообщении должно быть указано видео.")
                return
            except AttributeError:
                await utils.answer(message, "Ошибка: в сообщении должно быть указано видео.")
                return
        
        bot = "@videoconverter_bot"
        async with message.client.conversation(bot) as conv:
            enter = await conv.send_file(media)
            await sleep(1)
            krug = await conv.get_response()
            await utils.answer(message, krug)
            await enter.delete()
            await krug.delete()
