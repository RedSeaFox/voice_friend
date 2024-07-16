# Voice helper friend
## en
### About the program
The program is designed for situations where there is no possibility or desire to control a computer with a mouse or keyboard.

Management refers to the most common actions of an ordinary user. 
The main purpose of the program is listening or watching media. 

It is also planned to add:
1. Compilation of text files (to-do list, reminders, some information that needs to be recorded)
2. Start the timer 
3. Getting time information
4. Getting weather information.

To determine that the program is being accessed, there is a special word in the program-a beacon. It is declared in the module `voicehelper_friend_config.py`. For example, it can be the word *"friend"*:
``` python
 FRIEND = 'friend'
```

Russian is set by default in the program and, accordingly, the word-beacon is used by default in Russian (*"друг"*) and the username is also indicated in Russian (*"Люся"*). How to set the program up to work with English and other languages, see below

Management is carried out according to two scenarios.

**The first scenario**: the program constantly listens to incoming words in portions of 2 seconds.  If the program detects an appeal to it in words (a beacon word), then it selects all the words that entered the interval of 2 seconds along with the beacon word and tries to find the correspondence of these words to the commands that it can execute. If such a match is found, the program executes a command from the match. If such a match is not found, the program proceeds to the second scenario.
That is, the main purpose of the first scenario is to catch an appeal to a "friend" (the word is a beacon) and, if possible, execute the command. Therefore, the response in the first scenario is fast.

In the **second scenario** listening continues until the pause between words is more than 2-4 seconds or the message length is more than 100 characters. Next, the program also look for the correspondence of the words from the expression to the commands that the program can execute.
That is, in the second scenario, the program has already realized that it has been contacted and that the command may be quite long and that the user may not say this command very quickly. Therefore, the reaction in the second scenario is not very fast.

In the first release, you can launch the player and move back and forth through the playlist tracks. 
At this stage, a single playlist named `my_playlist.m3u` is used, which is currently compiled in advance by "hands" (using the keyboard and mouse). You can create a playlist in the VLC media player program. The playlist looks something like this:
```
#EXTM3U
#EXTINF:2,Kipling_If.mp3
file:///F:/MyMusic/Kipling_If.mp3
#EXTINF:5,Romeo_and_Juliet.mp3
file:///F:/MyMusic/Romeo_and_Juliet.mp3
#EXTINF:5,Waltz.mp3
file:///F:/MyMusic/Waltz.mp3
#EXTINF:10,Bella_ciao.mp3
file:///F:/MyMusic/Bella_ciao.mp3
```

In the near future, it is planned to add moving several tracks back and forth, moving to a specific track, moving within tracks at a given interval.

Since the user can express the same command in different words and since the recognition module does not always accurately recognize the endings of words, the program sets different call options for some commands.
For example, the following words can be used to launch the player: *play, sing*. It is written in the module `voicehelper_friend_config.py `:
```python
SET_PLAY = {'play', 'play', 'sing', 'sing'}
```

At this stage, the program runs under Windows. Tested on Windows 10. 
The program code contains outputs (print) for debugging. Some of them are commented out, but if desired, they can be commented out.

### Technology stack
The program is developed in Python 3.11  

The list of all modules and packages required for the correct operation of the program is contained in the file `requirements.txt `.


