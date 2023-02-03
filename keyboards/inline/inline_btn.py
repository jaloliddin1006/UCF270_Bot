from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, db, bot
import asyncio



war_check = InlineKeyboardMarkup(
        inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data=f"yes_check"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data=f"no_check"),
            
            
        ],
        
    ])


 
def inline_channel_btn(wars):
    # await db.create()
    # wars = await db.select_all_wars()
    if len(wars)<=6:
        row = 3
    elif len(wars)<=8: 
        row = 4
    elif len(wars)<=12: 
        row = 6
    elif len(wars)<=16: 
        row = 8
    else:
        row = 10
    
    wars_check = InlineKeyboardMarkup(row_width=row)
    tr = 1
    for war in wars:
        wars_check.insert(InlineKeyboardButton(text=f"{tr}", callback_data=f"{war[0]}"))
        tr += 1
    wars_check.add(InlineKeyboardButton(text=f"🔙 Ortga", callback_data=f"back_wars"))
        
    return wars_check

 
def inline_wars_btn(wars):
    # await db.create()
    # wars = await db.select_all_wars()
    if len(wars)<=6:
        row = 3
    elif len(wars)<=8: 
        row = 4
    elif len(wars)<=12: 
        row = 6
    elif len(wars)<=16: 
        row = 8
    else:
        row = 10
    
    wars_check = InlineKeyboardMarkup(row_width=row)
    tr = 1
    for war in wars:
        wars_check.insert(InlineKeyboardButton(text=f"{tr}-juftlik", callback_data=f"{war[0]}"))
        tr += 1
    wars_check.add(InlineKeyboardButton(text=f"⬅️ ", callback_data=f"back_wars_group"))
    wars_check.insert(InlineKeyboardButton(text=f"➡️ ", callback_data=f"forward_wars_group"))
    wars_check.add(InlineKeyboardButton(text=f"🔝 Menu", callback_data=f"back_wars"))
        
    return wars_check


def inline_wars_btn_v(wars):
    # await db.create()
    # wars = await db.select_all_wars()
    # if len(wars)<=:
    #     row = 3
    # elif len(wars)<=8: 
    #     row = 4
    # elif len(wars)<=12: 
    #     row = 6
    # elif len(wars)<=16: 
    #     row = 8
    # else:
    #     row = 10
    row = 5
    
    wars_check = InlineKeyboardMarkup(row_width=row)
    tr = 1
    for war in wars:
        wars_check.insert(InlineKeyboardButton(text=f"{tr}-juftlik", callback_data=f"{war[0]}"))
        tr += 1
    wars_check.add(InlineKeyboardButton(text=f"⬅️ ", callback_data=f"back_wars_group"))
    wars_check.insert(InlineKeyboardButton(text=f"➡️ ", callback_data=f"forward_wars_group"))
    wars_check.add(InlineKeyboardButton(text=f"🔝 Menu", callback_data=f"back_wars"))
        
    return wars_check


def war_winner(name1, name2):

    war_check = InlineKeyboardMarkup(
            inline_keyboard=[
            [
                InlineKeyboardButton(text=f"✅ {name1}", callback_data=f"{name1}"),
                InlineKeyboardButton(text=f"✅ {name2}", callback_data=f"{name2}"),
                
                
            ],
               [
                InlineKeyboardButton(text=f"❌ Jang bekor qilindi", callback_data=f"war_cancel"),
                
                
            ],
                [
                InlineKeyboardButton(text=f"🔙 Ortga", callback_data=f"back_wars_gr"),
                
                
            ],
            
        ])
    return war_check



def war_winner_2(name1, name2):

    war_check = InlineKeyboardMarkup(
            inline_keyboard=[
            [
                InlineKeyboardButton(text=f"✅ {name1}", callback_data=f"{name1}"),
                InlineKeyboardButton(text=f"✅ {name2}", callback_data=f"{name2}"),
                
                
            ],
             
                [
                InlineKeyboardButton(text=f"🔙 Ortga", callback_data=f"back_wars_gr"),
                
                
            ],
            
        ])
    return war_check
