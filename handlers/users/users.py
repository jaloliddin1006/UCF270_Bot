import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from loader import dp, db, bot
from data.config import ADMINS
from keyboards.inline.inline_btn import inline_wars_btn, war_winner_2, inline_wars_btn_v
from keyboards.default.default_btn import user_main, back_btn
from aiogram.dispatcher import FSMContext



@dp.message_handler(text="🏁 Ovoz berish", state="*")
async def janglar_uchun_ovoz_berish(message: types.Message, state=FSMContext):
    global war_v_tr
    war_v_tr = 0
    
    try:
        wars = await db.select_all_wars_v(war_v_tr)
        # print(message)
        id  = await db.select_user(tg_id=message.from_user.id)
        # print(wars)
        tr = 1
        await message.answer("👊 Mavjud UFC janglarga kim g'olib bo'lishiga ovoz bering", reply_markup=ReplyKeyboardRemove())
        # text = f"Ovoz berilmagan janglar {len(await db.select_all_wars())} ta\n\n"
        text = "👊 Janglar\n(✅ -  sizning tanlovlaringiz)\n\n"
        if wars[0][7]==1:
            for war in wars:
                voice = await db.select_voice(id[0], war[0])
                try:
                    if voice[3]==war[1]:
                        fir = "✅"
                        sec = ""
                    elif voice[3]==war[2]:
                        fir = ""
                        sec = "✅"
                except:
                        fir = ""
                        sec = ""
                text += f"{tr}.  {fir} {war[1]}      -⚔️-    {sec} {war[2]} \n"
                text += f" Sana: \t{war[3]}\n\n"
                tr += 1
        # await message.answer(text)
                
            # wars = await db.select_all_wars()
            # u_voice = await db.select_user_voice(message.from_user.id)
            # if len(wars) > len(u_voice):
                # for war in wars:
            # if not war[6]:
            await message.answer(text, reply_markup=inline_wars_btn_v(wars))
        #         check_voice = await db.select_check_user_voice(message.from_user.id, war[0])
        #         if not check_voice:
        
        
            
            await state.set_state("user_select_winner")
            # else:
            #     await message.answer("Hali janglar qo'yilmagan", reply_markup=user_main)
            #     await state.finish()
            # else:
            #     await state.finish()
            #     await message.answer("hammasiga ovoz berildi 11", reply_markup=user_main)    
            # await message.answer("hammasiga ovoz berib bo'lingan", reply_markup=user_main)
            # await state.finish()
        else:
            
            await message.reply("Janglar uchun ovoz berish to'xtatilgan", reply_markup=user_main)
        
    except:
        await message.answer("Ayni vaqtda bu bo'lim ishlamaydi", reply_markup=user_main) 
    
        
@dp.callback_query_handler(text="back_wars",state="*")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    await call.message.answer("Jang uchun ovoz berish bekor qilindi", reply_markup=user_main)
    await state.finish()
    
    
    
    
@dp.callback_query_handler(state="user_select_winner", text="forward_wars_group")
async def change_(call: CallbackQuery, state=FSMContext):
    global war_v_tr
    war_v_tr += 5

    try:
        wars = await db.select_all_wars_v(war_v_tr)
        # print(message)
        id  = await db.select_user(tg_id=call.from_user.id)
        # print(wars)
        tr = 1
        # text = f"Ovoz berilmagan janglar {len(await db.select_all_wars())} ta\n\n"
        text = "👊 Janglar\n(✅ -  sizning tanlovlaringiz)\n\n"
        if wars[0][7]==1:
            for war in wars:
                voice = await db.select_voice(id[0], war[0])
                # print(voice)
                try:
                    if voice[3]==war[1]:
                        fir = "✅"
                        sec = ""
                    elif voice[3]==war[2]:
                        fir = ""
                        sec = "✅"
                except:
                        fir = ""
                        sec = ""
                text += f"{tr}.  {fir} {war[1]}      -⚔️-    {sec} {war[2]} \n"
                text += f" Sana: \t{war[3]}\n\n"
                tr += 1
            # await call.message.answer("👊 Mavjud UFC janglarga kim g'olib bo'lishiga ovoz bering", reply_markup=ReplyKeyboardRemove())
            await call.message.delete()
            # await call.message.edit_reply_markup(text=text, reply_markup=inline_wars_btn_v(wars))
            await call.message.answer(text, reply_markup=inline_wars_btn_v(wars))
            
            await state.set_state("user_select_winner")
        else:
            await state.finish()
            
            await call.message.reply("Janglar uchun ovoz berish to'xtatilgan", reply_markup=user_main)
        
    except Exception as err:
        war_v_tr -= 5
        # await call.answer()
        # await state.finish()
        await call.answer(f"Boshqa ovoz berilmagan janglar qolmadi ") 
    
    
    
