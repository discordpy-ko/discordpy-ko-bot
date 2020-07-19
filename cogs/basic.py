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
        await self.bot.change_presence(activity=discord.Game(".!도움"))
        print("Bot Ready!")

    @commands.command(name="ping", aliases=["핑"])
    async def ping(self, ctx):
        text = await bot_lang.load_text("en", "ping")
        await ctx.send(str(text).format(round(int(self.bot.latency * 1000))))

    @commands.command()
    async def hellothisisverification(self, ctx):
        await ctx.send("eunwoo1104#9600 (ID: 288302173912170497)")

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed = discord.Embed(title='', description='', colour=discord.Color.red())
    # embed.add_field(name='', value='', inline=False)

    @commands.command(name="help", aliases=["도움"])
    async def help(self, ctx):
        embed = discord.Embed(title='discordpy-ko', description='프리픽스: `.!`', colour=discord.Color.gold())
        embed.add_field(name="문서검색 [키워드]", value="해당 키워드로 문서 검색을 합니다.", inline=False)
        embed.add_field(name="정보", value="봇의 정보를 보여줍니다.", inline=False)
        embed.add_field(name='DOCS', value='문서 관련 명령어를 출력합니다. 해당 명령어는 특정 서버에서 특정 유저만 사용 가능합니다.', inline=False)
        embed.add_field(name='PR', value='Pull Request 관련 명령어를 출력합니다. 해당 명령어는 특정 서버에서 특정 유저만 사용 가능합니다.', inline=False)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="정보")
    async def info(self, ctx):
        embed = discord.Embed(title="discordpy-ko 봇 정보", description="Created by [discordpy-ko](https://github.com/discordpy-ko).", colour=discord.Color.gold())
        embed.add_field(name="번역에 기여해주신 분들", value="eunwoo1104, UNKNOWN, sleepylapis, BGM, fxrcha, Minibox, 건유1019, 라고솔로가말했습니다, KokoseiJ, ArpaAP, Shio, 레이니, shilu, GPM567", inline=False)
        embed.add_field(name="추가 도움을 주신 분들", value="이준수(문서 웹사이트 글꼴)", inline=False)
        embed.add_field(name="들어가있는 서버 수", value=f"{len(self.bot.guilds)}개", inline=False)
        embed.add_field(name="추가 도움이 필요하시나요?", value="[번디파문 디스코드 서버](https://discord.gg/YbfbxpX)", inline=False)
        #embed.add_field(name="", value="", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="문서검색", aliases=["검색", "문서"])
    async def search(self, ctx, search: str):
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
        count = 1
        embed_list = []
        page_embed = embed.copy()
        for_res = result1.copy()
        for x in for_res:
            if count != 1 and count % 5 == 1:
                embed_list.append(page_embed)
                page_embed = embed.copy()
            base_link = "https://discordpy.cpbu.xyz/"
            link = base_link + x
            page_embed.add_field(name=str(count), value=f"[`{x}`]({link})", inline=False)
            result1.remove(x)
            count += 1
        embed_list.append(page_embed)
        await pager.start_page(self.bot, ctx, embed_list, embed=True)


def setup(bot):
    bot.add_cog(Basic(bot))
