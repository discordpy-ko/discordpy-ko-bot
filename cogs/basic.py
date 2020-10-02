import discord
from discord.ext import commands


class Basic(commands.Cog):
    """
    매우 기본적인 명령어들이 있는 Cog 입니다.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="핑", description="매우 기본적인 핑 명령어입니다.", aliases=["ping", "vld", "ㅔㅑㅜㅎ"])
    async def ping(self, ctx: commands.Context):
        """
        매우 기본적인 핑 명령어입니다.
        """
        await ctx.send(f":ping_pong: 퐁! ({round(self.bot.latency * 1000)}ms)")

    @commands.command(name="크레딧", description="문서 번역에 기여해주신 분들입니다.")
    async def credit(self, ctx: commands.Context):
        user_list = [x.name for x in self.bot.get_guild(704227416951881790).members if 704236010736713858 in [y.id for y in x.roles]]
        extra = await self.bot.get_guild(704227416951881790).fetch_member(309999691318165504)
        embed = discord.Embed(title="discordpy-ko에 기여해주신 분들", color=discord.Color.gold())
        embed.add_field(name="문서 번역", value=', '.join(user_list), inline=False)
        embed.add_field(name="추가적인 도움을 주신 분", value=f"{extra.name} - 문서 글꼴")
        await ctx.send(embed=embed)

    @commands.command(name="정보")
    async def info(self, ctx: commands.Context):
        embed = discord.Embed(title="discordpy-ko 봇 정보",
                              description="Created by [discordpy-ko](https://github.com/discordpy-ko).",
                              colour=discord.Color.gold())
        embed.add_field(name="들어가있는 서버 수", value=f"{len(self.bot.guilds)}개", inline=False)
        embed.add_field(name="추가 도움이 필요하시나요?", value="[번디파문 디스코드 서버](https://discord.gg/YbfbxpX)", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="eval")
    async def _eval(self, ctx: commands.Context, *, code: str):
        if ctx.author.id != 288302173912170497:
            return
        await ctx.send(await eval(code.lstrip("await ")) if code.startswith("await ") else eval(code))


def setup(bot):
    bot.add_cog(Basic(bot))
