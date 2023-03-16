import discord
from discord.ext import commands
from table2ascii import table2ascii, PresetStyle

from eve_db.discord_api import config
from eve_db.representors.representors import pilot_info_table_queryset
from eve_db.representors.representors import registration_pilot

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)  # инициализируем бота с префиксом '~'
ID_CHANNEL = config.config['ID_CHANNEL']


@bot.command()
async def ida(ctx):
	author = ctx.message.author
	await ctx.send(author.id)  # выводит в чат id автора сообщения
	await ctx.send(author.mention)  # выводит в чат имя автора сообщения


@bot.command()
async def registration(ctx,  name, corporation, tech_level, pilot_rating):
	discord_id = ctx.message.author.id
	await registration_pilot(discord_id=discord_id,
					   name=name,
					   corporation=corporation,
					   tech_level=tech_level,
					   pilot_rating=pilot_rating)


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
async def test(ctx, pilots_amount=20, implant_level=15, skills_rating=2, gun_rating=2):
	pilots_cards = await pilot_info_table_queryset(pilots_amount, implant_level, skills_rating, gun_rating)
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
		await ctx.channel.send(f"```\n{output}\n```")

def run():
	bot.run(config.config['TOKEN'])
