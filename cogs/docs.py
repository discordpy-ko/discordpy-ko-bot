import discord
import aiohttp
import asyncio
import github
import json
from bs4 import BeautifulSoup
from discord.ext import commands
from utils import page
from utils import build

special_keyword = {
    "python": "https://docs.python.org/ko/3/",
    "coroutine": "https://docs.python.org/ko/3/library/asyncio-task.html#coroutine",
    "faq": ["https://discordpy.cpbu.xyz/faq.html", "https://discordpy.cpbu.xyz/neo-docs/faq.html"]
}

aliases = {
    "파이썬": "python",
    "py": "python",
    "코루틴": "coroutine",
    "coro": "coroutine"
}

loop = asyncio.get_event_loop()


class DOCS(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="문서검색",
                      description="discord.py 문서에서 키워드로 검색을 합니다.",
                      usage="`.!문서검색 [키워드]`",
                      aliases=["검색", "문서", "rtfm", "ㄳ르", "문서좀읽으세요"])
    async def search_docs(self, ctx: commands.Context, *, keyword: str = None):
        if keyword is None:
            embed = discord.Embed(title="discord.py 번역 문서 링크",
                                  description="[1.5.0a 문서](https://discordpy.cpbu.xyz/)\n"
                                              "[neo 문서](https://discordpy.cpbu.xyz/neo-docs/)",
                                  color=discord.Color.gold())
            return await ctx.send(embed=embed)
        docs_url = "https://discordpy.cpbu.xyz/genindex.html"
        base_url = "https://discordpy.cpbu.xyz/search.html?q="
        base_link = "https://discordpy.cpbu.xyz/"
        num = 0
        if keyword.startswith("-neo "):
            keyword = keyword.replace("-neo ", "")
            docs_url = "https://discordpy.cpbu.xyz/neo-docs/genindex.html"
            base_url = "https://discordpy.cpbu.xyz/neo-docs/search.html?q="
            base_link = "https://discordpy.cpbu.xyz/neo-docs/"
            num = 1
        if keyword in special_keyword.keys():
            return await ctx.send(special_keyword[keyword] if keyword != "faq" else special_keyword[keyword][num])
        elif keyword in aliases.keys():
            return await ctx.send(special_keyword[aliases[keyword]] if aliases[keyword] != "faq" else special_keyword[aliases[keyword]][num])
        async with aiohttp.ClientSession() as session:
            async with session.get(docs_url) as res:
                text = await res.read()
        soup = BeautifulSoup(text, "html.parser")
        result1 = []
        embed = discord.Embed(title='discordpy-ko 문서 검색 결과',
                              description=keyword,
                              url=base_url + keyword,
                              colour=discord.Color.gold())
        for link in soup.findAll('a'):
            if keyword in str(link):
                result1.append(link.get('href'))
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        count = 1
        embed_list = []
        page_embed = embed.copy()
        for_res = result1.copy()
        if len(result1) == 0:
            return await ctx.send("검색 결과가 없습니다.")
        for x in for_res:
            if count != 1 and count % 5 == 1:
                embed_list.append(page_embed)
                page_embed = embed.copy()
            link = base_link + x
            page_embed.add_field(name=str(count), value=f"[`{x.split('#')[1]}`]({link})", inline=False)
            result1.remove(x)
            count += 1
        embed_list.append(page_embed)
        await page.start_page(self.bot, ctx, embed_list, embed=True)

    @commands.group(name="DOCS", description="문서 업데이트 관련 명령어입니다.", usage="`.!DOCS [서브커맨드]`", aliases=["docs"])
    async def docs(self, ctx: commands.Context):
        if 704236010736713858 not in [x.id for x in (await self.bot.get_guild(704227416951881790).fetch_member(ctx.author.id)).roles]:
            return await ctx.send("권한이 없습니다. 해당 명령어는 `번디파문` 서버에서 `기여자` 역할을 갖고 있어야 사용이 가능합니다.")
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='DOCS 명령어', colour=discord.Color.gold())
            embed.add_field(name='DOCS 업데이트', value='문서를 업데이트합니다. (소요시간: 1 ~ 2분)', inline=False)
            embed.add_field(name='DOCS 유저초대', value='관리자 전용', inline=False)
            await ctx.send(embed=embed)

    @docs.command(name="유저초대")
    async def invite_user(self, ctx: commands.Context, name: str):
        if not ctx.author.id == 288302173912170497:
            return

        with open('bot_settings.json', 'r', encoding="UTF-8") as f:
            bot_settings = json.load(f)
        g = github.Github(bot_settings["github_token"])
        user_got = g.search_users(name + "in:login")[0]
        embed = discord.Embed(title='GitHub 유저정보', description=user_got.login, colour=discord.Color.gold(),
                              url=user_got.html_url)
        await ctx.send(embed=embed)

        msg = await ctx.send("정말로 이 유저를 초대할까요?")
        [await msg.add_reaction(x) for x in ["⭕", "❌"]]

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '⭕'

        try:
            await self.bot.wait_for('reaction_add', timeout=60, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("시간이 초과됬습니다.")
        org = g.get_organization("discordpy-ko")
        org.invite_user(user=user_got)
        await ctx.send(f"`{user_got.login}`님을 초대했어요!")

    @docs.command(name="업데이트", aliases=["update", "UPDATE"])
    async def update(self, ctx: commands.Context, msg: str = None):
        msg = f"Updated by {ctx.author.name}" if msg is None else msg
        await loop.run_in_executor(None, build.build_docs, msg)
        await ctx.send(file=discord.File("build_log.txt"))


def setup(bot):
    bot.add_cog(DOCS(bot))
