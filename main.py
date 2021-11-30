import asyncio
import os
from discord.embeds import Embed
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

n: int = 0 # current challenge

with open("count.txt", "r") as f:
  n = int(f.read())
  f.close()
 
def write_count():
  global n
  with open("count.txt", "w") as f:
    f.write(str(n))
    f.close()

TOKEN = os.getenv("DISCORD_TOKEN")

description = """A discord bot to help manage the cyber-security association Read The Docs."""

bot = commands.Bot(command_prefix='!', description=description)

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game("Hacking governments and what not"))
    print('connected!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# @bot.command()
# async def purge(ctx,where=None,  amount=100):
#   if where:
#     channel = discord.utils.get(bot.get_all_channels(), name=where)
#     await channel.purge(limit=amount)
#   else:
#     await ctx.channel.purge(limit=amount)

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

def capture_the_flag_embed(href: str, date: str) -> Embed:
  embed=discord.Embed(title="Daily Challenge", description="Here is your daily capture the flag challenge", color=0x52ff74)
  embed.set_thumbnail(url="https://capturetheflag.withgoogle.com/img/flag_logo.gif")
  embed.add_field(name="Link", value=href, inline=True)
  embed.set_footer(text=f"Ahoy - {date}")
  return embed

async def challenge():
  global n
  when: tuple = (11, 0)
  # day = 86400s
  sleep_length: int = 86400
  channel_to_send_to = "challeges"
  await bot.wait_until_ready()
  channel = discord.utils.get(bot.get_all_channels(), name=channel_to_send_to)
  while not bot.is_closed():
    now = get_time()
    if now[0] == when[0] and now[1] <= when[1]:
        link = f"https://overthewire.org/wargames/bandit/bandit{n}.html"
        date = datetime.now().date()
        embed = capture_the_flag_embed(link, date)
        await channel.send(embed=embed)
    n+=1
    write_count()
    await asyncio.sleep(sleep_length)

@bot.command()
async def send_in(ctx, where, msg):
  channel = discord.utils.get(bot.get_all_channels(), name=where)
  await channel.send(msg)

# @bot.command()
# async def demo_challenge(ctx, where, msg):
#   channel = discord.utils.get(bot.get_all_channels(), name=where)
#   await channel.send(msg)
  
# @bot.command()
# async def test_challenge(ctx):
#   link = f"https://overthewire.org/wargames/bandit/bandit{n}.html"
#   date = datetime.now().date()
#   embed = capture_the_flag_embed(link, date)
#   await ctx.send(embed=embed)
  

bot.loop.create_task(challenge())
# run the bot
bot.run(TOKEN)

# https://discord.com/login?redirect_to=%2Foauth2%2Fauthorize%3Fclient_id%3D915217765294563389%26scope%3Dbot
