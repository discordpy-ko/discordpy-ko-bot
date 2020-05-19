import asyncio


async def auto_div_embed(bot, ctx, embed, result):
    emoji_list = ["⏹", "➡"]
    if len(result) == 0:
        embed.add_field(name="검색 결과 없음", value="이런! 검색 결과가 없네요...")
        return

    def check(reaction, user):
        return str(reaction.emoji) in emoji_list and user == ctx.author

    embed = embed
    lim_count = 0
    for x in result:
        lim_count += 1
        base_link = "https://discordpy.cpbu.xyz/"
        link = base_link + x
        embed.add_field(name=str(lim_count), value=f"[`{x}`]({link})", inline=False)
        result.remove(x)
        if lim_count == 5:
            break

    msg = await ctx.send(embed=embed)

    embed.clear_fields()

    for x in emoji_list:
        await msg.add_reaction(x)

    try:
        while True:
            reaction, user = await bot.wait_for("reaction_add", timeout=30, check=check)
            if str(reaction.emoji) == emoji_list[0]:
                break
            elif str(reaction.emoji) == emoji_list[1]:
                if len(result) == 0:
                    await ctx.send("더이상 결과가 없습니다.")
                    break
                try:
                    await msg.remove_reaction(emoji_list[1], ctx.author)
                except:
                    pass
                embed = embed
                lim_count = 0
                for x in result:
                    lim_count += 1
                    base_link = "https://discordpy.cpbu.xyz/"
                    link = base_link + x
                    embed.add_field(name=str(lim_count), value=f"[`{x}`]({link})", inline=False)
                    result.remove(x)
                    if lim_count == 5:
                        break
                await msg.edit(embed=embed)
                embed.clear_fields()
        try:
            await msg.clear_reactions()
        except:
            await msg.remove_reaction(emoji_list[0], msg.author)
            await msg.remove_reaction(emoji_list[1], msg.author)

    except asyncio.TimeoutError:
        ended_msg = await ctx.send("시간을 초과했습니다.")
        try:
            await msg.clear_reactions()
        except:
            await msg.remove_reaction(emoji_list[0], msg.author)
            await msg.remove_reaction(emoji_list[1], msg.author)
        await ended_msg.delete(delay=5)
        return
