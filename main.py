#1. Запускаем бота, он слушает беседу.
#2. При появлении собеседника спрашиваем - кому ищем пару
#3. из цели вытаскиваем искомые параметры, обрабатываем и предлагаем собеседнику
#4. Если согласен - далее, если нет - предлагаем поменять.
#5. Проводим поиск по параметрам, сохраняем результаты в БД
#6. Шуршим БД, ищем наиболее подходящих
#7. Говорим, сколько подходящих нашли, спрашиваем, сколько выводить.
#8. выводим, сколько указано.
import os
import time
import datetime

from vk_bot import VKBot


def funcrt(*args):
    print(len(args))
    print(*args)
    temp_target = {}
    target = {'bdate': "14.4.1988"}
    bdate = datetime.datetime.strptime("14.4.1988", "%d.%m.%Y")#.timetuple()
    print(type(bdate))


if __name__ == '__main__':
    bot = VKBot(vk_group_token = os.getenv('bot_token'))
    bot.wait_for_user()
