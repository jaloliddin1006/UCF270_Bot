import asyncio

from utils.db_api.postgresql import Database


async def test():
    db = Database()
    await db.create()

    # print("Users jadvalini yaratamiz...")
    # await db.drop_users()
    # await db.create_table_users()
    # print("Yaratildi")

    # print("Foydalanuvchilarni qo'shamiz")

    await db.add_user(122654789, "Jonibek 2", "@Yorqulov", 123456789)
    await db.add_user(868486454, "Ochil", "", 868486454)
    await db.add_user(544844848, "Jaloliddin 2", "@Mamatmusayev", 0)
    await db.add_user(454566321, "Fozil 2", "@Qorshiyev", 0)
    await db.add_user(455326321, "Fozil 3", "@Qorshiyev 999", 544844848)
    await db.add_user(455588321, "Fozil 4", "@Qorshiyev777", 123456789)
    
    
    
    
    
    await db.add_war("jangchi 1", "jangchi 2", "17-01-2022", "AgACAgIAAxkBAAIMq2PdDBYO94ZEdsHHHL7lFEy5Vx86AALBwzEbsEnpSrmSdcMPGPPcAQADAgADeAADLgQ")
    await db.add_war("jangchi 3", "jangchi 4", "18-01-2022", "AgACAgIAAxkBAAIMq2PdDBYO94ZEdsHHHL7lFEy5Vx86AALBwzEbsEnpSrmSdcMPGPPcAQADAgADeAADLgQ")
    await db.add_war("jangchi 5", "jangchi 6", "19-01-2022", "AgACAgIAAxkBAAIMq2PdDBYO94ZEdsHHHL7lFEy5Vx86AALBwzEbsEnpSrmSdcMPGPPcAQADAgADeAADLgQ")
    
    
    
    await db.add_voice(1, 1, "jangchi 1")
    await db.add_voice(1, 2, "jangchi 4")
    await db.add_voice(1, 3, "jangchi 5")
    await db.add_voice(2, 1, "jangchi 1")
    await db.add_voice(2, 3, "jangchi 6")
    await db.add_voice(3, 1, "jangchi 1")
    await db.add_voice(2, 2, "jangchi 4")
    await db.add_voice(3, 3, "jangchi 5")
    
    
    print("Qo'shildi")

    users = await db.select_all_users()
    print(f"Barcha foydalanuvchilar: {users}")

    user = await db.select_user(id=5)
    print(f"Foydalanuvchi: {user}")


asyncio.run(test())
