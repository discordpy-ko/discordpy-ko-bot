import discord
from discord.ext import commands


class Help(commands.Cog):
    """
    도움말 명령어 Cog 입니다.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="도움", aliases=["도움말", "help"])
    async def help(self, ctx: commands.Context, command_name: str = None):
        if command_name is not None:
            cogs = [(x, y.get_commands()) for x, y in self.bot.cogs.items()]
            for x in cogs:
                for n in x[1]:
                    if command_name == n.name:
                        embed = discord.Embed(title=f"{command_name} 명렁어 정보", description=str(n.description),
                                              color=discord.Color.gold())
                        embed.add_field(name="사용법", value=str(n.usage) if n.usage else f"`{n.name}`", inline=False)
                        embed.add_field(name="에일리어스", value=', '.join(n.aliases) if bool(n.aliases) else "없음",
                                        inline=False)
                        return await ctx.send(embed=embed)
            return await ctx.send(f"`{command_name}`(은)는 없는 명령어입니다.")
        base_embed = discord.Embed(title="명령어 리스트", description=f"프리픽스: `{ctx.prefix}`", color=discord.Color.gold())
        cogs = [(x, y.get_commands()) for x, y in self.bot.cogs.items()]
        for x in cogs:
            if not bool(x[1]):
                continue
            base_embed.add_field(name=x[0], value='`' + '`, `'.join([c.name for c in x[1]]) + '`',
                                 inline=False)
        await ctx.send(embed=base_embed)


def setup(bot):
    bot.add_cog(Help(bot))
