from vosk import Model, KaldiRecognizer

LANGUAGE = 'ru'

# TODO Сделать выбор констант в зависимости от языка

# TODO Сделать выбор модели в зависимости от языка
MODEL_VOSK = Model("model")

WORD_FRIEND = 'друг'
WORD_SAY_COMMAND = ', скажи твою команду.'
WORD_USER_NAME = 'Люся'

WORD_PROGRAM_IS_RUNNING = 'Программа запущена'

WORD_PLAYLIST_NOT_FOUND = 'Плейлист не найден. Воспроизведение не возможно'
WORD_PLAYLIST_EXCEPTION = 'Плейлист не загружен. Неизвестная ошибка. Обратитесь к разработчику'
WORD_PLAYLIST_END = ', это последний трек в плейлисте'
WORD_PLAYLIST_START = ', это начало плейлиста.'
WORD_PLAYLIST_EMPTY = 'Плейлист пустой'

SET_PLAY = {'играй', 'играть', 'пой', 'петь'}
SET_SEARCH = {'найди', 'ищи', 'поиск', 'найти'}
SET_NEXT = {'следующий', 'следующие', 'следующее', 'следующая', 'следующую', 'следующей'}
SET_PREVIOUS = {'предыдущий', 'предыдущие', 'предыдущее', 'предыдущая', 'предыдущая', 'предыдущей'}
SET_FORWARD = {'вперед'}  # здесь будет указание количества треков или секунд/минут
SET_BACK = {'назад'}  # здесь будет указание количества треков или секунд/минут

SET_ALL_COMMANDS = SET_PLAY | SET_SEARCH | SET_NEXT | SET_PREVIOUS | SET_FORWARD | SET_BACK


WORD_NO_COMMAND =  ', я не услышал команду. Обратись опять к другу'
WORD_PLAYER_START = ', включаю плеер'
WORD_PLAYER_NEXT = ', перехожу к следующему треку '
WORD_PLAYER_PREVIOUS = ', перехожу к предыдущему треку '
WORD_PLAYER_FORWARD = ''', команда вперед. Пока эта команда не работает. 
                Но в будущем эта команда позволит переходить на несколько треков вперед и передвигаться внутри трека '''
WORD_PLAYER_BACK  = ''', команда назад. Пока эта команда не работает. 
                Но в будущем эта команда позволит переходить на несколько треков назад и передвигаться внутри трека '''
WORD_PLAYER_SEARCH = ', ищу '
WORD_EXCEPT =  ''', что-то пошло не так. Попробуй обратиться опять к другу. 
                            По возможности сообщи разработчику морской лисе об этой ситуации'''

# all_commands = {'play': set_play,
#                 'search': set_search,
#                 'next': set_next,
#                 'previous': set_previous,
#                 'forward': set_forward,
#                 'back': set_back}


