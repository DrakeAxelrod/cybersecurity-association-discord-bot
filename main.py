import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from datetime import datetime
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

description = """A discord bot to help manage the cyber-security association Read The Docs."""

bot = commands.Bot(command_prefix='!', description=description)

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")

target_channel_id = 915217150493478972/915217150493478975

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game("Hacking governments and what not"))
    print('connected!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def purge(ctx,where=None,  amount=100):
  if where:
    channel = discord.utils.get(bot.get_all_channels(), name=where)
    await channel.purge(limit=amount)
  else:
    await ctx.channel.purge(limit=amount)

@bot.command()
async def whoyou(ctx):
  await ctx.send(description)
  
@bot.command()
async def time(ctx):
  now=datetime.strftime(datetime.now(),'%H:%M')
  await ctx.send(now)

def get_time():
  hour = int(datetime.now().time().strftime("%H"))
  min = int(datetime.now().time().strftime("%M"))
  return (hour, min)

s = get_time()

print(s[0])

async def challenge():
  when: tuple = (11, 00)
  # day = 86400s
  sleep_length = 10
  msg = "delayed"
  channel_to_send_to = "general"
  await bot.wait_until_ready()
  channel = discord.utils.get(bot.get_all_channels(), name=channel_to_send_to)
  while not bot.is_closed():
    now = get_time()
    if now[0] == when[0] and now[1] <= when[1]:
        await channel.send(msg)
    await asyncio.sleep(sleep_length)

bot.loop.create_task(challenge())

@bot.command()
async def get_channel(ctx, where, msg):
  channel = discord.utils.get(bot.get_all_channels(), name=where)
  await channel.send(msg)
# run the bot
bot.run(TOKEN)

# https://discord.com/login?redirect_to=%2Foauth2%2Fauthorize%3Fclient_id%3D915217765294563389%26scope%3Dbot
