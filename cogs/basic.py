import discord
import sys
import aiohttp
from discord.ext import commands
from bs4 import BeautifulSoup
import os

sys.path.append("..")
from Modules import bot_lang, pager


class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print(f'Loaded {__name__}!')

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot Ready!")

    @commands.command(aliases=["핑"])
    async def ping(self, ctx):
        text = await bot_lang.load_text("en", "ping")
        await ctx.send(str(text).format(round(int(self.bot.latency * 1000))))

    @commands.command()
    async def hellothisisverification(self, ctx):
        await ctx.send("eunwoo1104#9600 (ID: 288302173912170497)")

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed = discord.Embed(title='', description='', colour=discord.Color.red())
    # embed.add_field(name='', value='', inline=False)

    @commands.command(aliases=["도움"])
    async def help(self, ctx):
        embed = discord.Embed(title='discordpy-ko', description='Alpha | 프리픽스: `.!`', colour=discord.Color.gold())
        embed.add_field(name="문서검색 [키워드]", value="해당 키워드로 문서 검색을 합니다.", inline=False)
        embed.add_field(name='DOCS', value='문서 관련 명령어를 출력합니다. 해당 명령어는 특정 서버에서 특정 유저만 사용 가능합니다.', inline=False)
        embed.add_field(name='PR', value='Pull Request 관련 명령어를 출력합니다. 해당 명령어는 특정 서버에서 특정 유저만 사용 가능합니다.', inline=False)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def 문서검색(self, ctx, search: str):
        docs_url = "https://discordpy.cpbu.xyz/genindex.html"
        async with aiohttp.ClientSession() as session:
            async with session.get(docs_url) as res:
                text = await res.read()
        soup = BeautifulSoup(text, "html.parser")
        result1 = []
        embed = discord.Embed(title='discordpy-ko 문서 검색 결과', description=search,
                              url="https://discordpy.cpbu.xyz/search.html?q=" + search, colour=discord.Color.gold())
        for link in soup.findAll('a'):
            if search in str(link):
                result1.append(link.get('href'))
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await pager.auto_div_embed(self.bot, ctx, embed, result1)


def setup(bot):
    bot.add_cog(Basic(bot))
