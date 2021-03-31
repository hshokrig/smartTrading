import discord
from discord.ext import commands
from utils import bot_util as utils


class Screener(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(name='eh_price', help='Price changes in the extended hours')
    async def eh_price(self, ctx, *, symbols: str):
        symbols_list = symbols.split()
        print(symbols_list)

        str = utils.EH_change(symbols_list[0])
        if str[0] == 'pre':
            embed = discord.Embed(title='Premarket prices')
        else:
            embed = discord.Embed(title='Afterhour prices')

        for symbol in symbols_list:
            outputs = utils.EH_change(symbol)
            embed.add_field(name='{}          \a'.format(symbol.upper()), value=outputs[1], inline=True)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Screener(client))
