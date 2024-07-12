""" Setting up the program. (en)

This area is user-configurable.
Here you need to select the language in which the program will work (currently only Russian and English).
For Russian: LANGUAGE = 'ru'
For English: LANGUAGE = 'en'
The default language is Russian

Enter the name of the user who will work with the program.
USER_NAME = 'Lucy'
The default username is Lucy.

Настройка программы. (ru)

Эта область настраивается пользователем.
Здесь надо выбрать язык на котором будет работать программа (в настоящий момент только русский и английский).
Для русского: LANGUAGE = 'ru'
Для английского: LANGUAGE = 'en'
По умолчанию установлен русский язык

Ввести имя пользователя который будет работать с программой.
USER_NAME = 'Люся'
По умолчанию имя пользователя Люся
"""

# LANGUAGE = 'ru'
LANGUAGE = 'en'
# USER_NAME = 'Люся'
USER_NAME = 'Lucy'

""" Settings area for advanced users (en)

You can add another language here if you add another elif block LANGUAGE == 'new language' 
and specify it in the line LANGUAGE = ''

Область настроек для опытных пользователей (ru) 

Здесь можно добавить еще один язык, если добавить еще один блок elif LANGUAGE == 'new language'
и указать его в строке LANGUAGE = ''"""

from vosk import Model

if LANGUAGE == 'en':
    MODEL_VOSK = Model("vosk_model_small_en")

    # FRIEND = 'friend'
    FRIEND = 'hello'
    SAY_COMMAND = ', tell me your command.'

    PROGRAM_IS_RUNNING = 'The program is running'

    PLAYLIST_NOT_FOUND = 'The playlist is not found. Playback is not possible'
    PLAYLIST_EXCEPTION = 'The playlist is not loaded. Unknown error. Contact the developer'
    PLAYLIST_END = ', this is the last track in the playlist'
    PLAYLIST_START = ', this is the beginning of the playlist.'
    PLAYLIST_EMPTY = 'The playlist is empty'

    SET_PLAY = {'play', 'sing'}
    SET_SEARCH = { 'search', 'find'}
    SET_NEXT = {'next'}
    SET_PREVIOUS = { 'previous'}
    SET_FORWARD = {'forward'}  # here you will specify the number of tracks or seconds/minutes
    SET_BACK = {'back'}  # here you will specify the number of tracks or seconds/minutes

    SET_ALL_COMMANDS = SET_PLAY | SET_SEARCH | SET_NEXT | SET_PREVIOUS | SET_FORWARD | SET_BACK

    NO_COMMAND = ''', I haven't heard your command. Call for friend again.'''
    PLAYER_START = 'The player is starting'
    PLAYER_NEXT = ''', I'm moving on to the next track.'''
    PLAYER_PREVIOUS = ''', I'm moving on to the previous track.'''
    PLAYER_FORWARD = ''', This is a command forwards. 
                    This command is not working yet.
                    But in the future, this command will allow you to move forward several tracks 
                    and move inside the track '''
    PLAYER_BACK = ''', , This is a command back. 
                    This command is not working yet.
                    But in the future, this command will allow you to move back several tracks 
                    and move inside the track  '''
    PLAYER_SEARCH = ', SEARCH '
    EXCEPT = ''', Something went wrong. Try call for friend again.. 
                                    If possible, inform the developer RedSeaFox about this situation'''

elif LANGUAGE == 'ru':
    MODEL_VOSK = Model("vosk_model_small_ru")

    FRIEND = 'друг'
    SAY_COMMAND = ', скажи твою команду.'

    PROGRAM_IS_RUNNING = 'Программа запущена'

    PLAYLIST_NOT_FOUND = 'Плейлист не найден. Воспроизведение не возможно'
    PLAYLIST_EXCEPTION = 'Плейлист не загружен. Неизвестная ошибка. Обратитесь к разработчику'
    PLAYLIST_END = ', это последний трек в плейлисте'
    PLAYLIST_START = ', это начало плейлиста.'
    PLAYLIST_EMPTY = 'Плейлист пустой'

    SET_PLAY = {'играй', 'играть', 'пой', 'петь'}
    SET_SEARCH = {'найди', 'ищи', 'поиск', 'найти'}
    SET_NEXT = {'следующий', 'следующие', 'следующее', 'следующая', 'следующую', 'следующей'}
    SET_PREVIOUS = {'предыдущий', 'предыдущие', 'предыдущее', 'предыдущая', 'предыдущая', 'предыдущей'}
    SET_FORWARD = {'вперед', 'вперёд'}  # здесь будет указание количества треков или секунд/минут
    SET_BACK = {'назад'}  # здесь будет указание количества треков или секунд/минут

    SET_ALL_COMMANDS = SET_PLAY | SET_SEARCH | SET_NEXT | SET_PREVIOUS | SET_FORWARD | SET_BACK

    NO_COMMAND =  ', я не услышал команду. Обратись опять к другу'
    PLAYER_START = ', включаю плеер'
    PLAYER_NEXT = ', перехожу к следующему треку '
    PLAYER_PREVIOUS = ', перехожу к предыдущему треку '
    PLAYER_FORWARD = ''', команда вперед. Пока эта команда не работает. 
                    Но в будущем эта команда позволит переходить на несколько треков вперед и передвигаться внутри трека '''
    PLAYER_BACK  = ''', команда назад. Пока эта команда не работает. 
                    Но в будущем эта команда позволит переходить на несколько треков назад и передвигаться внутри трека '''
    PLAYER_SEARCH = ', ищу '
    EXCEPT =  ''', что-то пошло не так. Попробуй обратиться опять к другу. 
                                По возможности сообщи разработчику морской лисе об этой ситуации'''


START_OF_LIST = 'start_of_list_' + LANGUAGE + '.mp3'
END_OF_LIST = 'end_of_list_' + LANGUAGE + '.mp3'