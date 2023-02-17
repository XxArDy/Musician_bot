import shutil
from yt_dlp import YoutubeDL
from aiogram import types, Bot
from keyboards import continue_keyboard


class DownloadMusic:
    def __init__(self, bot: Bot, message: types.Message):
        self.msg = message
        self.bot = bot

    async def download(self):
        message = await self.bot.send_message(self.msg.chat.id, "Загрузка..")
        try:
            if 'https://' in self.msg.text:
                info = YoutubeDL().extract_info(self.msg.text, download=False)
            else:
                info = YoutubeDL().extract_info(f'ytsearch:{self.msg.text}', download=False)['entries'][0]
            filename = f'musics/{self.msg.from_user.id}/{info["title"]}.mp3'

            ydl_options = {'format': 'bestaudio/best',
                           'noplaylist': True,
                           'keepvideo': False,
                           'extractaudio': True,
                           'outtmpl': filename,
                           'postprocessors': [{
                               'key': 'FFmpegExtractAudio',
                               'preferredcodec': 'mp3',
                               'preferredquality': '192',
                           }],
                           }
            try:
                with YoutubeDL(ydl_options) as ydl:
                    ydl.download([info['webpage_url']])
            except Exception as e:
                print(e)
            await message.delete()
            await self.msg.reply_audio(open(filename, 'rb'), reply_markup=continue_keyboard)
            shutil.rmtree(f'musics/{self.msg.from_user.id}', ignore_errors=True)
        except Exception as e:
            print(e)
            await message.delete()
            await self.bot.send_message(self.msg.chat.id, f"{self.msg.text} - таку музику не знайдено!")
