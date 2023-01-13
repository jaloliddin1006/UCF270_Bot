import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.default_btn import user_main
from loader import dp, db, bot
from data.config import ADMINS
from utils.misc import subscription
from aiogram.types import ReplyKeyboardRemove

from keyboards.inline.subscription import check_button, start_keyboard

@dp.message_handler(commands=['start'])
async def show_channels(message: types.Message):
    CHANNELS = await db.select_all_channels()
    try:
    # await db.add_user(122654789, "Jonibek 2", "@Yorqulov", 123456789)
        user = await db.add_user(message.from_user.id,
                                 message.from_user.full_name,
                                 message.from_user.username,
                                 0
                                 )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(tg_id=message.from_user.id)

    join_channel = []
    aa = 0
    for channel in CHANNELS:
        chat = await bot.get_chat(channel[0])
        invite_link = await chat.export_invite_link()
        status = await bot.get_chat_member(channel[0], message.from_user.id)
        
        if status['status'] == 'left':
            channel_info = [invite_link, chat.title, 0]
        else:
            channel_info = [invite_link, chat.title, 1]
            aa += 1
        join_channel.append(channel_info)
            
    if aa != len(CHANNELS):   
        await message.answer(f"""Assalomu alaykum {message.from_user.full_name}""", reply_markup=ReplyKeyboardRemove())
        await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n",
                        
                         reply_markup=check_button(join_channel),
                         disable_web_page_preview=True)
    else:
        await message.answer("Xush kelibsiz!", reply_markup=user_main)

@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    CHANNELS = await db.select_all_channels()
    
    await call.message.delete()
    join_channel = []
    aa = 0
    for channel in CHANNELS:
        chat = await bot.get_chat(channel[0])
        invite_link = await chat.export_invite_link()
        status = await bot.get_chat_member(channel[0], call.from_user.id)
        
        if status['status'] == 'left':
            channel_info = [invite_link, chat.title, 0]
        else:
            channel_info = [invite_link, chat.title, 1]
            aa += 1
        join_channel.append(channel_info)
            
    if aa != len(CHANNELS):   
        await call.message.answer(f"""{call.from_user.full_name} kanallarga to'liq obuna bo'ling""", reply_markup=ReplyKeyboardRemove())
        await call.message.answer(f"Quyidagi kanallarga obuna bo'ling: \n",
                        
                         reply_markup=check_button(join_channel),
                         disable_web_page_preview=True)
    else:
        await call.message.answer("Xush kelibsiz! Botdan foydalanishingiz mumkin", reply_markup=user_main)

    # await show_channels(call)
    # result = str()
    # join_channel = []
    # for channel in CHANNELS:
    #     status = await subscription.check(user_id=call.from_user.id,
    #                                       channel=channel)
    #     channel = await bot.get_chat(channel)
    #     if status:
    #         result += f"<b>✅ {channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"
    #     else:
    #         invite_link = await channel.export_invite_link()
    #         result += (f"<b>👉 {channel.title}</b> kanaliga obuna bo'lmagansiz. "
    #                    f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n")

    #     status1 = await bot.get_chat_member(channel, call.from_user.id)
    #     print(status1)
    #     print(status1['status'])
    #     if status1['status'] == 'left':
    #         channel_info = [invite_link, channel.title, 0]
    #         # join_channel.append(channel_info)
    #     else:
    #         channel_info = [invite_link, channel.title, 1]
    #     join_channel.append(channel_info)
            
    # await call.message.answer(result, disable_web_page_preview=True, reply_markup=check_button(join_channel))


# @dp.message_handler(CommandStart())
# async def bot_start(message: types.Message): 
#     try:
#     # await db.add_user(122654789, "Jonibek 2", "@Yorqulov", 123456789)
#         user = await db.add_user(message.from_user.id,
#                                  message.from_user.full_name,
#                                  message.from_user.username,
#                                  0
#                                  )
#     except asyncpg.exceptions.UniqueViolationError:
#         user = await db.select_user(tg_id=message.from_user.id)

#     await message.answer("Xush kelibsiz!", reply_markup=user_main)

#     # ADMINGA xabar beramiz
#     count = await db.count_users()
#     msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
#     # await bot.send_message(chat_id=ADMINS[0], text=msg)