import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
import bot_util


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='..')

@bot.command(name='alive', help='Sends a radom response')
async def random_quote(ctx):
    messages = ['I am working!', 'Still working!', 'Really?', 'Still on, just back off!']

    response = random.choice(messages)
    await ctx.send(response)

@bot.command(name='roll_dice', help='Simulates rolling dice. roll number of dices number of sides.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='prod', help='Simulates rolling dice.')
async def prod(ctx, number_1: int, number_2: int):
    await ctx.send(number_1*number_2)

@bot.command(name='mean_return_1D', help='Simulates rolling dice.')
async def mean_return_1D(ctx, symbol: str, days_future: int, changes: float):
    file_address, number_of_events, reference_change = \
        bot_util.mean_return_1D(symbol=symbol, days_future=days_future, reference=changes)

    await ctx.send('{} events in the past with {:.2f}% daily changes'.format(number_of_events, changes))
    await ctx.send(file=discord.File(file_address))

@bot.command(name='mean_return_kD', help='Simulates rolling dice.')
async def mean_return_kD(ctx, symbol: str, days_future: int, days_past: int):
    file_address, number_of_events, reference_change = \
        bot_util.mean_return_kD(symbol=symbol, days_future=days_future, days_past=days_past)

    await ctx.send('{} events in the past with {:.2f}% changes over the last {} days'.format(number_of_events, reference_change, days_past))
    await ctx.send(file=discord.File(file_address))

bot.run(TOKEN)