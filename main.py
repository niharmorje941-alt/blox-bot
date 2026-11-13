import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"ONLINE: {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! Bot online hai!")

@bot.command()
async def ball(ctx, *, question=None):
    answers = ["Haan pakka!", "Nahi bhai kabhi nahi", "Maybe...", "100% Yes!", "Bilkul nahi"]
    await ctx.send(f"🎱 {random.choice(answers)}")

@bot.command()
async def dance(ctx):
    await ctx.send(f"{ctx.author.mention} is dancing! 🕺 https://media.tenor.com/1b8p9Z6r1XcAAAAC/dance.gif")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} ko kick kar diya!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} ko ban kar diya!")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f"✅ {member.mention} ko {role.name} de diya!")
    else:
        await ctx.send("Ye role mila hi nahi!")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unrole(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.remove_roles(role)
        await ctx.send(f"❌ {member.mention} se {role.name} hata diya!")

@bot.command()
async def owner(ctx):
    await ctx.send(f"👑 Owner hai: {ctx.guild.owner.mention}")

@bot.command()
async def coowner(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Co-Owner")
    if role and role.members:
        await ctx.send(f"👑 Co-Owner: {', '.join([m.mention for m in role.members])}")
    else:
        await ctx.send("Abhi koi Co-Owner nahi hai!")

@bot.command()
@commands.has_permissions(administrator=True)
async def op(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="OP")
    if not role:
        role = await ctx.guild.create_role(name="OP", permissions=discord.Permissions(administrator=True))
    await member.add_roles(role)
    await ctx.send(f"⚡ {member.mention} ab OP hai!")

bot.run(os.getenv("TOKEN"))
