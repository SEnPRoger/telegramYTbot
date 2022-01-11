# Bot for converting video from YouTube into mp3 file
### 📋 Version: 1.1 (Release)
### 👨🏼‍💻 Author: SEnPRoger
### 🔗 GitHub: https://github.com/SEnPRoger
### 📬 Feedback and suggestions: senproger@gmail.com
## How to use
>Send command /start to bot for start conversation and get addtional information</br>After that, send a link to Youtube video and press button "Convert to mp3" bellow recieved message from bot</br>Wait a 1-2 minutes and get complete audio file for listening or downloading

## Packages
#### For using bot, these packages are need to be installed

```$ pip install moviepy```

```$ pip install pytube3```

```$ pip install requests```

```$ pip install pyTelegramBotAPI```

## Functions
#### Functions for converting video

| Function name | Input                    | Description                    |
| ------------- | ------------------------------ | ------------------------------ |
| downloadVideo()      | Copy of object of Youtube class.       | Function for dowloading video from YouTube. |
| convertVideo()      | Copy of object of Youtube class.       | Function for converting video from YouTube to mp3 file. |
| formatTitle()      |Copy of object of Youtube class.       | Function for separating artist name from song name in video title. |

### 📜 Note
>You need to have permission to upload files to your server!

#### Functions for send messages from bot
| Function name | Description                    |
| ------------- | ------------------------------ |
| start_message()      | Handler for "/start" command.       |
| check_link()      | Function for checking if typed text contains link.       |
| callback_inline()      | Function for convert button below video title.       |

### 💡 Tip
>If you have troubles with sending audio via Telegram, ``timeout`` value can be changed

## ⚙️ Customizing
#### Function ``formatTitle()``:
  ```
  #check if video title have words, like: Lyric or Official
        if "Lyric" in audioTitle or "Official" in audioTitle or "Live" in audioTitle or "Video" in audioTitle:
            if "[" in audioTitle:
                split_string2 = audioTitle.split(" [", 2)
            if "(" in audioTitle:
                split_string2 = audioTitle.split(" (", 2)
            audioTitle = split_string2[0]
  ```
#### In function ``formatTitle()`` you can add your own words in video title filter, whose will be deleted, like:
> - Video
> - Lyric
> - Official
> - Visualizer