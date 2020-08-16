# 디스코드 봇 템플릿 by eunwoo1104#9600
# discord bot template by eunwoo1104#9600
import discord
import sys
import os
import json
from discord.ext import commands
from Modules import bot_lang

with open('botsetup.json', 'r', encoding="UTF-8") as f:
    bot_data = json.load(f) # loads bot setups

prefix = bot_data["default_prefix"] # bot prefix | 봇 프리픽스
stable_token = bot_data["stable_token"] # bot stable token | 봇 스테이블 토큰
canary_token = bot_data["canary_token"] # bot canary token | 봇 카나리 토큰
chosen_token = bot_data["chosen_token"] # chooses token | 토큰 선택
bot_name = bot_data["bot_name"] # bot name | 봇 이름
sys_lang = bot_data["sys_lang"] # language you want to use | 기본 언어
owner_id = bot_data["owner_id"] # owner id | 소유자 id


# 토큰 선택 코드
# token chooser
def token():
    if chosen_token == "stable":
        return stable_token
    elif chosen_token == "canary":
        return canary_token
    else:
        print(f"Token Error; Stopping bot.\nDetail: 'chosen_token' should be 'stable' or 'canary', but current setting is '{chosen_token}'")
        sys.exit()


async def get_prefix(bot, message):
    return commands.when_mentioned_or('.!')(bot, message)


bot = commands.Bot(command_prefix=get_prefix)
# 기본 help 명령어를 지우는 코드
# Removes help command (integrated in discord.py)
bot.remove_command('help')


# 봇 주인 확인 코드
# check owner
def is_owner(ctx):
    return ctx.message.author.id == int(owner_id)


# 로드
# loads cog
@bot.command()
@commands.check(is_owner)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    text = await bot_lang.load_text(sys_lang, "loaded_cog")
    await ctx.send(str(text).format(str(extension)))


# 언로드
# unloads cog
@bot.command()
@commands.check(is_owner)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    text = await bot_lang.load_text(sys_lang, "unloaded_cog")
    await ctx.send(str(text).format(str(extension)))


# 리로드
# reloads cog
@bot.command()
@commands.check(is_owner)
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    text = await bot_lang.load_text(sys_lang, "reloaded_cog")
    await ctx.send(str(text).format(str(extension)))


# cogs 업데이트
# updates cogs
@bot.command()
@commands.check(is_owner)
async def update(ctx):
    for ext_name in os.listdir("./cogs"):
        if ext_name.endswith('.py'):
            bot.reload_extension(f'cogs.{ext_name[:-3]}')
            text = await bot_lang.load_text(sys_lang, "updated_cogs")
            await ctx.send(str(text).format(str(ext_name[:-3])))


# cog를 불러오는 스크립트
for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token())
