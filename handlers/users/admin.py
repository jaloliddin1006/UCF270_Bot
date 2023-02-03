import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from data.config import ADMINS
from loader import dp, db, bot
from keyboards.default.default_btn import admin_main, admin_main_2, back_btn, voice_mute, voice_unmute
from keyboards.inline.inline_btn import war_check, inline_wars_btn, war_winner, inline_channel_btn


        
@dp.message_handler(text="📤 Xabar yozish", user_id=ADMINS)
async def get_reklama(msg:types.ContentTypes.all(), state: FSMContext):
    await msg.answer("Reklamani yuboring, yoki foydalanuvchilarga biror bir xabar yozing....", reply_markup=ReplyKeyboardRemove())
    await state.set_state("reklama")

@dp.message_handler(state="reklama", content_types=types.ContentType.ANY)
async def get_all_reklama(msg:types.Message,state:FSMContext):
    users = await db.select_all_users()
    son = 0
    await msg.answer(f"Bot a'zolari soni: {len(users)}")
    wait = await msg.answer("Biroz kuting, foydalanuvchilarga xabaringiz yetkazilayapti ... ", reply_markup=admin_main_2)
    await state.finish()
    for user in users:
        try:
            await bot.copy_message(user[1],msg.chat.id,msg.message_id, reply_markup=msg.reply_markup)
            son += 1
        except:
            pass
            # await db.delete_user(user_id=user[0])
        await asyncio.sleep(0.05)
    await wait.delete()
    await msg.answer(f"{son} nafar foydalanuvchilarga xabaringiz yetkazildi ✅ ", reply_markup=admin_main_2)
    # await asyncio.sleep(20)
    
    
@dp.message_handler(text="/start", user_id=ADMINS, state="*")
async def send_ad_to_all(message: types.Message):
    # await db.create()
    
    try:
    # await db.add_user(122654789, "Jonibek 2", "@Yorqulov", 123456789)
        user = await db.add_user(message.from_user.id,
                                 message.from_user.full_name,
                                 message.from_user.username,
                                 0
                                 )
    except:
        pass
    await message.answer("Assalommu alaykum hurmatli Admin", reply_markup=admin_main)
    
    

@dp.message_handler(text="📺 UFC Turnirlar")
async def send_ad_to_all(message: types.Message):
    try:
        await message.reply("👊 Mavjud UCF janglar ")
        await db.create()
        wars = await db.select_all_wars()
        tr = 1
        text = "👊 Janglar\n\n"
        if wars:
            for war in wars:
                if war[6]:
                    win = f"✅ G'olib:  <b>{war[6]}</b>\n📊 Xisob:  {war[5]}\n"
                else:
                    win = ""
                text += f"{tr}. {war[1]} - {war[2]} \n"
                text += win
                text += f"📅 Sana: \t{war[3]}\n\n"
                tr += 1
            
            # await bot.send_photo(message.from_user.id, war[4], text)
            await message.answer(text)
                # print(war)
            # await message.answer("Assalommu alaykum hurmatli Admin", reply_markup=admin_main)
        else:
            await message.answer("Birorta ham jang yo'q hozircha 1")
            
    except:
        await message.answer("Birorta ham jang yo'q hozircha")
    
     
#############   Jang qo'shish boshlandi  ####################

@dp.message_handler(text="➕ Jang qo'shish", user_id=ADMINS, state=None)
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Yangi jang qo'shish")
    await message.answer("1-jangchining ism-familiasini kiriting", reply_markup=back_btn)
    await state.set_state("firs_name")
    
    
@dp.message_handler(user_id=ADMINS,state="*", text="🚫 Bekor qilish")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await state.finish()
    await message.answer("Amal bekor qilindi.\n\nBosh menu", reply_markup=admin_main)
    
@dp.message_handler(state="firs_name", content_types="text")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    first_name = message.text
    await state.update_data(
            {"first_name": first_name}
        )
        
    await message.answer("2-jangchining ism-familiasini kiriting", reply_markup=back_btn)
    await state.set_state("second_name")
    
    
    
@dp.message_handler(state="second_name", content_types="text")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    second_name = message.text
    await state.update_data(
            {"second_name": second_name}
        )
        
    await message.answer("Ushbu jang sanasini kiriting (01-01-2023)", reply_markup=back_btn)
    await state.set_state("war_date")
    
    
