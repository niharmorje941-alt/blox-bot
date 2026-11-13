from flask import Flask
import threading, os
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is alive!"
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()

import discord
from discord.ext import commands
import random, json

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# --- ECONOMY DATA ---
try:
    with open('economy.json') as f:
        eco = json.load(f)
except:
    eco = {}

def save_eco():
    with open('economy.json', 'w') as f:
        json.dump(eco, f)

def get_bal(user_id):
    if str(user_id) not in eco:
        eco[str(user_id)] = {"coins": 0, "xp": 0, "level": 1}
    return eco[str(user_id)]

@bot.event
async def on_ready():
    print(f"ONLINE: {bot.user}")
    await bot.change_presence(activity=discord.Game(name="!help | BLOX BOT"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # --- INVITE LINK BLOCK (tera purana wala) ---
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

    # --- XP SYSTEM ---
    u = get_bal(message.author.id)
    u["xp"] += 5
    if u["xp"] >= u["level"] * 100:
        u["level"] += 1
        u["xp"] = 0
        await message.channel.send(f"🎉 {message.author.mention} Level {u['level']} pe pahuch gaya! GG!")
    save_eco()

    await bot.process_commands(message)

# --- HELP ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="🤖 BLOX BOT - All Commands", color=0x00ff00)
    embed.add_field(name="📊 Info", value="`!ping` `!userinfo` `!serverinfo` `!avatar` `!rank`", inline=False)
    embed.add_field(name="🎲 Fun", value="`!meme` `!joke` `!8ball` `!coinflip` `!dice` `!roast`", inline=False)
    embed.add_field(name="💰 Economy", value="`!balance` `!daily` `!beg` `!gamble`", inline=False)
    embed.add_field(name="🛡️ Moderation", value="`!kick` `!ban` `!unban` `!timeout` `!clear` `!slowmode` `!lock` `!unlock`", inline=False)
    embed.add_field(name="⚙️ Utility", value="`!say` `!poll` `!invite`", inline=False)
    await ctx.send(embed=embed)

# --- INFO ---
@bot.command()
async def ping(ctx):
    await ctx.send(f"Bot Online hai! ✅ {round(bot.latency * 1000)}ms")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name} ka Info", color=0x3498db)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "Pata nahi")
    embed.add_field(name="Top Role", value=member.top_role.mention)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    g = ctx.guild
    embed = discord.Embed(title=f"{g.name}", color=0x9b59b6)
    embed.add_field(name="Members", value=g.member_count)
    embed.add_field(name="Channels", value=len(g.channels))
    embed.add_field(name="Owner", value=g.owner.mention if g.owner else "Pata nahi")
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.avatar.url if member.avatar else member.default_avatar.url)

@bot.command()
async def rank(ctx, member: discord.Member = None):
    member = member or ctx.author
    u = get_bal(member.id)
    await ctx.send(f"🏆 {member.mention} | Level: **{u['level']}** | XP: **{u['xp']}/{u['level']*100}** | Coins: **{u['coins']}** 🪙")

# --- FUN ---
@bot.command()
async def meme(ctx):
    memes = ["https://i.imgflip.com/9ehk.jpg", "https://i.imgflip.com/30b1gx.jpg", "https://i.imgflip.com/1bij.jpg", "https://i.imgflip.com/26am.jpg"]
    await ctx.send(random.choice(memes))

@bot.command()
async def joke(ctx):
    jokes = ["Teacher: Kal homework kyu nahi kiya? Student: Sir, WiFi ne dhoka de diya 😭", "Aloo ko pyaar hua, to wo ban gaya Aloo-lu 😂", "Wifi ka password kya hai? - Pyaar se mango, de dunga 😎"]
    await ctx.send(random.choice(jokes))

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, q=None):
    ans = ["Haan pakka!", "Bilkul nahi", "Ho sakta hai", "Mujhe nahi lagta", "100% Haan", "Bhai rehne de 😂"]
    await ctx.send(f"🎱 {random.choice(ans)}")

@bot.command()
async def coinflip(ctx):
    await ctx.send(f"🪙 {random.choice(['Heads!', 'Tails!'])}")

@bot.command()
async def dice(ctx):
    await ctx.send(f"🎲 Tumhe mila: **{random.randint(1,6)}**")

@bot.command()
async def roast(ctx, member: discord.Member = None):
    member = member or ctx.author
    roasts = ["Teri shakal dekh ke WiFi bhi disconnect ho jata hai 😂", "Tu itna slow hai, ki teri ping bhi sharma jaye", "Tera joke sunke Alexa bhi chup ho gayi"]
    await ctx.send(f"{member.mention} {random.choice(roasts)}")

# --- ECONOMY ---
@bot.command()
async def balance(ctx):
    u = get_bal(ctx.author.id)
    await ctx.send(f"💰 {ctx.author.mention} tere paas **{u['coins']}** coins hai!")

@bot.command()
async def daily(ctx):
    u = get_bal(ctx.author.id)
    u["coins"] += 500
    save_eco()
    await ctx.send(f"🎁 Daily reward! +500 coins. Ab total: {u['coins']}")

@bot.command()
async def beg(ctx):
    amt = random.randint(10, 100)
    u = get_bal(ctx.author.id)
    u["coins"] += amt
    save_eco()
    await ctx.send(f"😭 Kisi ne tujhe {amt} coins de diye! Total: {u['coins']}")

@bot.command()
async def gamble(ctx, amt: int):
    u = get_bal(ctx.author.id)
    if amt > u["coins"]:
        await ctx.send("Itne coins hai hi nahi tere paas!")
        return
    if random.choice([True, False]):
        u["coins"] += amt
        await ctx.send(f"🎉 Jeet gaya! +{amt} coins. Total: {u['coins']}")
    else:
        u["coins"] -= amt
        await ctx.send(f"💀 Haar gaya! -{amt} coins. Total: {u['coins']}")
    save_eco()

# --- MODERATION ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} kick ho gaya!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} ban ho gaya!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, name):
    bans = await ctx.guild.bans()
    for b in bans:
        if b.user.name == name:
            await ctx.guild.unban(b.user)
            await ctx.send(f"✅ {name} unban ho gaya!")
            return
    await ctx.send("Ye banda ban list me nahi hai!")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int = 5):
    await member.timeout(discord.utils.utcnow() + discord.timedelta(minutes=minutes))
    await ctx.send(f"⏰ {member.mention} ko {minutes} min ke liye timeout!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amt: int = 10):
    await ctx.channel.purge(limit=amt+1)
    await ctx.send(f"🧹 {amt} messages delete kar diye!", delete_after=3)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, sec: int = 0):
    await ctx.channel.edit(slowmode_delay=sec)
    await ctx.send(f"🐢 Slowmode {sec} sec pe set!")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Channel lock!")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Channel unlock!")

# --- UTILITY ---
@bot.command()
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send(msg)

@bot.command()
async def poll(ctx, *, q):
    msg = await ctx.send(f"📊 **Poll:** {q}\n👍 = Haan | 👎 = Nahi")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command()
async def invite(ctx):
    await ctx.send(f"Bot ko add karne ke liye: https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot")

bot.run(os.getenv("TOKEN"))
