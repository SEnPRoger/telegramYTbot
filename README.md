# Bot for converting video from YouTube into mp3 file
### 📋 Version: 1.2 (Release)
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
### Here some ideas for customization your bot:
- ### 💬 Adding your own words in title video filter
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
- ### 🌐 Adding option for choosing language
  First of all, you need to add JSON module at head of code ```import json``` for reading file with translated strings and add this code:</br></br>
  ```
  f = open ('dictionary.json', "r", encoding="utf8")
  data = json.loads(f.read())
  ```
  Variable ```data``` will be used for getting string by language and phrase key. </br></br> After that, you need to allow user choose prefer language. For that we will create a observer for new ```/lang``` command:</br></br>
  ```
  @bot.message_handler(commands = ['lang'])
  def change_language(message):
      keyboard = types.InlineKeyboardMarkup()
      
      changeLangEN_button = types.InlineKeyboardButton(text="EN", callback_data="chooseLang_EN")
      changeLangRU_button = types.InlineKeyboardButton(text="FR", callback_data="chooseLang_FR")  
      
      keyboard.add(changeLangEN_button, changeLangRU_button)
      
      bot.send_message(message.chat.id, str(data["en"][0]["chooseLang_text"]), reply_markup="keyboard")
  ```
  Here we are added new two button below asking message from bot: ```changeLangEN_button``` and ```changeLangFR_button```. Of course, you can add more buttons with other languages.</br></br>Now we have to create a function for selecting language. Create a new variable ```lang``` at head of code for storage prefered language and import it in ```@bot.callback_query_handler``` by adding this line ```global lang```. Part of the already done code here should look like this:</br></br>
  ```
  global lang

    if call.data == "chooseLang_EN":
      lang = "en"

    if call.data == "chooseLang_RU":
      lang = "fr"
  ```
  Almost done - finally we can replace all strings at part, where bot send messages to user in ```str(data["lang"][0]["key_from_json_file"])```. And do not forget to import variable ```lang``` by adding this line ```global lang``` in every function, where we send message to user.
  ### ❗️ Important
  > Variable ```lang``` must be same as your key for identifying language in ```dictionary.json```