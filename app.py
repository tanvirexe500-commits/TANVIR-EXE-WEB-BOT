import discord
from discord.ext import commands
import requests
import firebase_admin
from firebase_admin import credentials, db
import time
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def get_config():
    try:
        response = requests.get("https://pastebin.com/raw/J9YMj5px", timeout=10)
        lines = response.text.strip().split('\n')
        return lines[0].strip(), int(lines[1].strip())
    except:
        return None, None

BOT_TOKEN, TARGET_CHANNEL_ID = get_config()

cred = credentials.Certificate("service-account.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://uid-admin-panel-default-rtdb.firebaseio.com/'
})

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

FIREBASE_REF = db.reference("uids")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if not TARGET_CHANNEL_ID or message.author == bot.user or message.channel.id != TARGET_CHANNEL_ID:
        return

    msg_content = message.content.strip()
    uid = None

    if msg_content.startswith('!free '):
        parts = msg_content.split(' ')
        if len(parts) > 1:
            uid = parts[1]
    elif msg_content.isdigit():
        uid = msg_content

    if uid and 9 <= len(uid) <= 15:
        days = 2
        api_url = f"http://187.77.151.220:6012/uid?add={uid}&days={days}"
        
        try:
            requests.get(api_url, timeout=5)
            expiry_time = int(time.time() * 1000) + (days * 24 * 60 * 60 * 1000)
            FIREBASE_REF.child(uid).set({
                "uid": uid,
                "days": str(days),
                "expiryTime": expiry_time
            })

            embed = discord.Embed(title="🚀 FREE ACCESS GRANTED", color=0x3498db)
            if bot.user.avatar:
                embed.set_thumbnail(url=bot.user.avatar.url)
            
            embed.add_field(name="👤 UID", value=f"`{uid}`", inline=True)
            embed.add_field(name="⌛ Limit", value="`48H`", inline=True)
            embed.add_field(name="🗓️ Status", value="`✅ Successfully Added`", inline=False)
            
            await message.channel.send(embed=embed)
        except:
            pass

    await bot.process_commands(message)

if BOT_TOKEN:
    keep_alive()
    bot.run(BOT_TOKEN)
