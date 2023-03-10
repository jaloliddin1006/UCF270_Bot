import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from keyboards.inline.subscription import check_button, start_keyboard
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS
# from data.config import CHANNELS
from utils.misc import subscription
from loader import bot, db


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):  
        try: 
                
            CHANNELS = await db.select_all_channels()
            
            if update.message:
                user = update.message.from_user.id
                if update.message.text in ['/start', '/help']:
                    return
            elif update.callback_query:
                user = update.callback_query.from_user.id
                if update.callback_query.data == "check_subs":
                    return
            else:
                return
            join_channel = []

            result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
            final_status = True
            for channel_id in CHANNELS:
                # print(channel_id[0])
                # print(await bot.get_chat(channel_id[0]))
                status = await subscription.check(user_id=user,
                                                channel=channel_id[0])
                final_status *= status
                channel = await bot.get_chat(channel_id[0])
                    
                # status = await bot.get_chat_member(channel, update.message.from_user.id)
                invite_link = await channel.export_invite_link()
                
                if not status:
                    channel_info = [invite_link, channel.title, 0]
                else:
                    channel_info = [invite_link, channel.title, 1]
                    # aa += 1
                join_channel.append(channel_info)
                
                if not status:
                    # invite_link = await channel.export_invite_link()
                    result += (f"???? <a href='{invite_link}'>{channel.title}</a>\n")

            if not final_status:
                await update.message.answer("Kanallarga to'liq obuna bo'ling", reply_markup=ReplyKeyboardRemove())
                await update.message.answer(result, disable_web_page_preview=True, reply_markup=check_button(join_channel))
                raise CancelHandler()
        except:
            await db.delete_channels()
            
            await bot.send_message(ADMINS[0], "Ushbu bot qaysidir kanaldan chiqarib yuborildi, Botning kanalda adminligiga to'laqonli ishonch hosil qiling. Xavfsizlik uchun barcha ulangan kanallar majburiy a'zolik ro'yxatidan o'chirildi. ")