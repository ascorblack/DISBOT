from config import settings
import json
import random
import discord
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions, HelpCommand, Command
import asyncio
import time
import os
import asyncpg


#DATABASE POSTGRE
async def main():

    conn = await asyncpg.connect('postgres://ilfyoporwceozk:7ecb4b11da128e5fe2ab8cd4c033cb84d441429a7db59242df28f4e14c2d221e@ec2-54-246-115-40.eu-west-1.compute.amazonaws.com:5432/daul7ke701krm9')

    await conn.execute('''
        CREATE TABLE users(
            id serial PRIMARY KEY,
            name text,
            dob date
        )
    ''')

    await conn.execute('''
        INSERT INTO users(name, dob) VALUES($1, $2)
    ''', 'Bob', datetime.date(1984, 3, 1))

    row = await conn.fetchrow(
        'SELECT * FROM users WHERE name = $1', 'Bob')
    await conn.close()

asyncio.get_event_loop().run_until_complete(main())