The offline library [vosk](https://alphacephei.com/vosk/) is used for speech recognition  and its [models](https://alphacephei.com/vosk/models):  *vosk-model-small-en-us-0.15* and *vosk-model-small-ru-0.22*.  
In the first release, the program works with Russian and English. You can add your own language.
To do this, you need to:
1. Download the lightweight language model  [from here](https://alphacephei.com/vosk/models ) and unpack it into the program folder
2. in the module `voicehelper_friend_config.py ` specify the language and add the `elif` block in which to fill in the constants.


### Installation Instructions
Python 3.11 must be installed. Perhaps the program will work on other versions of Python 3. 

Download and place files in a separate folder `voicehelper_friend.py ` and `voicehelper_friend_config.py `. 

Download lightweight libraries **vosk** `vosk-model-small-en-us-0.*` for management in English and `vosk-model-small-ru-0.*` for management in Russian. The program was tested with the libraries `vosk-model-small-en-us-0.15` and `vosk-model-small-ru-0.22`. But the program should also work with other versions of lightweight  libraries. Libraries can be taken from this repository from folder [VoiceHelper](https://github.com/RedSeaFox/voice_friend/tree/master/VoiceHelper) or from the developer's website https://alphacephei.com/vosk/models . Libraries should also be placed in the program folder.

Set up a virtual environment. Take the dependencies from the file `requirements.txt `.

That is, the folder structure should be something like this:  
![file_structure](/image/file_structure.jpg)


In "VLC media player" create a playlist named `my_playlist.m3u`.  
The playlist must contain the full path to the media files, indicating the disk and folders.  
Example: `file:///F:/MyMusic/Romeo_and_Juliet.mp3`. 

For the Russian language in the module `voicehelper_friend_config.py ` specify the name of the user who will communicate with the program. The default name is Люся:  
```python
LANGUAGE = 'ru'
USER_NAME = 'Люся'
```
For English in the module `voicehelper_friend_config.py ` specify the language `en" and the name of the user who will communicate with the program. For example, the name Lucy:  
```python
LANGUAGE = 'en'
USER_NAME = 'Lucy'
``` 

### Instructions for use
The program is started by the file ``voicehelper_friend.py ``. 
The program settings are located in the module `voicehelper_friend_config.py `.  

Before starting the program in the module ``voicehelper_friend_config.py `` you need to select a language and enter a username. **By default, the language is Russian, and the username is Люся**.

In the first release, the team is able to play media files from a playlist named ``my_playlist.m3u`` and move on to the next or previous track.  
You can **start a playlist** with one of the words: *play, sing*.  
**Go to the next track**: *next*.  
**Go to the previous track**: *previous*

### An example of how the program works ###

There is a playlist file named *my_playlist.m3u* in the program folder.  
Run the program (run the file `voicehelper_friend.py` ). At startup, the program informs you that the program is running.  
If we want to start playing a playlist, we say: *"friend, play"*.
If the phrase is fully recognized, the player starts.  
If only the word *"friend"* is recognized, then the program asks you to tell her a command. We can pronounce one or more words from the list *SET_PLAY = {'play', 'play', 'sing', 'sing'}*. For example, we can say *"play, sing"*. Then the player will start.  
If the program hears the word *"friend"* during playback, the player is paused and the program asks you to say a command.  
If during playback the program hears *"friend"* and some other command that it knows how to execute, then the program executes this command.

## ru
### О программе
Программа для ситуаций, когда нет возможности или желания управлять компьютером при помощи мышки или клавиатуры.

Под управлением подразумеваются  самые обычные действия обычного пользователя. 
Основное назначение программы - прослушивание или просмотр медиа. 

Также планируется добавить:
1. составление текстовых файлов (список дел, напоминания, какая-то информация, которую надо зафиксировать)
2. запуск таймера 
3. получение информации о времени
4. получение информации о погоде.

Чтобы определить, что обращаются к программе, в программе есть специальное слово маячок. Объявляется оно в модуле `voicehelper_friend_config.py` и по умолчанию это слово *"друг"* :
``` python
FRIEND = 'друг'
```


Управление осуществляется по двум сценариям.

**Первый сценарий**: программа постоянно прослушивает входящие слова порциями по 2 секунды.  Если программа обнаруживает в словах обращение к ней (слово-маячок), то она отбирает все слова которые вошли в интервал 2 секунд вместе со словом маячком и пытается найти соответствие этих слов командам, которые она умеет выполнять. Если такое соответствие найдено, то программа выполняет команду из соответствия. Если же такое соответствие не найдено, то программа переходит ко второму сценарию.
То есть основная цель первого сценария уловить обращение к «другу» (слово-маячок) и по возможности выполнить команду. Поэтому отклик по первому сценарию быстрый.

Во **втором сценарии** прослушивание идет до тех пор пока пауза между словами не станет больше 2-4 секунд или длина сообщения не станет больше 100 символов. Далее также ищется соответствие слов из выражения командам, которые программа умеет выполнять.
То есть во втором сценарии программа уже поняла, что к ней обратились и что возможно команда будет достаточно длинная и что пользователь может говорить эту команду не очень быстро. Поэтому реакция по второму сценарию не очень быстрая.

В первом релизе доступен запуск плеера,  и перемещение по трекам плейлиста вперед и назад. 
На данном этапе используется единственный плейлист с именем `my_playlist.m3u`, который пока составляется заранее "руками" ( с помощью клавиатуры и мышки). Плейлист можно составить в программе "VLC media player". Выглядит плейлист примерно так:
```
#EXTM3U
#EXTINF:2,Kipling_If.mp3
file:///F:/MyMusic/Kipling_If.mp3
#EXTINF:5,Romeo_and_Juliet.mp3
file:///F:/MyMusic/Romeo_and_Juliet.mp3
#EXTINF:5,Waltz.mp3
file:///F:/MyMusic/Waltz.mp3
#EXTINF:10,Bella_ciao.mp3
file:///F:/MyMusic/Bella_ciao.mp3
```

В ближайшее время планируется добавить перемещение на несколько треков вперед-назад, перемещение к конкретному треку, перемещение внутри треков на заданный интервал.

Так как одну и ту же команду пользователь может выразить разными словами и так как модуль распознавания не всегда точно распознает окончания слов, в программе для некоторых команд задаются различные варианты вызова.
Так например для запуска плеера могут использоваться такие слова: *играй, играть, пой, петь*. Это прописано в модуле `voicehelper_friend_config.py`:
``` 
SET_PLAY = {'играй', 'играть', 'пой', 'петь'}
```

На данном этапе программа работает под Windows. Тестировалась на Windows 10. 
В коде программы вставлены выводы (print) для отладки. Часть из них закомментирована, но при желании, их можно раскомментировать.

### Стек технологий
Программа разработана на Python 3.11  

Перечень всех модулей и пакетов, необходимых для корректной работы программы содержаться в файле `requirements.txt`.


Для распознавания речи используется оффлайн-библиотека [vosk](https://alphacephei.com/vosk/) и ее малые (Lightweight) [модели](https://alphacephei.com/vosk/models ): *vosk-model-small-en-us-0.15* и *vosk-model-small-ru-0.22*.  
В первом релизе программа работает с русским и английским языком. Вы можете добавить свой язык.
Для этого надо:
1. скачать малую языковую модель (Lightweight)  [отсюда](https://alphacephei.com/vosk/models) и распаковать ее в папку с программой
2. в модуле `voicehelper_friend_config.py` указать язык и добавить блок `elif`, в котором заполнить константы.


### Инструкция по установке
Должен быть установлен Python 3.11. Возможно прграмма будет работать и на других версиях Python 3. 

Скачать с репозитория из папки [VoiceHelper](https://github.com/RedSeaFox/voice_friend/tree/master/VoiceHelper) и поместить в отдельную папку файлы `voicehelper_friend.py` и `voicehelper_friend_config.py`. 

Скачать малые (Lightweight) библиотеки **vosk** `vosk-model-small-en-us-0.*` для управления на английском языке и `vosk-model-small-ru-0.*` для управления на русском языке. Программа тестировалась с библиотеками `vosk-model-small-en-us-0.15` и `vosk-model-small-ru-0.22`. Но с другими версиями малых библиотек программа также должна работать. Библиотеки можно взять с этого репозитория из папки [VoiceHelper](https://github.com/RedSeaFox/voice_friend/tree/master/VoiceHelper) или с сайта разработчика https://alphacephei.com/vosk/models. Библиотеки надо поместить в папку с программой.

Настроить виртуальное окружение. Зависимости взять из файла `requirements.txt`.

То есть структара папки должна быть примерно такая:  
![file_structure](/image/file_structure.jpg)


В "VLC media player" создать плейлист с именем `my_playlist.m3u`.  
В плейлисте должен быть прописан полный путь к медиафайлам, с указанием диска и папок.  
Пример: `file:///F:/MyMusic/Romeo_and_Juliet.mp3`. 

Для русского языка в модуле `voicehelper_friend_config.py` указать имя пользователя, который будет общаться с программой. По умолчанию имя Люся:  
```python
LANGUAGE = 'ru'
USER_NAME = 'Люся'
```
Для английского языка в модуле `voicehelper_friend_config.py` указать язык `'en'` и имя пользователя, который будет общаться с программой. Например, имя Lucy:  
```python
LANGUAGE = 'en'
USER_NAME = 'Lucy'
``` 

### Инструкция по использованию
Программа запускается файлом ```voicehelper_friend.py```. 
Настройки программы находятся в модуле `voicehelper_friend_config.py`.  

Перед запуском программы в модуле ```voicehelper_friend_config.py``` необходимо выбрать язык и ввести имя пользователя. **По умолчанию язык – русский, а имя пользователя Люся**.

В первом релизе команда умеет воспроизводить медиа-файлы из плейлиста с именем ```my_playlist.m3u``` и переходить к следующему или предыдущему треку.  
**Запустить плейлист** можно одним из слов:  *играй, играть, пой, петь*.  
**Перейти к следующему треку**: *следующий*.  
**Перейти к предыдущему треку**: *предыдущий*

### Пример работы программы ###

В папке с программой есть файл плейлиста с именем my_playlist.m3u.  
Запускаем программу (запускаем файл voicehelper_friend.py). При запуске программа сообщает, что программа запущена.  
Если хотим запустить воспроизведение плейлиста, то говорим: "друг играй".
Если фраза распознана полностью, то запускается плеер.  
Если распознано только слово "друг", то программа просит сказать ей команду. Можем произнести одно или несколько слов из списка  *SET_PLAY = {'играй', 'играть', 'пой', 'петь'}*. Например, можем сказать *"пой, играй, пой"*. Тогда запуститься плеер.  
Если во время воспроизведения программа услышит слово "друг", то плеер ставится на паузу и программа просит произнести команду.  
Если во время воспроизведения программа услышит "друг" и еще какую-то команду, которую она умеет выполнять, то программы выполнит эту команду.