@dp.callback_query_handler(state="user_select_winner", text="back_wars_group")
async def change_(call: CallbackQuery, state=FSMContext):
    global war_v_tr
    war_v_tr -= 5
    print(war_v_tr)
    try:
        wars = await db.select_all_wars_v(war_v_tr)
        # print(message)
        id  = await db.select_user(tg_id=call.from_user.id)
        # print(wars)
        tr = 1
        # text = f"Ovoz berilmagan janglar {len(await db.select_all_wars())} ta\n\n"
        text = "👊 Janglar\n(✅ -  sizning tanlovlaringiz)\n\n"
        if wars[0][7]==1:
            for war in wars:
                voice = await db.select_voice(id[0], war[0])
                # print(voice)
                try:
                    if voice[3]==war[1]:
                        fir = "✅"
                        sec = ""
                    elif voice[3]==war[2]:
                        fir = ""
                        sec = "✅"
                except:
                        fir = ""
                        sec = ""
                text += f"{tr}.  {fir} {war[1]}      -⚔️-    {sec} {war[2]} \n"
                text += f" Sana: \t{war[3]}\n\n"
                tr += 1
            # await call.message.answer("👊 Mavjud UFC janglarga kim g'olib bo'lishiga ovoz bering", reply_markup=ReplyKeyboardRemove())
            await call.message.delete()
            # await 
            await call.message.answer(text, reply_markup=inline_wars_btn_v(wars))
            
            await state.set_state("user_select_winner")
        else:
            await state.finish()
            
            
            await call.message.reply("Janglar uchun ovoz berish to'xtatilgan", reply_markup=user_main)
        
    except Exception as err:
        war_v_tr += 5
        await call.answer(f"Bu janglarni eng birinchisi") 





@dp.callback_query_handler(state="user_select_winner")
async def change_(call: CallbackQuery, state=FSMContext):
    war_id = call.data
    war = await db.select_war(war_id)

    name1 = war[1]
    name2 = war[2]
    text = f"{war[1]}  ⚔️  {war[2]} \n\n"
    text += f"📅 Jang kuni: {war[3]}\n\n"
    if war[6]==None:
        await call.message.delete()
        await state.update_data(
            {"war": war_id}
    )
                    
        text += f"✅ Kim g'olib bo'ladi.\n"
        await bot.send_photo(call.from_user.id, war[4], text, reply_markup=war_winner_2(name1, name2))
        await state.set_state("user_select_winner_2")
    else:
        await call.answer()
        text += f"👊 G'olib: {war[6]}"
        await bot.send_photo(call.from_user.id, war[4], f"Jang o'z nihoyasiga yetgan.\n\n{text}")
        # await call.message.answer()
        await state.set_state("user_select_winner")
    
    
@dp.callback_query_handler(text="back_wars_gr",state="*")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    await call.message.answer("Jang uchun ovoz berish bekor qilindi", reply_markup=user_main)
    await state.finish()
    
    
# df3sf1sd32f1sd32f1
    
    
    
