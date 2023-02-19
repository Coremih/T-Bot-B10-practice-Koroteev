import telebot
from config import keys, TOKEN
from extensions import Converter, APIException, GetNoun
from telebot import types


bot = telebot.TeleBot(TOKEN)


def create_markup(base=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for i in keys.keys():
        if i != base:
            buttons.append(types.KeyboardButton(i.capitalize()))
    markup.add(*buttons)
    return markup


def get_decl(a, b, q):
    base_t = f"{GetNoun.get_noun(float(a.replace(',', '.')), keys[b][1], keys[b][2])} ({keys[b][0]})"
    quote_t = f"{keys[q][3]} ({keys[q][0]})"
    return base_t, quote_t


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    user_name = message.from_user.full_name
    text = f"Привет, {user_name}!\n \
\nВведите запрос в следующем формате: \
\n<имя валюты> <в какую валюту перевести> <количество>, \
\nнапример:  доллар рубль 100 \
\nСписок доступных валют:  /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:\n"
    for key in keys:
        text = '\n-  <b>'.join((text, key)) + '</b>\n   <i>' + keys[key][0] + '  |  ' + keys[key][4] + '</i>'
    bot.send_message(message.chat.id, text, parse_mode='html')




@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    vals = message.text.lower().split()
    try:
        if len(vals) != 3:
            raise APIException("Количество параметров должно быть равно 3")
        b, q, a = map(str.lower, vals)
        total_base = Converter.get_price(*vals)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка ввода запроса...\n{e}")
    else:
        text = f"Цена {a} {get_decl(a, b, q)[0]} в {get_decl(a, b, q)[1]} = {round(total_base, 4)}"
        bot.send_message(message.chat.id, text)


bot.polling()
