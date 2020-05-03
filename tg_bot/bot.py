import os
import subprocess
import logging
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, \
        InlineKeyboardMarkup, InlineKeyboardButton, \
        CallbackQuery
from aiogram.utils import executor

from conf.conf import *
from translate.translate import Translate

API_TOKEN = bot_api_token
logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

tr = Translate()

commands = ['help', 'translate', 'search_dictionary', 'show_dictionary', 'rules']
help_message = ''' \
    ivrez's english learing bot.
    available commands:
    /start - start bot interaction
    /translate - translate word using google api
    /search - search words in local dict
    /show_dict - show all words in local dict
    /rules - show engish rules from local dict
'''

class Form(StatesGroup):
    translate = State()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(help_message)

@dp.message_handler(commands=['translate'])
async def send_welcome(message: types.Message):
    await Form.translate.set()
    quit_btn = InlineKeyboardButton('quit', callback_data='quit_btn')
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(quit_btn)
    await message.answer("input some text here", reply_markup=inline_kb)

@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer(help_message)

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
        add_to_dict_btn = InlineKeyboardButton('add to dictionary', callback_data='add_btn')
        quit_btn = InlineKeyboardButton('quit', callback_data='quit_btn')
        inline_kb = InlineKeyboardMarkup()
        inline_kb.add(add_to_dict_btn)
        inline_kb.add(quit_btn)
        await message.answer(answer, reply_markup=inline_kb)

    except Exception as err:
        answer = "Translation Error: " + str(err)
        await message.answer(answer)

@dp.callback_query_handler(lambda c: c.data == 'add_btn', state="*")
async def process_callback_add_to_dictionary(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    src_lang = 'en'
    dest_lang = 'ru'
    text = str(callback_query.message.text)
    li = re.split(" |\n", text)
    if li[0] == 'ru:':
        src_lang = 'ru'
        dest_lang = 'en'
    li.pop(0)
    print(li[0])

    stop = dest_lang + ':'
    src_text = ''
    stop_i = 0
    for i, word in enumerate(li):
        if word == stop:
            stop_i = i+1
            break
        src_text += word + ' '

    dest_text = ' '.join(li[stop_i:])

    #print("LIST:")
    #print(li)
    #print(src_lang, ' : ', src_text)
    #print('\n')
    #print(dest_lang, ' : ', dest_text)
    tr.add_word(src_text, dest_text) if src_lang == 'en' else tr.add_word(dest_text, src_text)

    await bot.send_message(callback_query.from_user.id, 'words added to dictionary')

@dp.callback_query_handler(lambda c: c.data == 'quit_btn', state="*")
async def process_callback_quit(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await bot.send_message(callback_query.from_user.id, help_message)
