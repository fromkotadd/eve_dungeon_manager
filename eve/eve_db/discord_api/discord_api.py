import discord
from discord.ext import commands
import threading

from eve_db.discord_api import config
from eve_db.representors.representors import pilot_info_table

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)  # инициализируем бота с префиксом '!'
ID_CHANNEL = config.config['ID_CHANNEL']

# s = pilot_info_table()
@bot.command()
async def ida(ctx):
	author = ctx.message.author
	await ctx.send(author.id)  # выводит в чат id автора сообщения
	await ctx.send(author.mention)  # выводит в чат имя автора сообщения


@bot.command()
async def first(ctx):
	# channel = bot.get_channel(ID_CHANNEL)
	channel = ctx.channel
	await channel.send(pilot_info_table())


def run():
	bot.run(config.config['TOKEN'])
