import discord
import asyncio
import sys
from discord.ext import commands
from github import Github
from git import Repo
import shutil
import json
import os

sys.path.append("..")
from Modules import async_github as agh
from Modules import async_sphinx_builder as asb

with open('botsetup.json', 'r', encoding="UTF-8") as f:
    bot_data = json.load(f)  # loads bot setups

github_token = bot_data["github_token"]
org_name = bot_data["org_name"]
loc_repository = bot_data["loc_repository"]
web_repository = bot_data["web_repository"]


class KoDocs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print(f'Loaded {__name__}!')

    async def cog_check(self, ctx):
        return ctx.author in ctx.guild.get_role(704236010736713858).members and ctx.guild.id == 704227416951881790

    @commands.group()
    async def DOCS(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='DOCS 명령어', description='프리픽스: ".!"', colour=discord.Color.gold())
            embed.add_field(name='DOCS 업데이트', value='문서를 업데이트합니다. (소요시간: 1 ~ 2분)', inline=False)
            embed.add_field(name='DOCS 유저초대', value='관리자 전용', inline=False)
            await ctx.send(embed=embed)

    @DOCS.command()
    async def 유저초대(self, ctx, name: str):
        if not ctx.author.id == 288302173912170497:
            return
        g = Github(github_token)
        user_got = g.search_users(name + "in:login")[0]
        embed = discord.Embed(title='GitHub 유저정보', description=user_got.login, colour=discord.Color.gold(), url=user_got.html_url)
        await ctx.send(embed=embed)

        await ctx.send("정말로 이 유저를 초대할까요?")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '⭕'

        try:
            await self.bot.wait_for('reaction_add', timeout=60, check=check)
        except asyncio.TimeoutError:
            await ctx.send("시간이 초과됬습니다.")
            return
        org = g.get_organization(org_name)
        org.invite_user(user=user_got)
        await ctx.send(f"`{user_got.login}`님을 초대했어요!")

    @DOCS.command()
    async def 업데이트(self, ctx, *, desc: str = None):
        # 아직 비동기 사용 안함
        # 나중에 이 코드 자체를 분리해버릴 예정
        if desc is None:
            desc = f"Updated by {ctx.author.display_name}"
        await ctx.send("잠시만 기다려주세요...")
        org = await agh.get_gh_org(org_name)
        repo_github_loc = await agh.get_gh_org_repo(org, loc_repository)
        repo_github_web = await agh.get_gh_org_repo(org, web_repository)

        commit_message = desc

        await agh.clone_gh_repo(repo_github_loc, "loc")
        await agh.clone_gh_repo(repo_github_web, "docsweb")

        await ctx.send("깃헙에서 최신 로케일 파일을 다운로드했어요! 이제 빌드를 시작할께요...")

        await asb.build_dpdocs()

        await ctx.send("빌드 완료! 이제 깃헙에 커밋할께요.")

        await agh.push_local_repo("docsweb", commit_message)

        await ctx.send("깃헙에 커밋 완료!")
        await ctx.send(file=discord.File("./discord.py-master/docs/log_make.log"))
        os.remove("./discord.py-master/docs/log_make.log")

    # embed = discord.Embed(title='', description='', colour=discord.Color.red())
    # embed.add_field(name='', value='', inline=False)

    @commands.group()
    async def PR(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='GitHub Pull Request 명령어', description='프리픽스: ".!"',
                                  colour=discord.Color.gold())
            embed.add_field(name='PR 정보 [PR번호]', value='해당 Pull Request 정보를 보여줍니다.', inline=False)
            embed.add_field(name='PR Merge [PR번호]', value='해당 Pull Request를 master 브랜치로 Merge합니다', inline=False)
            await ctx.send(embed=embed)

    @PR.command()
    async def 정보(self, ctx, num: int = None):
        if num is None:
            return
        g = Github(github_token)
        org = g.get_organization(org_name)
        repo_github_loc = org.get_repo(loc_repository)
        pr = repo_github_loc.get_pull(num)
        embed = discord.Embed(title='Pull Request', description=f'#{num}', colour=discord.Color.gold(), url=pr.html_url)
        embed.add_field(name='제목', value=pr.title, inline=False)
        embed.add_field(name='PR 요청자 이름', value=pr.user.login)
        embed.add_field(name='Merge 가능 여부', value=str(pr.mergeable), inline=False)

        await ctx.send(embed=embed)

    @PR.command()
    async def Merge(self, ctx, num: int):
        g = Github(github_token)
        org = g.get_organization(org_name)
        repo_github_loc = org.get_repo(loc_repository)
        pr = repo_github_loc.get_pull(num)
        pr.merge()
        await ctx.send("해당 Pull Request를 Merge 했어요!")


def setup(bot):
    bot.add_cog(KoDocs(bot))
