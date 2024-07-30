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

LANGUAGE = 'ru'
USER_NAME = 'Люся'
# LANGUAGE = 'en'
# USER_NAME = 'Lucy'

""" Settings area for advanced users (en)

You can add another language here if you add another elif block LANGUAGE == 'new language' 
and specify it in the line LANGUAGE = ''

You can also change the words used to invoke commands here.

Область настроек для опытных пользователей (ru) 

Здесь можно добавить еще один язык, если добавить еще один блок elif LANGUAGE == 'new language'
и указать его в строке LANGUAGE = ''

Так же здесь можно изменить слова, которыми вызываются команды.
"""

from vosk import Model

if LANGUAGE == 'en':
    MODEL_VOSK = Model("vosk_model_small_en")

    # The word is a beacon. The program uses it to determine that the user is accessing the program.
    FRIEND = 'friend'

    # Launch the player
    SET_PLAY = {'play', 'sing'}

    # Go to the next track
    SET_NEXT = {'next'}
    # Go to the previous track
    SET_PREVIOUS = { 'previous'}

    # Go to:
    #  or to the track with the specified number in the playlist
    #  ot to a specific time in the track
    SET_GOTO = {'go', 'move', 'number'}

    # Fast-forward:
    # or through several tracks
    # or to a specific time in the track
    SET_FORWARD = {'forward'}
    SET_BACK = {'back'}

    # For the SET_GET, SET_FORWARD and SET_BACK commands,
    # it specifies exactly how to move along tracks or in time.
    SET_MEASURE_TRACK = {'track', 'tracks', 'song', 'songs'}
    SET_MEASURE_SECOND = {'second', 'seconds'}
    SET_MEASURE_MINUTE = {'minute', 'minutes'}
    SET_MEASURE_HOUR = {'hour', 'hours'}

    SET_BYE = {'bye', 'goodbye', 'adieu'}
    SET_SEARCH = { 'search', 'find'}

    SET_ALL_COMMANDS = SET_PLAY | SET_SEARCH | SET_NEXT | SET_PREVIOUS | SET_FORWARD | SET_BACK | SET_BYE | SET_GOTO
    SET_MEASURE_TIME = SET_MEASURE_SECOND | SET_MEASURE_MINUTE | SET_MEASURE_HOUR

    SAY_COMMAND = ', tell me your command.'
    PROGRAM_IS_RUNNING = 'The program is running'
    PLAYLIST_NOT_FOUND = 'The playlist is not found. Playback is not possible'
    PLAYLIST_EXCEPTION = 'The playlist is not loaded. Unknown error. Contact the developer'
    PLAYLIST_END = ', this is the last track in the playlist'
    PLAYLIST_START = ', this is the beginning of the playlist.'
    PLAYLIST_EMPTY = 'The playlist is empty'
    NO_COMMAND = ''', I haven't heard your command. Call for friend again.'''
    NO_NUMBER = ''', I haven't heard the number. Call for friend again.'''
    PLAYER_START = 'The player is starting'

    PLAYER_NEXT = ''', I'm going on to the next track.'''
    PLAYER_PREVIOUS = ''', I'm going  on to the previous track.'''

    PLAYER_FORWARD = ''', Fast forward '''
    PLAYER_BACK = ''',  Fast backward '''

    GOTO = ', go to track number '
    GOTO_TRACK = ',go to track number '
    MEASURE_UNDEFINED = ''', I didn't hear how to move. For a second, a minute, or a track?
                                Call for friend again.'''
    TIME_TRACK = ''', track duration '''

    END_OF_TRAC = ', end of the track'

    LIMIT_MAX_JUMP = ''', It takes a long time to go through several tracks,
            therefore, the number of tracks when jumping through several tracks is limited to 20.
            If you need to switch to more tracks, use the transition to a specific track by its number in the playlist.
            To do this, use the commands:    ''' + ', '.join(SET_GOTO)

    MAX_JUMP = 20

    PLAYER_SEARCH = ', the search command is not working yet '
    EXCEPT = ''', Something went wrong. Try call for friend again.. 
                                    If possible, inform the developer RedSeaFox about this situation'''
    BYE = '''Closing the program'''

    All_NAME_NUMBER = {
        'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
        'ten', 'eleven', 'twelve', 'thirteen','fourteen', 'fifteen',
        'sixteen', 'seventeen', 'eighteen', 'nineteen',
        'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety',
        'hundred', 'thousand'
    }

    NAME_THOUSAND = {'thousand'}
    NAME_HUNDRED = {'hundred'}

    NAME_NUMBER_DICT = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'eleven': 11,
        'twelve': 12,
        'thirteen': 13,
        'fourteen': 14,
        'fifteen': 15,
        'sixteen': 16,
        'seventeen': 17,
        'eighteen': 18,
        'nineteen': 19,
        'twenty': 20,
        'thirty': 30,
        'forty': 40,
        'fifty': 50,
        'sixty': 60,
        'seventy': 70,
        'eighty': 80,
        'ninety': 90,
        'hundred': 100,
        'thousand': 1000
    }

    MAX_NUMBER = 19999
    MESSAGE_MAX_NUMBER = ', I can only work with numbers no more than 20,000'