@dp.message_handler(state="war_date", content_types="text")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    war_date = message.text
    await state.update_data(
            {"war_date": war_date}
        )
        
    await message.answer("Jangchilar juftligini rasmini yuboring", reply_markup=back_btn)
    await state.set_state("send_photo")
    
    
@dp.message_handler(state="send_photo", content_types="photo")
async def send_ad_to_all(message: types.Message, state=FSMContext):

    photo = message.photo[-1].file_id
    await state.update_data(
            {"photo": photo}
        )



    data = await state.get_data()
    first_name = data.get("first_name")
    second_name = data.get("second_name")
    war_date = data.get("war_date")
    
    # text = f"\t 👊‍♂️  \n\n"
    text = f"{first_name} - {second_name} \n\n"
    text += f"📅 Sana: \t{war_date}\n\n"
    text += f"Ma'lumotlar to'grimi?"
    
    await bot.send_photo(message.from_user.id, photo, text, reply_markup=war_check)
        
    await state.set_state("war_check")
    
    
@dp.callback_query_handler(state="war_check")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.edit_reply_markup()
    if call.data == "yes_check":
        
        data = await state.get_data()
        first_name = data.get("first_name")
        second_name = data.get("second_name")
        war_date = data.get("war_date")
        photo = data.get("photo")
        try:
            # await db.create()
            
            await db.add_war(first_name=first_name, second_name=second_name, war_date=war_date, photo=photo)
            await call.message.answer("Bazaga qo'shildi ✅")
            # users  = await db.select_all_users()
            # for i in users:
            #     try:
            #         await bot.send_message(i[1], "Yangi jang qo'shildi, o'z g'olibingizni belgilab qo'ying")
            #         await asyncio.sleep(0.05)
            #     except:
            #         pass
        except:
            
            await call.message.answer("Bazaga qo'shilmadi, xatolik ❌")
    else:
        await call.message.answer("Bazaga qo'shilmadi, bekor qilindi ❌")
    await state.finish()
    await call.message.answer("Bosh menu", reply_markup=admin_main)
    
    
#############   Jang qo'shish tugadi  ####################
    
    
    
    
    ##########################   jangni ochirish boshlandi ########################
@dp.message_handler(text="➖ Jang o'chirish", user_id=ADMINS, state="*")
async def delete_war_func(message: types.Message, state=FSMContext):
    await message.answer("Qaysi jangni o'chirib tashlamoqchisiz", reply_markup=ReplyKeyboardRemove())
    # await db.create()
    global del_tr 
    del_tr = 0
    wars = await db.select_all_wars_admin(del_tr)
    all = await db.select_all_wars()
    tr = 1
    text = f"👊 Janglar: {del_tr+1} - {del_tr+len(wars)} / {len(all)} \n\n"
    for war in wars:
        
        text += f"{tr}. {war[1]} - {war[2]} \n"
        text += f"📅 Sana: \t{war[3]}\n\n"
        tr += 1
    await message.answer(text, reply_markup=inline_wars_btn(wars))
    await state.set_state("delete_war")
    
@dp.callback_query_handler(text="back_wars",state="delete_war")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    await state.finish()
    await call.message.answer("Bosh menu", reply_markup=admin_main)
        
    
    
@dp.callback_query_handler(state="delete_war", text="forward_wars_group")
async def change_(call: CallbackQuery, state=FSMContext):
    global del_tr
    del_tr += 8
    try:
        
        
        wars = await db.select_all_wars_admin(del_tr)
        if wars:
            tr = 1
            text = f"👊 Janglar: {del_tr+1} - {del_tr+len(wars)} / {len(await db.select_all_wars())}\n\n"
            for war in wars:
                
                text += f"{tr}. {war[1]} - {war[2]} \n"
                text += f"📅 Sana: \t{war[3]}\n\n"
                tr += 1
            await call.message.delete()
            await call.message.answer(text, reply_markup=inline_wars_btn(wars))
            await state.set_state("delete_war")
        else:
            a = 'a'+4
    except Exception as err:
        del_tr -= 8
        # await call.answer()
        # await state.finish()
        await call.answer(f"Boshqa  janglar qolmadi ") 
        
        
    
