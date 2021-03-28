import discord
from discord.ext import commands
import random


class Initialization(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        client = self.client
        await client.change_presence(activity=discord.Game(name='with the API'))
        print('We have logged in as {0.user}'.format(client))


    # Commands
    @commands.command()
    async def alive(self, ctx):
        messages = ['I am working!', 'Still working!', 'Really?', 'Still on, just back off!']
        response = random.choice(messages)
        await ctx.send(response)


def setup(client):
    client.add_cog(Initialization(client))
