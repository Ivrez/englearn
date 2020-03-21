import os
import subprocess
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from conf.conf import *
from translate.translate import Translate

API_TOKEN = bot_api_token
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

tr = Translate()

commands = ['help', 'translate', 'search_dictionary', 'show_dictionary', 'rules']

class Form(StatesGroup):
    translate = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("ivrez's english learning words tg bot.\ncommands - /help.\nfuck you.")
@dp.message_handler(commands=['help'])
async def send_commands(message: types.Message):
    answer = ''
    for i in commands:
        answer += '/' + i + '\n'
    await message.answer(answer)


@dp.message_handler(commands=['translate'])
async def send_welcome(message: types.Message):
    await Form.translate.set()
    await message.answer("input some text here")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('canceled.\nall commands - /help.\nfuck you', reply_markup=types.ReplyKeyboardRemove(), reply=False)

@dp.message_handler(state=Form.translate)
async def process_translate(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            text = str(message.text)

        translated = tr.translate(text)
        src_lang = translated.src
        dest_lang = translated.dest
        tr_text = translated.text
        answer = src_lang + ": " + text + '\n'
        answer += dest_lang + ": " + tr_text + '\n'
        answer += '/cancel for fuck off.'

    except Exception as err:
        answer = "Translation Error: " + err

    await message.answer(answer, reply=False)
