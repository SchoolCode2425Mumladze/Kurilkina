import random
import telebot
from keys import alphabet, letter_map, bukvs_numb
from os import environ

bot = telebot.TeleBot(environ['TG_TOKEN'])
timer = 0
last_bot = ''
def FindNumbersOfBukvs():
    last_bot_num = bukvs_numb.get(last_bot)
    return last_bot_num

def cities(message: str):  # функция игры в города
    global last_bot
    global timer
    if last_bot != '' or timer == 0:
        num_of_last_bot = FindNumbersOfBukvs()
        if message in alphabet[num_of_last_bot]:

            # Получаем последнюю букву сообщения
            last = message[len(message) - 1].lower()
            #if message in alphabet[lalast_num]:
            # Получаем предпоследнюю букву, если длина сообщения больше 1
            #lalast = message[len(message)-2].lower() if last == 'ь' or last == 'ъ' or last == "ы" else None

            # Проверяем, есть ли последняя буква в словаре
            lalast = last
            x = 1

            while True:

                if letter_map[lalast] == 0:
                    lalast = message[len(message) - x].lower()

                # num_of_bukv = list(letter_map.keys()).index(lalast) + 1
                # print(num_of_bukv)
                    #rand = random.randint(0, letter_map[lalast])
                    x += 1
                    continue
                elif letter_map[lalast] > 0:
                    num_of_bukv = list(letter_map.keys()).index(lalast) + 1
                    print(num_of_bukv)
                    rand = random.randint(0, letter_map[lalast])  # Генерируем случайный индекс города
                    break
                #elif letter_map[lalast] > 0:
                #   num_of_bukv = list(letter_map.keys()).index(lalast) + 1
                #  print(num_of_bukv)
                #  rand = random.randint(0, letter_map[lalast])

                else:
                    return "Не могу подобрать город на эту букву."

            # Получаем название города из списка `alphabet` по индексу
            computer_ans = alphabet[num_of_bukv][rand - 1]
            lalast = ''



    else:
        computer_ans = "Такого города не существует в России"
    last_bot = computer_ans[len(computer_ans) - 1]
    return computer_ans

def numbers(user_num: int, rand_num: int):  # функция игры в угадай число
    res_num = ''
    if user_num > rand_num:
        res_num = 'Загаданное число меньше'
    elif user_num < rand_num:
        res_num = 'Загаданное число больше'
    else:
        res_num = 'Поздравляю! Вы угадали число'
    return res_num


@bot.message_handler(commands=['start'])

def main(message):
    print("user.start")
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}{' '+message.from_user.last_name if message.from_user.last_name is not None else ''}!\n'
        'В какую из игр ты хочешь поиграть: в "города" или в "угадай число"?'
    )


curr_game = ""
curr_rand_num = 0


@bot.message_handler()
def info(message):
    global curr_game, curr_rand_num
    user_text = message.text.lower()
    # Если выбор игры
    if user_text == 'города':
        bot.send_message(message.chat.id, "Напишите название города.")
        curr_game = "города"
    elif user_text == 'угадай число':
        bot.send_message(message.chat.id, "Я загадал число от 1 до 100. Попробуйте угадать!")
        curr_rand_num = random.randint(1, 100)
        curr_game = "угадай число"
    elif user_text == 'стоп':
        bot.send_message(message.chat.id,
                         "Игра остановлена. Напишите 'города' или 'угадай число', чтобы начать заново.")
        curr_game = ""
    # Если игра
    elif curr_game == "угадай число":
        try:
            user_num = int(user_text)
            play_numbers(message, user_num)
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите число.")
    elif curr_game == "города":
        play_cities(message)
    else:
        bot.send_message(message.chat.id, "Я вас не понял. Напишите 'города' или 'угадай число'.")


def play_cities(message):
    global timer
    user_city = message.text
    timer += 1
    bot.send_message(message.chat.id, cities(user_city))


def play_numbers(message, user_num: int):
    global curr_rand_num, curr_game
    response = numbers(user_num, curr_rand_num)
    bot.send_message(message.chat.id, response)
    if response == 'Поздравляю! Вы угадали число':
        curr_rand_num = 0
        curr_game = ""


print("Успешный запуск прослушивания бота")
bot.infinity_polling()