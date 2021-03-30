import os
import discord
from discord.ext import commands
from datetime import timedelta, datetime
from utils import bot_util_dev as utils


class Announcements(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(name='wl', help='Shows a watchlist.')
    async def wl(self, ctx, period: str):
        embed = discord.Embed(title='{} WATCHLIST'.format(period.upper()), colour = discord.Colour.blue())
        cont = 1

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while cont:
            await ctx.send('Write "stop" to stop, otherwise enter a new WL entry as <ticker> // <message>')
            msg = await self.client.wait_for('message', check=check)
            contents = msg.content.split('/')
            print(contents)

            if contents[0] == 'stop':
                cont = 0
                pass
            else:
                embed.add_field(name='{}'.format(contents[0].upper()), value='{} '.format(contents[1]), inline=False)

        txt = msg.created_at.strftime('Today at %-I:%M %p' if ctx.message.created_at.date() == datetime.today().date()
                                      else 'Yesterday at %-I:%M %p' if ctx.message.created_at.date() == (datetime.today() - timedelta(1)).date()
                                      else '%d/%m/%Y')
        #txt = 'time stamp here'

        #embed.set_author(name=ctx.author.name, icon_url=self.client.user.avatar_url)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text='{} signal | {}'.format(ctx.author.name, txt))

        # msg.author == ctx.author and msg.channel == ctx.channel

        channel = self.client.get_channel(817862207739658282)
        if channel is not None:
            await channel.send(embed=embed)
        else:
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Announcements(client))
