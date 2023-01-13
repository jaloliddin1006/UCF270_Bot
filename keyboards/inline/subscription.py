from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# check_button = InlineKeyboardMarkup(
#     inline_keyboard=[[
#         InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs")
#     ]]
# )

 
def check_button(channels):

    channels_check = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        if channel[2]==0:
            channels_check.insert(InlineKeyboardButton(text=f"{channel[1]}", url=f"{channel[0]}"))
        else:
            channels_check.insert(InlineKeyboardButton(text=f"✅{channel[1]}", url=f"{channel[0]}"))
    channels_check.add(InlineKeyboardButton(text=f"✅ Obunani tekshirish ✅ ", callback_data=f"check_subs"))
        
    return channels_check

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

studyboi = InlineKeyboardButton('https://t.me/studyboiibot', url='https://t.me/studyboiibot')
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(studyboi)