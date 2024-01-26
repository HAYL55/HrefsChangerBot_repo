
from aiogram import Bot
from aiogram.types import Message, FSInputFile, ContentType
from aiogram.utils.markdown import hlink, link
from aiogram.enums import ParseMode
from aiogram.enums.message_entity_type import MessageEntityType
from core.utils.settings import Settings
from core.utils.States import Stateses
from aiogram.fsm.context import FSMContext
import emoji
import re
from bs4 import BeautifulSoup


async def get_start(message:Message, bot:Bot, state: FSMContext):
    await message.answer('Сейчас введите ссылку которая заменит собой все ссылки из следующего сообщения')
    await state.set_state(Stateses.INPUT_HREF)

async def get_href(message:Message,state:FSMContext):
    file = open('href1', 'w')
    file.write(message.text)
    await state.set_state(Stateses.INPUT_TEXT)
    await message.answer('теперь введите текст в котором нужно заменить ссылки')

async def litl_chang(message:Message, bot:Bot, state: FSMContext):
    hreff = open('href1')
    href = hreff.read()
    hrefs = []
    counter = 0
    new_message_last = ''

    text = message.html_text
    #hrefs_not_chanched = re.findall(r'href=[\'"]?([^\'" >]+)', text)        #реальные ссылки
    #hrefs_not_chanched = re.findall(r'(https?://\S+)', text)                #вместе с тегами и гавном
    hrefs_not_chanched = re.findall ("(?P<url>https?://[^\s^\"]+)", text)


    for i in hrefs_not_chanched:
        af = f'<a href="{href}">{i}</a>'
        hrefs.append(af)

    # print(len(hrefs_not_chanched))
    # print(len(hrefs))
    #
    # for i in range(0,len(hrefs_not_chanched)):
    #     print(hrefs_not_chanched[i])
    # for i in range(0,len(hrefs)):
    #     print(hrefs[i])

    # if message.entities != None:
    #     for entiti in message.entities:
    #         if entiti.url != None:
    #             entiti.url = href

    if message.content_type == ContentType.PHOTO:
        if message.caption_entities != None:
            for entiti in message.caption_entities:
                if entiti.url != None:
                    entiti.url = href

    elif message.content_type == ContentType.TEXT:
        if message.entities != None:
            for entiti in message.entities:
                if entiti.url != None:
                    entiti.url = href

    new_message = message.html_text

    for i in range(0,len(hrefs)):
        if i == 0 and hrefs_not_chanched[i] != href:
            new_message_last = new_message.replace(hrefs_not_chanched[i], hrefs[i])
        elif hrefs_not_chanched[i] != href:
            new_message_last = new_message_last.replace(hrefs_not_chanched[i], hrefs[i])

    if message.content_type == ContentType.PHOTO:
        file1 = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file1.file_path, 'boba.jpg')

        photo = FSInputFile("boba.jpg")

        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=new_message_last, parse_mode="HTML")

    elif message.content_type == ContentType.TEXT:
        await message.answer(new_message_last, disable_web_page_preview=True, parse_mode="HTML")

    await state.set_state(Stateses.NONE)

async def change_href(message:Message, state: FSMContext):
    new_message = ''
    now_offset_end = 0
    offset_end = 0
    next_ = ''
    end_result = 0
    if message.entities != None:
        for entiti in message.entities:
            if entiti.url != None:
                hreff = open('href1')
                href = hreff.read()
                prev_ = message.text[now_offset_end:entiti.offset]
                next_ = message.text[entiti.offset + entiti.length:]
                new_link = link(message.text[entiti.offset:entiti.offset+entiti.length - end_result], href)
                new_message += f'{prev_}{new_link}'
                #await message.answer(new_message, parse_mode="Markdown", disable_web_page_preview=True)
                now_offset_end = entiti.offset + entiti.length
                offset_end = entiti.offset + entiti.length
                #await state.set_state(Stateses.NONE)
                await message.answer(f'{len(message.text)} -> {offset_end}')
            else:
                pass

        if len(message.text) != offset_end:
            new_message += next_

        await message.answer(new_message, parse_mode="Markdown", disable_web_page_preview=True)


    else:
        await message.answer('текст не как не отформатирован')
