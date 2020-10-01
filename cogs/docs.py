import discord
import aiohttp
from bs4 import BeautifulSoup
from discord.ext import commands
from utils import page

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


class DOCS(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="문서검색",
                      description="discord.py 문서에서 키워드로 검색을 합니다.",
                      usage=".!문서검색 [키워드]",
                      aliases=["검색", "문서", "rtfm", "ㄳ르", "문서좀읽으세요"])
    async def search_docs(self, ctx: commands.Context, *, keyword: str):
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
            return special_keyword[keyword] if keyword != "faq" else special_keyword[keyword][num]
        elif keyword in aliases.keys():
            return special_keyword[aliases[keyword]] if aliases[keyword] != "faq" else special_keyword[aliases[keyword]][num]
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


def setup(bot):
    bot.add_cog(DOCS(bot))
