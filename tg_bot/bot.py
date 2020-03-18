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
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

tr = Translate()

class Form(StatesGroup):
    translate = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.reply("ivrez's english learning words tg bot", reply=False)

@dp.message_handler(commands=['translate'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/translate` command
    """
    await Form.translate.set()
    await message.reply("input some text here", reply=False)


@dp.message_handler(state=Form.translate)
async def process_translate(message: types.Message, state: FSMContext):
    """
    Process translation 
    """
    async with state.proxy() as data:
        text = message.text

    try:
        translated = tr.translate(text)
    except Exception as err:
        translated = "Translation Error: " + err

    await message.reply(translated, reply=False)
