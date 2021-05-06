import os
import discord
from discord.ext import commands

from utils import bot_util as utils


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

    @commands.command()
    async def ah_stat(self, ctx, yesterday_change: float, today_change: float, intra_day_change: float, followed_by_weekend: int):
        file_address, number_of_events, mean_gain, win_chance = \
            utils.SPY_AH(yesterday_change=yesterday_change, today_change=today_change,
                         intra_day_change=intra_day_change, followed_by_weekend=followed_by_weekend)

        embed = discord.Embed(title='AH gain statistics for {}'.format('SPY'), colour=discord.Colour.green())

        embed.add_field(name='Your inputs',
                        value='Yesterday change of {:.2f}%, today change of {:.2f}%, and intra-day change of {:.2f}%'. \
                        format(yesterday_change, today_change, intra_day_change), inline=False)

        embed.add_field(name='Summary',
                        value='{} events in the past with average gain of {:.2f}% and winning chance of {}% '.\
                        format(number_of_events, mean_gain, int(win_chance*100)), inline=False)

        embed.set_image(url="attachment://"+file_address.split('/')[-1])

        embed.set_footer(icon_url=ctx.message.author.avatar_url, text='developed by {}'.format(ctx.author.name))

        await ctx.send(file=discord.File(file_address), embed=embed)




def setup(client):
    client.add_cog(Statistics(client))
