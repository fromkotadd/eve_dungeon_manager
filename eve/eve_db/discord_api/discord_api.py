import discord
from discord.ext import commands
from table2ascii import table2ascii, PresetStyle

from eve_db.discord_api import config
from eve_db.representors.representors import pilot_info_table_queryset

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)  # инициализируем бота с префиксом '~'
ID_CHANNEL = config.config['ID_CHANNEL']


@bot.command()
async def ida(ctx):
	author = ctx.message.author
	await ctx.send(author.id)  # выводит в чат id автора сообщения
	await ctx.send(author.mention)  # выводит в чат имя автора сообщения


@bot.command()
async def foo(ctx):
	pilot_cards = await pilot_info_table_queryset()

	for pilot_card in pilot_cards:
		embed = discord.Embed(color=discord.Color.green())
		embed.add_field(name='name', value=pilot_card['name'], inline=True)
		embed.add_field(name='corporation', value=pilot_card['corporation'], inline=True)
		embed.add_field(name='tech_level', value=pilot_card['tech_level'], inline=True)
		embed.add_field(name='pilot_rating', value=pilot_card['pilot_rating'], inline=True)
		embed.add_field(name='dungeon_visits_amount', value=pilot_card['dungeon_visits_amount'], inline=True)
		embed.add_field(name='skills_rating', value=pilot_card['skills_rating'], inline=True)
		await ctx.channel.send(embed=embed)


@bot.command()
async def test(ctx):
	pilots_cards = await pilot_info_table_queryset()
	for pilots_card in pilots_cards:
		output = table2ascii(
			header=['ИМЯ', 'КОРПА', 'ТЕХ.УР.', 'РЕЙТИНГ', 'ПРОХОДКИ', 'СРЕДНИЙ.УР.СКИЛЛОВ'],
			body=[
				[
					pilots_card['name'],
					pilots_card['corporation'],
					pilots_card['tech_level'],
					pilots_card['pilot_rating'],
					pilots_card['dungeon_visits_amount'],
					pilots_card['skills_rating']
				]
			],
			style=PresetStyle.plain
		)
		embed = discord.Embed(color=discord.Color.green(), description=output)
		await ctx.channel.send(f"```\n{output}\n```")

@bot.command()
async def t(ctx, arg1='so', arg2='so'):
	await ctx.send(f'You passed {arg1} and {arg2}')
def run():
	bot.run(config.config['TOKEN'])
