import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import utils.bot_util as util

load_dotenv()
#TOKEN_dev = os.getenv('DISCORD_TOKEN_DEV')
TOKEN = os.getenv('DISCORD_TOKEN')
path = os.getenv('DISCORD_PATH')
print(path)

client = commands.Bot(command_prefix='..')


@client.command(name='load', help='Load a cog')
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print('load worked')
    await ctx.send(f'Cog {extension} has been loaded. Try help to see all the new commands.')


@client.command(name='unload', help='Unload a cog')
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Cog {extension} has been unloaded.')


@client.command(name='reload', help='Reload a cog')
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


for filename in os.listdir(path+'/cogs'):
    if filename.endswith('.py') and filename != '__init__.py':
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(TOKEN)