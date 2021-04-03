import os
import discord
from discord.ext import commands
from datetime import timedelta, datetime
from utils import bot_util as utils


class Announcements(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(name='roi', help='Shows return of investments.')
    async def roi(self, ctx):
        embed = discord.Embed(title='RECAP    {}'.format(ctx.message.created_at.strftime('%d/%m/%Y')), colour=discord.Colour.green())
        cont = 1
        roi = 0

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while cont:
            await ctx.send('Write "stop" to stop, otherwise enter a new ROI entry as <ticker> / <buy> / <sell>')
            msg = await self.client.wait_for('message', check=check)
            contents = msg.content.split('/')

            if contents[0] == 'stop':
                cont = 0
                pass
            else:
                embed.add_field(name='{}'.format(contents[0].upper()),
                                value='{} -> {} = {:.1f} %'.format(contents[1], contents[2], 100*(float(contents[2])/float(contents[1]) - 1)),
                                inline=False)
                roi += 100*(float(contents[2])/float(contents[1]) - 1)

        embed.add_field(name='Total ROI = {:.2f}%'.format(roi), value=' \a', inline=False)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text='{} signal'.format(ctx.author.name))

        channel = self.client.get_channel(810198440226062436)
        if channel:
            await channel.send(embed=embed)
        else:
            await ctx.send(embed=embed)

    @commands.command(name='mywl', help='Shows your watchlist.')
    async def mywl(self, ctx, period: str):
        embed = discord.Embed(title='{} WATCHLIST'.format(period.upper()), colour=discord.Colour.blue())
        cont = 1
        count, accuracy = 0, 0


        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while cont:
            await ctx.send('Write "stop" to stop, otherwise enter a new WL entry as <ticker> / <message>')
            msg = await self.client.wait_for('message', check=check)
            contents = msg.content.split('/')

            if contents[0] == 'stop':
                cont = 0
                pass
            else:
                embed.add_field(name='{}'.format(contents[0].upper()), value='{} '.format(contents[1]), inline=False)

        embed.timestamp = datetime.utcnow()
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text='{} signalc'.format(ctx.author.name))

        ## it should be replaced with a channel ID of this server
        channel = self.client.get_channel(817862207739658282)
        if channel:            # if channel is exist
            await channel.send(embed=embed)
        else:
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Announcements(client))