@dp.callback_query_handler(state="delete_war", text="back_wars_group")
async def change_(call: CallbackQuery, state=FSMContext):
    global del_tr
    del_tr -= 8
    try:
        
        
        wars = await db.select_all_wars_admin(del_tr)
        if wars:
            tr = 1
            text = f"👊 Janglar: {del_tr+1} - {del_tr+len(wars)} / {len(await db.select_all_wars())}\n\n"
            for war in wars:
                
                text += f"{tr}. {war[1]} - {war[2]} \n"
                text += f"📅 Sana: \t{war[3]}\n\n"
                tr += 1
            await call.message.delete()
            await call.message.answer(text, reply_markup=inline_wars_btn(wars))
            await state.set_state("delete_war")
        else:
            a = 'a'+4
    except Exception as err:
        del_tr += 8
        # await call.answer()
        # await state.finish()
        await call.answer(f"Janglarni birinchi bo'limi") 
        
@dp.callback_query_handler(state="delete_war")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    id = int(call.data) 
    await state.update_data(
        {"id": id}
    )


    # await db.create()
    war = await db.select_war(id=int(id))
    
    # print(war[0])
    text = f" {war[1]} -  {war[2]} \n\n"
    text += f"📅 Sana: \t{war[3]}\n\n"
    text += f"Xaqiqatdan ham jangni ro'yxatdan ochirib tashlamoqchimisiz?"
    
    await bot.send_photo(call.from_user.id, war[4], text, reply_markup=war_check)
    await state.set_state("delete_war_check")
        
@dp.callback_query_handler(state="delete_war_check")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    if call.data == "yes_check":
        
        data = await state.get_data()
        id = data.get("id")
        # await db.create()
        await db.delete_war(int(id))
        await call.message.answer("Jang o'chirildi ✅")
            
        voices = await db.select_all_users()
        
        # print(voices)
        for user in voices:
            # print(user)
            score = await db.select_user_voice_sum(user[0])
            # print(score[0])
            if score[0]==None:
                
                await db.update_user_score(user[0], 0)
            else:
                await db.update_user_score(user[0], score[0])
    else:
        await call.message.answer("Bekor qilindi ❌")
    await delete_war_func(call.message, state)
    # await state.finish()
    ##########################   jangni ochirish tugadi ########################
    
    
    
    
    ############################   ovoz berishni yoqish va ochirish bolimi boshlandi $#########################33
@dp.message_handler(text="🔔/🔕 Ovoz berishni yoqish/o'chirish", user_id=ADMINS, state="*")
async def send_ad_to_all(message: types.Message):
    try:
        await message.answer("Ovoz berish xususiyatini o'zgartiring")
        wars = await db.select_all_wars()
        if wars[0][7] == 0:
            await message.answer("Ovoz berish to'xtatilgan 🔕.\n\nOvoz berishni yoqish uchun quidagi tugmani bosing 👇🏻", reply_markup=voice_unmute)
        else:
            await message.answer("Ovoz berish yoqilgan 🔔.\n\nOvoz berishni to'xtatish uchun quidagi tugmani bosing 👇🏻", reply_markup=voice_mute)
    except:
        await message.answer("Sizda hali birorta ham jang qo'shilmagan. Oldin jang qo'shing.", reply_markup=admin_main)
        

    
