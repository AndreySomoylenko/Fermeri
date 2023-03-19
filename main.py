import requests
import numpy
import math
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage


def sm(sh, dist):
    t = math.ceil(math.log2(sh)) - 2

    s = 0

    for i in range(1, t + 1):
        s += 2 * 200 / (200 + 8 * 2 ** (i - 1))
    x = math.ceil((dist - s) / 2)
    resFuel = 100 * 10 * (t + x)
    resO = 7 * x * 10 + 7 * x * 50
    return resFuel,  resO

def sm2(resFuel, resO):
    return resFuel // 10, resO // 7

def length(sh, dist):
    t = math.ceil(math.log2(sh)) - 2

    s = 0

    for i in range(1, t + 1):
        s += 2 * 200 / (200 + 8 * 2 ** (i - 1))
    x = math.ceil((dist - s) / 2)
    return x + t



hrds = {
    'X-Auth-Token': 'v427t5hx'
}

#req = requests.get('https://dt.miet.ru/ppo_it_final', headers=hrds).json()['message']

# for i in req:
#     pts = i['points']
#     summ = 0
#     sum2 = 0
#     print('Новый полет')
#     for p in pts:
#         res = sm(p['SH'], p['distance'])
#         res2 = length(p['SH'], p['distance'])
#         sum2 += res2
#         print('Fuel:', res[0])
#         print('Oxy', res[1])
#         print('sm', sum(res))
#         print()
#         summ += sum(res)
#     print('общ сумма', summ)
#     print('общ дни', sum2)
#     print('\n')

TOKEN = '6179449058:AAGkvnqpXluWwcnyLyXODUEtPwZfcedVI2g'

# class Form(StatesGroup):
#     s1 = State()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['fly'])
async def fly(message: types.Message):
    await message.reply('Новый полет. Введите данные по порядку\nФормат: "sh dist" в каждой новой строке')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Команды:\n/fly\n/get')

@dp.message_handler(commands=['get'])
async def get(message: types.Message):
    req = requests.get('https://dt.miet.ru/ppo_it_final', headers=hrds).json()['message']

    for i in req:
        pts = i['points']
        summ = 0
        sum2 = 0
        output = ''
        sumFuel = 0
        sumOxy = 0

        output += 'Новый полет\n\n'
        for p in pts:
            res = sm(p['SH'], p['distance'])
            res2 = length(p['SH'], p['distance'])
            sum2 += res2
            res3 = sm2(res[0], res[1])
            output += 'Fuel Money: ' + str(res[0]) + '\n'
            output += 'Oxy Money: ' + str(res[1]) + '\n'
            output += 'Fuel: ' + str(res3[0]) + '\n'
            output += 'Oxy: ' + str(res3[1]) + '\n'
            output += '\n'
            sumFuel = res3[0]
            sumOxy = res3[1]
            summ += sum(res)
        output += 'общ сумма: ' + str(summ) + '\n'
        output += 'общ топливо: ' + str(sumFuel) + '\n'
        output += 'общ кислород: ' + str(sumOxy) + '\n'

        output += 'общ дни: ' + str(sum2) + '\n'
        output += '\n'
        await message.reply(output, reply=False)


@dp.message_handler()
async def any(message: types.Message):
    pts = str(message.text).split('\n')
    summ = 0
    sum2 = 0
    output = ''
    sumFuel = 0
    sumOxy = 0
    for p in pts:
        p = [int(x) for x in p.split(' ')]
        res = sm(p[0], p[1])
        res2 = length(p[0], p[1])
        sum2 += res2
        res3 = sm2(res[0], res[1])
        output += 'Fuel Money: ' + str(res[0]) + '\n'
        output += 'Oxy Money: ' + str(res[1]) + '\n'
        output += 'Fuel: ' + str(res3[0]) + '\n'
        output += 'Oxy: ' + str(res3[1]) + '\n'
        output += '\n'
        sumFuel = res3[0]
        sumOxy = res3[1]
        summ += sum(res)
    output += 'общ сумма: ' + str(summ) + '\n'
    output += 'общ топливо: ' + str(sumFuel) + '\n'
    output += 'общ кислород: ' + str(sumOxy) + '\n'

    output += 'общ дни: ' + str(sum2) + '\n'
    output += '\n'
    await message.reply(output, reply=False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






