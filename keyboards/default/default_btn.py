from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp, db, bot
from data.config import ADMINS


admin_main = ReplyKeyboardMarkup(
    keyboard=[
 
        [
            KeyboardButton(text="🤼‍♂️ UFC Janglar"), 
        ],
         [
            KeyboardButton(text="➕ Jang qo'shish"), 
            KeyboardButton(text="➖ Jang o'chirish"), 
        ],
                  [
            KeyboardButton(text="🔔/🔕 Ovoz berishni yoqish/o'chirish"), 
        ],
                [
            KeyboardButton(text="⚔️ Jang hisobi"), 
            KeyboardButton(text="📊 Reyting"), 
        ],
                   [
            KeyboardButton(text="↔️ Qo'shimcha bo'lim"), 
        ],
         
    ],
    resize_keyboard=True,
    input_field_placeholder="Admin buyruqlari"
)


admin_main_2= ReplyKeyboardMarkup(
    keyboard=[
 
         [
            KeyboardButton(text="⛓ Kanallar ro'yxati"), 
        ],
         [
            KeyboardButton(text="➕ Kanal qo'shish"), 
            KeyboardButton(text="➖ Kanal o'chirish"), 
        ],
                  [
            KeyboardButton(text="📤 Xabar yozish"), 
        ],
       
                   [
            KeyboardButton(text="⏏️ Bosh menu"), 
        ],
         
    ],
    resize_keyboard=True,
    input_field_placeholder="Admin buyruqlari 2"
)


back_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚫 Bekor qilish"), 
        ],
         
    ],
    resize_keyboard=True,
    input_field_placeholder="Bekor qilish uchun bosing"
)


voice_mute = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔕 Ovoz berishni to'xtatish 🔕"), 
        ],
         [
            KeyboardButton(text="🚫 Bekor qilish"), 
        ],
    ],
    resize_keyboard=True,
)

voice_unmute = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔔 Ovoz berishni yoqish 🔔"), 
        ],
         [
            KeyboardButton(text="🚫 Bekor qilish"), 
        ],
    ],
    resize_keyboard=True,
)




user_main = ReplyKeyboardMarkup(
    keyboard=[
 

         [
            KeyboardButton(text="🤼‍♂️ UFC Janglar"), 
        ],
                  [
            KeyboardButton(text="🏁 Ovoz berish"), 
            KeyboardButton(text="🔱 Yig'ilgan ball"), 
        ],
                [
            KeyboardButton(text="🤖 Bot haqida"), 
            KeyboardButton(text="📊 Reyting"), 
        ],
                   [
            KeyboardButton(text="✍️ Adminga xabar yozish"), 
        ],
         
    ],
    resize_keyboard=True,
    input_field_placeholder="Asosiy menu"
)
