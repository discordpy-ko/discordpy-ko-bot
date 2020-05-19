import discord
from discord.ext import commands


# 오류 처리
class Error(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'Loaded {__name__}!')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # 없는 명령어 감지시 실행
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction(emoji="🤔")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("권한이 없습니다.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("필수 인자가 누락되었습니다.")
        # 위쪽에 해당되지 않을 경우 실행 (오류 출력)
        else:
            await ctx.send(f'오류 - `{error}`')


def setup(client):
    client.add_cog(Error(client))
