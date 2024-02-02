# Discord bot import
import discord
from discord import app_commands
from discord.ext import commands

# My program import


#test_guild_id = your_guild_id

class help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="コマンドについての簡単な使い方を出します。")
    #@app_commands.guilds(test_guild_id)
    #@app_commands.default_permissions(administrator=True)
    async def help_command(self, interaction: discord.Interaction):
        embed=discord.Embed(title="コマンドリスト")
        embed.add_field(name="このBotは/help以外はサーバー管理者しか使用することができません。", value="", inline=False)
        embed.add_field(name="/xbird add [account/hashtag]", value="X（旧Twitter）の通知を送信するアカウントもしくは、ハッシュタグを追加します。\n\n**__引数の説明（必須項目には「※必須」とつけています。）__**\n\n__[user_name/hashtag]：（※必須）アカウントもしくは、ハッシュタグを入力してください。\n※ユーザー名入力の例：「@Twitter」の場合、「Twitter」\n※ハッシュタグ入力の例：「#Twitter」の場合、「Twitter」__\n\n__webhook_url：（※必須）Discordのチャンネルで事前に作成したWebhookのURLを入力してください。", inline=False)
        embed.add_field(name="/xbird delete [account/hashtag]", value="X（旧Twitter）の通知を送信するアカウントもしくは、ハッシュタグを削除します。", inline=False)
        embed.add_field(name="/xbird list [account/hashtag]", value="X（旧Twitter）の通知を送信する登録があるアカウントもしくは、ハッシュタグを一覧を表示します。", inline=False)
        embed.add_field(name="/help", value="このBotのコマンドの簡単な使い方を出します。", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(help(bot))