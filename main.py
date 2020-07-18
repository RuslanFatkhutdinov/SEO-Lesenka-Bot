import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


def phrase_to_list(phrase: str) -> list:
    """Конвертирует строку в список. Строка разбивается по запятой и
       знаку переноса строки. Слова приводятся к нижнему региструю.
       Удаляются пробелы в начале и конце строки.

    Args:
        phrase [str]: Фраза.

    Returns:
        clear_phrases_list [list]: Список с фразами.
    """
    phrases_list = phrase.replace('\n', ',').split(',')
    stripped_phrases_list = list(map(str.strip, phrases_list))
    lower_phrases_list = list(map(str.lower, stripped_phrases_list))
    clear_phrases_list = list(filter(None, lower_phrases_list))

    return clear_phrases_list


def phrase_multipler(phrase: str) -> list:
    """Функция для разномжения слов в фразе для парсинга в WS.

    Args:
        phrase [str]: Фраза.

    Returns:
        query_result [list]: Список размноженных фраз.
    """
    word_list = phrase.split(' ')
    len_word_list = len(word_list)
    max_words = 8
    query_result = []

    query_result.append(phrase)

    if len_word_list >= max_words:
        query_string = (
            f'Запрос больше {max_words} слов ({len_word_list}): {phrase}'
        )
        query_result.append(query_string)
    elif len_word_list >= 2:
        words_left = max_words - len_word_list
        for i in range(1, words_left):
            query_string = (
                '"' + word_list[0] + f' {word_list[0]}' * i +
                ' ' + ' '.join(word_list[1:]) + '"'
            )
            query_result.append(query_string)
    else:
        for i in range(1, max_words-1):
            query_string = '"' + word_list[0] + f' {word_list[0]}' * i + '"'
            query_result.append(query_string)

    return query_result


def multipler_result(phrase_list: list) -> dict:
    """Получение размноженных фраз из списка фраз.

    Args:
        phrase_list [list]: список пользовательских фраз.

    Returns:
        queries_dict [dict]: словарь с размноженными пользловательскими
        фразами.
    """
    queries_dict = {}
    for phrase in phrase_list:
        query = phrase_multipler(phrase)
        queries_dict[phrase] = query

    return queries_dict


def return_phrases(phrase_list: dict) -> print:
    """Вывод на печать размноженных пользовательских фраз.

    Args:
        phrase_list [dict]: словарь с размноженными пользловательскими
        фразами.
    """
    answer = []
    for keys, values in phrase_list.items():
        for element in values:
            clean_element = element.replace(' "', '"')
            answer.append(clean_element)
    return answer


def user_frase(update: Update, context: CallbackContext):
    users_query = update.message.text
    list_phrases = phrase_to_list(users_query)
    result_list = multipler_result(list_phrases)

    update.message.reply_text(
        text='\n'.join(return_phrases(result_list))
    )


def command_start_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=(
            'Это простой бот, который поможет составить "лесенку" '
            'из поисковой фразы.'
        )
    )


def main():
    updater = Updater(
        token=TELEGRAM_TOKEN,
        use_context=True,
    )

    updater.dispatcher.add_handler(
        CommandHandler(command='start', callback=command_start_handler)
    )
    updater.dispatcher.add_handler(
        MessageHandler(filters=Filters.text, callback=user_frase)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
