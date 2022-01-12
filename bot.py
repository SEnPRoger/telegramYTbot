import telebot
from telebot import types
from telebot.types import Message
from requests.exceptions import ConnectionError
import config
from pytube import YouTube
from moviepy.editor import *

# =============================================================================
# Code for Video Converter to MP3 Telegram Bot from Youtube
#
# Version: 1.1 (Release)
# Date: 12.01.2022
# Author: SEnPRoger
#
# Contact: senproger@gmail.com
# (for feedback & suggestions)
#
# License: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# The bellow copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# Copyright (c) 2022 SEnPRoger
# =============================================================================

bot = telebot.TeleBot(config.TOKEN)

# strings for initializing important data for bot
mp4_file = ""
mp3_file = ""
audioTitle = ""
author = ""
url = ""

# function for dowloading video from YouTube
def downloadVideo(youtube):
    global mp4_file
    mp4_file = youtube.streams.get_highest_resolution().download()

# function for converting video from YouTube to mp3 file
def convertVideo(youtube):
    global mp3_file, mp4_file
    mp3_file = youtube.title + ".mp3"

    videoClip = VideoFileClip(mp4_file.title())
    audioClip = videoClip.audio

    audioClip.write_audiofile(mp3_file)
    audioClip.close()
    videoClip.close()

    os.remove(mp4_file)

# function for separating artist name from song name in video title  
def formatTitle(youtube):
    global audioTitle, author

    # check if video from "Topic" kind of channels on YT
    if "Topic" in youtube.author:
        split_string = youtube.author.split("- ", 1)
        author = split_string[0]
    else:
        author = youtube.author

    # check if authors name in name of video title
    if author in youtube.title:
        split_string = youtube.title.split("- ", 1)
        audioTitle = split_string[1]
        author = split_string[0]

        # check if video title have words, like: Lyric or Official
        if "Lyric" in audioTitle or "Official" in audioTitle or "Live" in audioTitle or "Video" in audioTitle:
            if "[" in audioTitle:
                split_string2 = audioTitle.split(" [", 2)
            if "(" in audioTitle:
                split_string2 = audioTitle.split(" (", 2)
            audioTitle = split_string2[0]
    else:
        audioTitle = youtube.title
        author = youtube.author

# handler for "/start" command
@bot.message_handler(commands = ['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello ✌️. Do you want to download a music or track, but it is only on Youtube?\n\n• Send me a link to a clip from Youtube and I will send you an audio track📬\n(Conversion takes approximately 1 minute)\n\n🧑‍💻Author: <a href='https://github.com/SEnPRoger'>SEnPRoger</a>", parse_mode='html')

# function for checking if typed text contains link
@bot.message_handler(content_types = ['text'])
def check_link(message):
    global mp3_file, audioTitle, author, url
    if "youtu" in message.text:
        url = message.text
        youtube = YouTube(url)  

        #creating additional button below message with video title
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="Convert to mp3🎵", callback_data="convert")
        keyboard.add(callback_button1)
        bot.send_message(message.chat.id, youtube.title + " 📽", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Something went wrong. Perhaps the entered text is not a link or the video is no longer available❌")

# observer for convert button below video title
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "convert":
            global mp3_file, audioTitle, author, url
            youtube = YouTube(url)

            # starting converting proccess
            bot.edit_message_text(chat_id=call.message.chat.id, text="Converting the video... (Preparing the video)⌛️", message_id=call.message.message_id)
            downloadVideo(youtube)
            bot.edit_message_text(chat_id=call.message.chat.id, text="Converting the video... 🟩⬜️⬜️\n(Extracting audio track) ⌛️", message_id=call.message.message_id)
            convertVideo(youtube)
            bot.edit_message_text(chat_id=call.message.chat.id, text="Converting the video... 🟩🟩⬜️\n(Formatting metadata) ⌛️", message_id=call.message.message_id)
            formatTitle(youtube)

            bot.edit_message_text(chat_id=call.message.chat.id, text="Converting the video... 🟩🟩🟩\n(A few seconds left) ⌛️", message_id=call.message.message_id)
            audio = open(mp3_file, 'rb')
            # trying to send audio file via Telegram
            try:
                bot.send_audio(call.message.chat.id, audio, performer=author, title=audioTitle, timeout=160)
                bot.edit_message_text(chat_id=call.message.chat.id, text="Converting the video... 3/3 (Done) ✅", message_id=call.message.message_id)
                audio.close()
                os.remove(mp3_file)
            # if we will detect some issues with Telegram or catch connection errors
            except ConnectionError:
                bot.edit_message_text(chat_id=call.message.chat.id, text="Converting the video... (Failed to send audio file) ❌", message_id=call.message.message_id)
                audio.close()
                os.remove(mp3_file)

bot.polling(none_stop = True)