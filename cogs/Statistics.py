import os
import discord
from discord.ext import commands

from utils import bot_util_dev as utils


class Statistics(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command()
    async def mean_return_1d(self, ctx, symbol: str, days_future: int, changes: float):
        file_address, number_of_events, reference_change = \
            utils.mean_return_1D(symbol=symbol, days_future=days_future, reference=changes)
        await ctx.send('{} events in the past with {:.2f}% daily changes'.format(number_of_events, changes))
        await ctx.send(file=discord.File(file_address))

    @commands.command()
    async def mean_return_kd(self, ctx, symbol: str, days_future: int, days_past: int):
        file_address, number_of_events, reference_change = \
            utils.mean_return_kD(symbol=symbol, days_future=days_future, days_past=days_past)
        await ctx.send('{} events in the past with {:.2f}% changes over the last {} days'.format(number_of_events,
                                                                                                 reference_change,
                                                                                                 days_past))
        await ctx.send(file=discord.File(file_address))


def setup(client):
    client.add_cog(Statistics(client))