@dp.callback_query_handler(state="user_select_winner_2")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer(f"{call.data} ✅")
    
    data = await state.get_data()
    war2 = data.get("war")
    id  = await db.select_user(tg_id=call.from_user.id)
    try:
        await db.delete_user_voice(id[0], int(war2))
        await db.add_voice(id[0], int(war2), call.data)
        # await db.update_user_voice(id[0], int(war2), call.data)
    except:
        await db.add_voice(id[0], int(war2), call.data)
    
    # print(aa)
    wars = await db.select_all_wars_v(war_v_tr)
    
    tr = 1
    await call.message.answer("👊 Mavjud UCF janglarga kim g'olib bo'lishiga ovoz bering", reply_markup=ReplyKeyboardRemove())
    text = "👊 Janglar\n(✅ -  sizning tanlovlaringiz)\n\n"
    if wars[0][7]==1:
        for war in wars:
            voice = await db.select_voice(id[0], war[0])
            try:
                if voice[3]==war[1]:
                    fir = "✅"
                    sec = ""
                elif voice[3]==war[2]:
                    fir = ""
                    sec = "✅"
            except:
                    fir = ""
                    sec = ""
            text += f"{tr}.  {fir} {war[1]}      -⚔️-    {sec} {war[2]} \n"
            text += f" Sana: \t{war[3]}\n\n"
            tr += 1
        await call.message.answer(text, reply_markup=inline_wars_btn_v(wars))
        await state.set_state("user_select_winner")
                
    else:
        await state.finish()
        
        await call.message.reply("Janglar uchun ovoz berish to'xtatilgan", reply_markup=user_main)
    
        
        
        

@dp.message_handler(text="🎯 Yig'ilgan ball", state=None)
async def janglar_uchun_ovoz_berish(message: types.Message, state=FSMContext):
    ball = await db.select_user(tg_id = message.from_user.id)
    await message.answer(f"<i> {message.from_user.full_name} sizning jami to'plagan balingiz: {ball[5]} ball</i>")
    
    


@dp.message_handler(text="🤖 Bot haqida", state=None)
async def janglar_uchun_ovoz_berish(message: types.Message, state=FSMContext):
    text = f"Assalomu alaykum {message.from_user.full_name}.\n\n"
    text += "🤖 Bu bot orqali «UFC Fantasy» turnirida ishtirok etib siz o‘z menejerlik qobiliyatingizni namoyon etishingiz va vaqtingizni maroqli o‘tkazgan holda sovrinlarga ega bo‘lishingiz mumkin.\n\n"

    text +="🤩 Turnirlarda ishtirok etish mutloq bepul. Buning uchun siz, bizning botimizda ishtirok etish tugmasini bosishingiz kerak bo‘ladi.\n\n"

    text +="👊  MIXSPORT telegram kanaliga o‘ting va batafsil ma’lumotni oling.\n"
    await message.answer(f"{text}\n@mixsportuz_bot |  @mixsportuzb ")
    
    

@dp.message_handler(text="✍️ Adminga xabar yozish", state=None)
async def janglar_uchun_ovoz_berish(message: types.Message, state=FSMContext):
    await message.answer("Marhamat adminga xabaringizni qoldiring.", reply_markup=back_btn)
    await state.set_state("adminga-xabar")
    
    
@dp.message_handler( state="adminga-xabar", text="🚫 Bekor qilish")
async def janglar_uchun_ovoz_berish(message: types.Message, state=FSMContext):
    await message.answer("Bosh menu", reply_markup=user_main)
    await state.finish()   
    
    
@dp.message_handler( state="adminga-xabar")
async def janglar_uchun_ovoz_berish(message: types.Message, state=FSMContext):
    try:
        # await bot.send_message(ADMINS[0],"📌 Yangi xabar")
        msg = f"📌 Yangi xabar\n"
        msg += f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>\n\n"
        msg += f"{message.text}"
        await bot.send_message(ADMINS[0], msg)
        await message.answer("Xabaringiz adminga yetkazildi", reply_markup=user_main)
        await state.finish()
        
    except:
        
        await message.answer("Faqat matn ko'rinishidagi xabarlarni yubora olasiz.")
        await message.answer("Marhamat adminga xabaringizni qoldiring.", reply_markup=back_btn)
        
         
        
        
        
