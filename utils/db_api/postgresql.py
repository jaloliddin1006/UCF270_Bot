from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config
##### drop tableda cascade 
class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id BIGSERIAL PRIMARY KEY,
        tg_id BIGINT NOT NULL UNIQUE, 
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        by_whom BIGINT,
        score BIGINT
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_ufc(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Ufcwar (
        id BIGSERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        second_name VARCHAR(255) NOT NULL,
        war_date VARCHAR(255) NOT NULL,
        photo VARCHAR(555) NOT NULL,
        score VARCHAR(155),
        winner VARCHAR(255),
        voice_start BIGINT
        
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_voice(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Voice (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES Users(id) ON DELETE CASCADE NOT NULL,
        war_id BIGINT REFERENCES Ufcwar(id) ON DELETE CASCADE NOT NULL,
        winner VARCHAR(255) NOT NULL,
        score BIGINT
       
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_channels(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Channels (
        channel_id BIGSERIAL PRIMARY KEY,
        channel_name VARCHAR(255) NOT NULL,
        channel_link VARCHAR(255) NOT NULL
       
        );
        """
        await self.execute(sql, execute=True)
        
        
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, tg_id, full_name, username, by_whom):
        sql = "INSERT INTO users (tg_id, full_name, username, by_whom, score) VALUES($1, $2, $3, $4, 0) returning *"
        return await self.execute(sql, tg_id, full_name, username, by_whom, fetchrow=True)

    async def add_war(self, first_name, second_name, war_date, photo):
        sql = "INSERT INTO Ufcwar (first_name, second_name, war_date, photo, voice_start) VALUES($1, $2, $3, $4, 0) returning *"
        return await self.execute(sql, first_name, second_name, war_date, photo, fetchrow=True)

    async def add_voice(self, user_id, war_id, winner):
        sql = "INSERT INTO Voice (user_id, war_id, winner, score) VALUES($1, $2, $3, 0) returning *"
        return await self.execute(sql, user_id, war_id, winner, fetchrow=True)

    async def add_chanel(self, chanel_id, chanel_name, chanel_link):
        sql = "INSERT INTO Channels (channel_id, channel_name, channel_link) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, chanel_id, chanel_name, chanel_link, fetchrow=True)

    async def select_all_wars(self):
        sql = "SELECT * FROM Ufcwar ORDER BY id"
        return await self.execute(sql, fetch=True)
    
    async def select_all_wars_admin(self, lim):
        sql = f"SELECT * FROM Ufcwar  ORDER BY id OFFSET {lim} FETCH FIRST 8 ROW ONLY"
        return await self.execute(sql, fetch=True)
    
    async def select_all_wars_v(self, lim):
        sql = f"SELECT * FROM Ufcwar WHERE winner IS NULL ORDER BY id OFFSET {lim} FETCH FIRST 5 ROW ONLY"
        return await self.execute(sql, fetch=True)
    
    async def select_war(self, id):
        sql = f"SELECT * FROM Ufcwar WHERE id = {id}"
        return await self.execute(sql, fetchrow=True)
    
    async def select_voice(self, user_id, war_id):
        sql = f"SELECT * FROM Voice WHERE user_id = {user_id} AND war_id = {war_id}"
        return await self.execute(sql, fetchrow=True)
    
    async def select_check_user_voice(self, user_id, war_id):
        sql = f"SELECT * FROM users LEFT JOIN voice ON voice.user_id = users.id WHERE users.tg_id = {user_id} AND voice.war_id = {war_id}"
        return await self.execute(sql, fetchrow=True)
    
    async def select_user_voice(self, user_id):
        sql = f"SELECT * FROM users LEFT JOIN voice ON voice.user_id = users.id WHERE users.tg_id = {user_id} "
        return await self.execute(sql, fetch=True)
    
    async def select_all_voice(self):
        sql = f"SELECT * FROM Voice"
        return await self.execute(sql, fetch=True)
    
    async def select_user_voice_sum(self, id):
        sql = f"SELECT SUM(score) FROM Voice  WHERE user_id = {id}"
        return await self.execute(sql, fetchrow=True)
    
    
    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_channels(self):
        sql = "SELECT * FROM Channels"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_raiting(self):
        sql = f"SELECT  user_id, SUM(score), MIN(id) FROM voice GROUP BY user_id ORDER BY sum, min limit 20"
        return await self.execute(sql, fetch=True)
    
#  select * from users order by score desc limit 5
    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_voice_mute(self, check):
        sql = "UPDATE Ufcwar SET voice_start=$1 "
        return await self.execute(sql, check, execute=True)
    
    async def update_war_winner(self,war, winner, score):
        sql = "UPDATE Ufcwar SET winner=$1, score=$2 WHERE id=$3"
        return await self.execute(sql, winner, score, war, execute=True)
    
    async def update_user_voice(self,u_id, war_id, winner):
        sql = "UPDATE Voice SET winner=$1 WHERE user_id=$2, war_id=$3"
        return await self.execute(sql, winner, u_id, war_id, execute=True)
    
    async def update_voice_winner(self,war, winner):
        sql = "UPDATE Voice SET  score=5 WHERE winner=$1 AND war_id=$2  "
        return await self.execute(sql, winner, war, execute=True)

    async def update_voice_yutkazdi(self,war):
        sql = "UPDATE Voice SET  score=0 WHERE war_id=$1  "
        return await self.execute(sql, war, execute=True)

    async def update_user_score(self,id, score):
        sql = "UPDATE Users SET  score=$1 WHERE id=$2  "
        return await self.execute(sql, score, id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_user_voice(self,u_id, war_id ):
        await self.execute(f"DELETE FROM Voice WHERE user_id =$1 AND war_id=$2",u_id, war_id, execute=True)
    
    
    async def delete_wars(self):
        await self.execute("DELETE FROM Voice WHERE TRUE", execute=True)
        await self.execute("DELETE FROM Ufcwar WHERE TRUE", execute=True)

    async def delete_war(self, id ):
        await self.execute(f"DELETE FROM Ufcwar WHERE id =$1",id, execute=True)
    

    async def drop_wars(self):
        await self.execute("DROP TABLE Ufcwar", execute=True)

    async def delete_channel(self, id ):
        await self.execute(f"DELETE FROM Channels WHERE channel_id =$1",id, execute=True)
        # print("okkkkk ochirildi------------", id)
    async def delete_channels(self):
        await self.execute(f"DELETE FROM Channels WHERE TRUE", execute=True)
        # print("okkkkk ochirildi------------", id)
    

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)