@dp.message_handler(text="🔕 Ovoz berishni to'xtatish 🔕", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    await db.update_voice_mute(0)
    await message.answer(" Ovoz berish to'xtatildi 🔕", reply_markup=admin_main)
    users = await db.select_all_users()
    for i in users:
        try:
            await bot.send_message(i[1], " Ovoz berish to'xtatildi 🔕")
            await asyncio.sleep(0.05)
        except:
            pass
    
    
@dp.message_handler(text="🔔 Ovoz berishni yoqish 🔔", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    await db.update_voice_mute(1)
    await message.answer(" Ovoz berish boshlandi 🔔", reply_markup=admin_main)
    users = await db.select_all_users()
    for i in users:
        try:
            await bot.send_message(i[1], " Ovoz berish boshlandi 🔔")
            await asyncio.sleep(0.05)
        except:
            pass
    ############################   ovoz berishni yoqish va ochirish bolimi boshlandi $#########################33
    
    
    
    
    ####################### jang hisobini o'zgartishi bo'limi boshlanishi $##################################
@dp.message_handler(text="📝 Jang hisobi", user_id=ADMINS)
async def golibni_aniqlash_wardan(message: types.Message, state=FSMContext):
    # await message.answer("Assalommu alaykum hurmatli Admin", reply_markup=admin_main)
    
    global del_tr
    del_tr = 0 
    await message.answer("Qaysi jangni hisobini o'zgartirmoqchisiz", reply_markup=ReplyKeyboardRemove())
    # await db.create()
    # wars = await db.select_all_wars()
    wars = await db.select_all_wars_admin(del_tr)
    tr = 1
    text = f"👊 Janglar: {del_tr+1} - {del_tr+len(wars)} / {len(await db.select_all_wars())}\n\n"
    for war in wars:
        if war[6]:
            win = f"✅ G'olib:  <b>{war[6]}</b>\n📝 Xisob:  {war[5]}\n"
        else:
            win = ""
        text += f"{tr}. {war[1]} -  {war[2]} \n"
        text += win
        text += f"📅 Sana: \t{war[3]}\n\n"
        tr += 1
    
    await message.answer(text, reply_markup=inline_wars_btn(wars))
    await state.set_state("change_war")
    
    
     
@dp.callback_query_handler(text="back_wars",state="change_war")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    await state.finish()
    await call.message.answer("Bosh menu", reply_markup=admin_main)
        
        
        
    
@dp.callback_query_handler(state="change_war", text="forward_wars_group")
async def change_(call: CallbackQuery, state=FSMContext):
    global del_tr
    del_tr += 8
    try:
        
        
        wars = await db.select_all_wars_admin(del_tr)
        if wars:
            tr = 1
            text = f"👊 Janglar : {del_tr+1} - {del_tr+len(wars)} / {len(await db.select_all_wars())}\n\n"
            for war in wars:
                        
                if war[6]:
                    win = f"✅ G'olib:  <b>{war[6]}</b>\n📝 Xisob:  {war[5]}\n"
                else:
                    win = ""
                text += f"{tr}. {war[1]} -  {war[2]} \n"
                text += win
                text += f"📅 Sana: \t{war[3]}\n\n"
                tr += 1
            await call.message.delete()
            await call.message.answer(text, reply_markup=inline_wars_btn(wars))
            await state.set_state("change_war")
        else:
            a = 'a'+4
    except Exception as err:
        del_tr -= 8
        # await call.answer()
        # await state.finish()
        await call.answer(f"Boshqa  janglar qolmadi ") 
        
        
    
@dp.callback_query_handler(state="change_war", text="back_wars_group")
async def change_(call: CallbackQuery, state=FSMContext):
    global del_tr
    del_tr -= 8
    try:
        
        
        wars = await db.select_all_wars_admin(del_tr)
        if wars:
            tr = 1
            text = f"👊 Janglar: {del_tr+1} - {del_tr+len(wars)} / {len(await db.select_all_wars())}\n\n"
            for war in wars:
                    
                if war[6]:
                    win = f"✅ G'olib:  <b>{war[6]}</b>\n📝 Xisob:  {war[5]}\n"
                else:
                    win = ""
                text += f"{tr}. {war[1]} -  {war[2]} \n"
                text += win
                text += f"📅 Sana: \t{war[3]}\n\n"
                tr += 1
            await call.message.delete()
            await call.message.answer(text, reply_markup=inline_wars_btn(wars))
            await state.set_state("change_war")
        else:
            a = 'a'+4
    except Exception as err:
        del_tr += 8
        # await call.answer()
        # await state.finish()
        await call.answer(f"Janglarni birinchi bo'limi") 
    
     
@dp.callback_query_handler(state="change_war")
async def golibni_aniqlash_war(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    id = int(call.data) 
    await state.update_data(
        {"id": id}
    )


    # await db.create()
    war = await db.select_war(id=int(id))
    name1 = war[1]
    name2 = war[2]
    # print(war[0])
    await state.update_data(
        {"name1": name1}
    )
    await state.update_data(
        {"name2": name2}
    )
    text = f"\n {name1}  🤜🤛🏾   {name2} \n\n"
    # text += f"📅 Sana: \t{war[3]}\n\n"
    text += f"  Kim g'olib bo'ldi "
    
    await bot.send_photo(call.from_user.id, war[4], text, reply_markup=war_winner(name1, name2))
    await state.set_state("change_war_winner")
        
        
        
@dp.callback_query_handler(text="war_cancel",state="change_war_winner")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    id = data.get("id")
    # winner = data.get("winner")
    await db.update_war_winner(id, "❌ Bekor qilindi", "❌")
    await db.update_voice_yutkazdi(id)
    await state.finish()
    
    voices = await db.select_all_users()
    
    # print(voices)
    for user in voices:
        # print(user)
        score = await db.select_user_voice_sum(user[0])
        # print(score[0])
        if score[0]==None:
            
            await db.update_user_score(user[0], 0)
        else:
            await db.update_user_score(user[0], score[0])
        # print("yangilandi", score[0])
    await call.message.answer("❌ Bekor qilindi", reply_markup=admin_main)
    # await golibni_aniqlash_wardan(call.message, state)

    # await db.update_voice_winner(id, winner)
    
@dp.callback_query_handler(text="back_wars_gr",state="change_war_winner")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    await state.finish()
    await golibni_aniqlash_wardan(call.message, state)
    
@dp.callback_query_handler(state="change_war_winner")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.edit_reply_markup()
    
    data = await state.get_data()
    name1 = data.get("name1")
    name2 = data.get("name2")
    winner = call.data
    print(winner)
    await call.message.answer(f" {winner} ✅ - g'olib")
    await state.update_data(
        {"winner": winner}
    )
    
    await call.message.answer(f"Ochkolar hisobini kiriting: \n\n {name1}   🤜🤛🏾    {name2} \n[xx-xx    :    xx-xx]")
    await state.set_state("change_war_score")

        
        
    
@dp.message_handler(state = "change_war_score", content_types="text")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    score = message.text
    
    data = await state.get_data()
    id = data.get("id")
    winner = data.get("winner")
    await db.update_war_winner(id, winner, score)
    await db.update_voice_yutkazdi(id)
    await db.update_voice_winner(id, winner)
    
    voices = await db.select_all_users()
    # print(voices)
    for user in voices:
        # print(user)
        score = await db.select_user_voice_sum(user[0])
        # print(score[0])
        if score[0]==None:
            
            await db.update_user_score(user[0], 0)
        else:
            await db.update_user_score(user[0], score[0])
        # print("yangilandi", score[0])
        # await message.answer(f"{user[1]} {score[0]}")
    
    
    await message.answer("G'olib belgilandi, foydalanuvchilarga ballar berildi ✅", reply_markup=admin_main)
    
            # users  = await db.select_all_users()
            
    for i in voices:
        try:
            await bot.send_message(i[1], "Jang xisobi belgilandi. Tahminingiz to'g'ri chiqqanidan xursandmiz, g'olibni topolmagan bo'lsangiz keyingi janglarda omad tilab qolamiz.")
            await asyncio.sleep(0.05)
        except:
            pass
    await state.finish()
    ####################### jang hisobini o'zgartishi bo'limi boshlanishi $##################################
        
    
    
    ###########################################   reyting boshlandi #################################3
@dp.message_handler(text="📊 Reyting")
async def send_ad_to_all(message: types.Message):
    raiting = await db.select_raiting()
    text = f"🔝 G'oliblarni to'g'ri topgan top 20 kishi:\n\n"
    tr = 1
    # a = []
    for i in raiting:
        user = await db.select_user(id = i[0])
       
        if user[3]:
            text += f"{tr}. @{user[3]} - {i[1]} ball\n"
        else: 
            text += f"{tr}. <a href='tg://i?id={user[1]}'> {user[2]} </a> - {i[1]} ball\n"
        tr += 1
    # print(a)
    # print(set(a))
    text += "\n 🤖 https://t.me/mixsportuz_bot"
    await message.answer(text)
    
    
@dp.message_handler(text="↔️ Qo'shimcha bo'lim", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    await message.answer("2-bo'lim amallari", reply_markup=admin_main_2)
    
    
    
    
@dp.message_handler(text="⏏️ Bosh menu", user_id=ADMINS, state="*")
async def send_ad_to_all(message: types.Message):
    await message.answer("Asosiy bo'lim amallari", reply_markup=admin_main)
    
    
    
    
@dp.message_handler(text="📣 Kanallar ro'yxati", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    await message.answer("Majburiy a'zolik kanallari")
    channels = await db.select_all_channels()
    text = "📣 Kanallar ro'yxati:\n\n"
    tr = 1
    for chanel in channels:
        text += f"📣 {tr} - {chanel[1]}\n📣 Link: {chanel[2]}\n\n"
        tr += 1
    await message.answer(text)
        
    
    
    
@dp.message_handler(text="➕ Kanal qo'shish", user_id=ADMINS)
async def send_ad_to_all(message: types.Message, state = FSMContext):
    await message.answer("Birinchi navbatda botni kanalga qo'shing.")
    await message.answer("Kanaldan biror postni forward qiling, \nyoki kanal id sini yuboring (-100....) \nyoki username sini yuboring ( misol uchun:  @mychannel )")
    await state.set_state("kanal_qoshish")
    
    
@dp.message_handler(state="kanal_qoshish", user_id=ADMINS, content_types=types.ContentTypes.ANY)
async def send_ad_to_all(message: types.Message, state = FSMContext):
    # print(message)
    try:
        if message.forward_from_chat:
            # print(message.forward_from_chat.id)
            id = message.forward_from_chat.id
            name = message.forward_from_chat.title
            chat = await bot.get_chat(id)
            invite_link = await chat.export_invite_link()
        elif message.text:
            chanel = await bot.get_chat(message.text)
            # print(chanel)
            id = chanel.id
            invite_link = await chanel.export_invite_link()
            name = chanel.full_name
        else:
            await message.answer("Nimadir xato ketti")
        
        await bot.get_chat_member(id, message.from_user.id)
        text = f"Name: {name}\n"
        text += f"Link: {invite_link}\n"
        text += f"\nQo'shildi ✅\n"
        await db.add_chanel(id, name, invite_link)
        await message.answer(text,reply_markup=admin_main_2)
    except Exception as err:
        await message.answer(f"Oldin botni kanal yoki guruhga qo'shing, so'ngra qaytadan urinib ko'ring.\n\nYoki bot linki to'g'riligiga e'tibor bering: {err}",reply_markup=admin_main_2)
    await state.finish()
        
        
        
        
    
@dp.message_handler(text="➖ Kanal o'chirish", user_id=ADMINS)
async def send_ad_to_all(message: types.Message, state = FSMContext):
    try:
        await message.answer("Majburiy a'zolik kanallari", reply_markup=ReplyKeyboardRemove())
        channels = await db.select_all_channels()
        text = "Qaysi kanallarni majburiy a'zolikdan olib tashlamoqchisiz:\n\n"
        text += "📣 Kanallar ro'yxati:\n\n"
        tr = 1
        # print(channels)
        for chanel in channels:
            text += f"📣 {tr} - {chanel[1]}\n📣 Link: {chanel[2]}\n\n"
            tr += 1
        await message.answer(text, reply_markup=inline_channel_btn(channels))
            
        
    
        await state.set_state("delete_channels")
    except:
        await message.answer("Majburiy a'zolik kanallari xatolik sodir boldi", reply_markup=admin_main_2)
        
    
     
@dp.callback_query_handler(text="back_wars",state="delete_channels")
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    await state.finish()
    await call.message.answer("Bosh menu 2", reply_markup=admin_main_2)
        
     
@dp.callback_query_handler(state="delete_channels")
async def golibni_aniqlash_war(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    try:
        
            
        chanel = await bot.get_chat(call.data)
        # print(chanel)
        id = chanel.id
        await db.delete_channel(id)
        invite_link = await chanel.export_invite_link()
        name = chanel.full_name
        

        text = f"Name: {name}\n"
        text += f"Link: {invite_link}\n"
        text += f"\nO'chirildi ✅ \n"
        
        await call.message.answer(text)   
        
    except Exception as err:
        await call.message.answer(f"Nimadur xato ketti : {err}")  
         
    await state.finish()
    await call.message.answer("Bosh menu 2", reply_markup=admin_main_2)
        ################################################################################################################################
        ################################################################################################################################
        ################################################################################################################################
        ################################################################################################################################
        ################################################################################################################################
    
    

    
    
    

@dp.message_handler(user_id=ADMINS, content_types=types.ContentTypes.TEXT)
async def check(message: types.Message):
    try:
        if message.reply_to_message:
            u_id = message.reply_to_message.entities[0].user.id
            text = message.text
            # await message.answer(u_id)
            # await message.answer(text)
            await bot.send_message(u_id, text)
            await message.answer("xabaringiz yetkazildi. ")
        else:
            pass
    except:
        await message.answer("Nimadir xato bo'ldi")