elif LANGUAGE == 'ru':
    MODEL_VOSK = Model("vosk_model_small_ru")

    # Слово - маячок. По нему программа определяет, что обратились к ней.
    FRIEND = 'друг'

    # Запустить плеер
    SET_PLAY = {'играй', 'играть', 'пой', 'петь'}

    # Перейти к следующему треку
    SET_NEXT = {'следующий', 'следующие', 'следующее', 'следующая', 'следующую', 'следующей'}
    # Перейти к предыдущему треку
    SET_PREVIOUS = {'предыдущий', 'предыдущие', 'предыдущее', 'предыдущая', 'предыдущая', 'предыдущей'}

    # Прейти:
    # или к треку с указанным номером в плейлисте
    # или к конкретному времени в треке
    SET_GOTO= {'иди', 'перейди', 'включи'}

    # Прыжок (быстрая перемотка):
    # или через несколько треков
    # или через несколько секунд/минут/часов
    SET_FORWARD = {'вперед', 'вперёд'}
    SET_BACK = {'назад'}

    # Для команд SET_GOTO, SET_FORWARD и SET_BACK указывает как именно надо двигаться
    # по трекам или во времени.
    SET_MEASURE_TRACK = {'трек', 'трека', 'треку', 'треков',
                         'песня', 'песни', 'песен', 'песню'}
    SET_MEASURE_SECOND = {'секунда', 'секунды', 'секунд', 'секунду'}
    SET_MEASURE_MINUTE = {'минута', 'минуты', 'минут', 'минуту'}
    SET_MEASURE_HOUR = {'час', 'часа', 'часов'}

    SET_BYE = {'пока', 'до свидания', 'прощай'}
    SET_SEARCH = {'найди', 'ищи', 'поиск', 'найти'}

    SET_ALL_COMMANDS = SET_PLAY | SET_SEARCH | SET_NEXT | SET_PREVIOUS | SET_FORWARD | SET_BACK | SET_BYE | SET_GOTO
    SET_MEASURE_TIME = SET_MEASURE_SECOND | SET_MEASURE_MINUTE | SET_MEASURE_HOUR

    SAY_COMMAND = ', скажи твою команду.'
    PROGRAM_IS_RUNNING = 'Программа запущена'
    PLAYLIST_NOT_FOUND = 'Плейлист не найден. Воспроизведение не возможно'
    PLAYLIST_EXCEPTION = 'Плейлист не загружен. Неизвестная ошибка. Обратитесь к разработчику'
    PLAYLIST_END = ', это последний трек в плейлисте'
    PLAYLIST_START = ', это начало плейлиста.'
    PLAYLIST_EMPTY = 'Плейлист пустой'
    NO_COMMAND =  ', я не услышал команду. Обратись опять к другу'
    NO_NUMBER = ', я не услышал число. Обратись опять к другу'
    PLAYER_START = ', включаю плеер'

    PLAYER_NEXT = ', перехожу к следующему треку '
    PLAYER_PREVIOUS = ', перехожу к предыдущему треку '

    PLAYER_FORWARD = '''Быстрая перемотка вперед '''
    PLAYER_BACK = '''Быстрая перемотка назад '''

    GOTO = ', перехожу '
    GOTO_TRACK = ', перехожу к треку номер '
    MEASURE_UNDEFINED = ''', я не услышал как двигаться. На секунду, минуту или трек?
                            Обратись опять к другу'''
    TIME_TRACK = ''', продолжительность трека '''

    END_OF_TRAC = ', конец трека'

    LIMIT_MAX_JUMP = ''', переход через несколько треков занимает много времени,
        поэтому количество треков при прыжке через несколько треков ограничено 20.
        Если надо перейти на большее количество треков, воспользуйся переходом к конкретному треку по его номеру в плейлисте.
        Для этого используй команды:    ''' + ', '.join(SET_GOTO)

    MAX_JUMP = 20

    PLAYER_SEARCH = ', команда поиска пока не работает '
    EXCEPT = ''', что-то пошло не так. Попробуй обратиться опять к другу. 
                                По возможности сообщи разработчику морской лисе об этой ситуации'''
    BYE = '''Закрываю программу'''

    All_NAME_NUMBER = {
        'один', 'одна', 'одну', 'одно','первой', 'первую', 'два', 'две','второй', 'вторую',
        'три', 'третий','третьему', 'третья',  'третьей', 'третью', 'четыре', 'пять',
        'шесть', 'семь', 'восемь', 'девять', 'десять', 'одиннадцать', 'двенадцать',
        'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать', 'семнадцать',
        'восемнадцать', 'девятнадцать', 'двадцать', 'тридцать', 'сорок',
        'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто',
        'сто', 'сотня', 'сотни', 'сотен','двести', 'триста', 'четыреста', 'пятьсот', 'шестьсот',
        'семьсот', 'восемьсот', 'девятьсот', 'тысяча', 'тысячу', 'тысячи', 'тысяч'
    }

    NAME_THOUSAND = {'тысяча', 'тысячу', 'тысячи', 'тысяч'}
    NAME_HUNDRED = {'сотня', 'сотни', 'сотен'}

    NAME_NUMBER_DICT = {
        'один': 1, 'одна': 1, 'одну': 1, 'одно': 1, 'первой': 1, 'первую': 1,
        'два': 2, 'две': 2, 'второй': 2, 'вторую': 2,
        'три': 3,'третий': 3,'третьему': 3, 'третья': 3,  'третьей': 3, 'третью': 3,
        # todo просклонять остальные цифры
        'четыре': 4,
        'пять': 5,
        'шесть': 6,
        'семь': 7,
        'восемь': 8,
        'девять': 9,
        'десять': 10,
        'одиннадцать': 11,
        'двенадцать': 12,
        'тринадцать': 13,
        'четырнадцать': 14,
        'пятнадцать': 15,
        'шестнадцать': 16,
        'семнадцать': 17,
        'восемнадцать': 18,
        'девятнадцать': 19,
        'двадцать': 20,
        'тридцать': 30,
        'сорок': 40,
        'пятьдесят': 50,
        'шестьдесят': 60,
        'семьдесят': 70,
        'восемьдесят': 80,
        'девяносто': 90,
        'сто': 100, 'сотня': 100, 'сотни': 100, 'сотен': 100,
        'двести': 200,
        'триста': 300,
        'четыреста': 400,
        'пятьсот': 500,
        'шестьсот': 600,
        'семьсот': 700,
        'восемьсот': 800,
        'девятьсот': 900,
        'тысяча': 1000, 'тысячу': 1000, 'тысячи': 1000, 'тысяч': 1000
    }

    MAX_NUMBER = 19999
    MESSAGE_MAX_NUMBER = ', я могу работать только с числами не больше 20000'

START_OF_LIST = 'start_of_list_' + LANGUAGE + '.mp3'
END_OF_LIST = 'end_of_list_' + LANGUAGE + '.mp3'

def number_greater_len_pl(number, len_playlist,):
    if LANGUAGE == 'en':
        return f'''You  have said a number {number}.  
        But there are {len_playlist} tracks in your playlist right now. 
            To go to a specific track, call a number from one to {len_playlist}'''

    elif LANGUAGE == 'ru':
        return f''', ты назвала цифру {number}.  
        Но в твоем плейлисте сейчас {len_playlist} треков. 
            Для перехода к конкретному треку назови число от одного до {len_playlist}
            '''
    else:
        return ''