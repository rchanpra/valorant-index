import discord
import mysql.connector
import os
from dotenv import load_dotenv

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="valorant"
)
dbcursor = db.cursor()

PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is online')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
#    print(f'{message.author} said "{message.content}" in #{message.channel}')
    
    if message.content.startswith(PREFIX + 'weapon'):
        weapon = message.content.split()[1]
        dbcursor.execute("SELECT name, category, cost, fire_rate, magazine_size, reload_time FROM weapons WHERE name=%s",[weapon])
        data = dbcursor.fetchone()
        msg = "Name: " + data[0] + "\nCategory: " + data[1] + "\nCost: " + str(data[2]) + "\nFire Rate: " + str(data[3]) + "\nMagazine Size: " + str(data[4]) + "\nReload Time: " + str(data[5])
        await message.channel.send(msg)

load_dotenv()
client.run(os.getenv('TOKEN'))