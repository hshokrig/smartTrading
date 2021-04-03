import discord
from discord.ext import commands
from utils import bot_util as utils
import json

class Screener(commands.Cog):

    def __init__(self, client):
        self.client = client

        root_dir = utils.get_root_dir()
        with open('{}/src/Watchlists.json'.format(root_dir)) as json_file:
            self.wl = json.load(json_file)

        with open('{}/src/Sympathy_plays.json'.format(root_dir)) as json_file:
            self.sympathy = json.load(json_file)

    # Events

    # Commands
    @commands.command(name='price', help='Price changes in the extended hours')
    async def price(self, ctx, *, symbols: str):
        symbols_list = symbols.split()
        print(symbols_list)

        market_hour, price_change = utils.get_price(symbols_list[0])
        if market_hour == 'pre':
            embed = discord.Embed(title='Premarket price changes', colour=discord.Colour.light_gray())
        elif market_hour == 'after':
            embed = discord.Embed(title='Afterhour price changes', colour=discord.Colour.light_gray())
        elif market_hour == 'RH':
            embed = discord.Embed(title='Market price changes', colour=discord.Colour.light_gray())

        for symbol in symbols_list:
            _, price_change = utils.get_price(symbol)
            embed.add_field(name='{}          \a'.format(symbol.upper()), value=price_change, inline=True)

        await ctx.send(embed=embed)


    @commands.command(name='wl', help='Price changes of a watchlist')
    async def wl(self, ctx, *, wl_name: str):
        exist = 0
        for wl in self.wl:      #iterate on all watchlists
            if wl_name.lower() in self.wl[wl]['names']:
                exist = 1
                prices = dict.fromkeys(self.wl[wl]['symbols'])
                for ticker in self.wl[wl]['symbols']:
                    try:
                        market_hour, prices[ticker] = utils.get_price(ticker)
                    except:
                        market_hour, prices[ticker] = 'RH', 'n/a'

        if exist == 0:
            await ctx.send('I do not have watchlist {}'.format(wl_name.upper()))
        else:
            if market_hour == 'pre':
                embed = discord.Embed(title='Watchlist {} in premarket'.format(wl_name.upper()), colour=discord.Colour.light_gray())
            elif market_hour == 'after':
                embed = discord.Embed(title='Watchlist {} in after hours'.format(wl_name.upper()), colour=discord.Colour.light_gray())
            else:
                embed = discord.Embed(title='Watchlist {} in market hours'.format(wl_name.upper()), colour=discord.Colour.light_gray())

        for ticker in list(prices.keys()):
            embed.add_field(name='{}          \a'.format(ticker.upper()), value=prices[ticker], inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='sympathy', help='Find sympathy plays')
    async def sympathy(self, ctx, *, symbol: str):
        exist = 0
        if symbol.upper() in self.sympathy:
            exist = 1
            prices = dict.fromkeys(self.sympathy[symbol.upper()])
            for ticker in self.sympathy[symbol.upper()]:
                market_hour, prices[ticker] = utils.get_price(ticker)

        if exist == 0:
            await ctx.send('I do not have any sympathy play for {}'.format(symbol.upper()))
        else:
            if market_hour == 'pre':
                embed = discord.Embed(title='Sympathy plays for {} in premarket'.format(symbol.upper()), colour=discord.Colour.light_gray())
            elif market_hour == 'after':
                embed = discord.Embed(title='Sympathy plays for {} in after hours'.format(symbol.upper()), colour=discord.Colour.light_gray())
            else:
                embed = discord.Embed(title='Sympathy plays for {} in market hours'.format(symbol.upper()), colour=discord.Colour.light_gray())

        for ticker in list(prices.keys()):
            embed.add_field(name='{}          \a'.format(ticker.upper()), value=prices[ticker], inline=True)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Screener(client))
