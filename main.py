from flask import Flask
import threading, os
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is alive!"
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ONLINE: {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Bot Online hai! ✅ {round(bot.latency * 1000)}ms")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "discord.gg/" in message.content or "discord.com/invite/" in message.content:
        if message.author.guild_permissions.administrator:
            await bot.process_commands(message)
            return
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Invite link allowed nahi hai! ❌")
        except:
            pass
        return

    await bot.process_commands(message)

bot.run(os.getenv("TOKEN"))
