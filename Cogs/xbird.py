# Discord bot import
import discord
from discord.ext import commands
from discord import app_commands

# My program import
from Cogs.CommandPrograms.xbird_add import Add
from Cogs.CommandPrograms.xbird_delete import Delete
from Cogs.CommandPrograms.xbird_list import List

#test_guild_id = your_guild_id

#@app_commands.guilds(test_guild_id)
@app_commands.default_permissions(administrator=True)
class Xbird(app_commands.Group):
    def __init__(self, bot: commands.Bot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot

    # /xbird add *
    xbird_add = app_commands.Group(name="add", description="指定されたアカウントやハッシュタグの更新の通知を送信する設定を行います。")
    
    @xbird_add.command(name="account", description="指定されたアカウントの通知を送信する設定を行います。")
    @app_commands.describe(user_name="X（旧Twitter）のユーザーネーム（例：@twitterのtwitterの部分）")
    @app_commands.describe(webhook_url="Discordで作成したWebhookのURL")
    #@app_commands.describe(message="通常の通知をする時に出すメッセージの指定（入力がない場合はデフォルトメッセージを出します。）")
    #@app_commands.describe(mention="メンションを行うロール（入力がない場合はメンションない状態になります。）")
    async def xbird_account_add(self, interaction: discord.Interaction, user_name: str, webhook_url: str):
        mode = 'account'

        xb_add = Add()
        await xb_add.add_info(interaction, mode, user_name, webhook_url)
    
    @xbird_add.command(name="hashtag", description="指定されたハッシュタグの通知を送信する設定を行います。")
    @app_commands.describe(hashtag="X（旧Twitter）上でのハッシュタグ（例：#TwitterのTwitterの部分）")
    @app_commands.describe(webhook_url="Discordで作成したWebhookのURL")
    #@app_commands.describe(message="通常の通知をする時に出すメッセージの指定（入力がない場合はデフォルトメッセージを出します。）")
    #@app_commands.describe(mention="メンションを行うロール（入力がない場合はメンションない状態になります。）")
    async def xbird_hashtag_add(self, interaction: discord.Interaction, hashtag: str, webhook_url:str):
        mode = 'hashtag'

        xb_add = Add()
        await xb_add.add_info(interaction, mode, hashtag, webhook_url)

    # /xbird delete *
    xbird_delete = app_commands.Group(name="delete", description="指定されたアカウントやハッシュタグの更新の通知を送信する設定を削除します。")

    @xbird_delete.command(name="account", description="指定されたアカウントの通知を送信する設定を削除します")
    async def xbird_account_delete(self, interaction: discord.Interaction):
        mode = "account"

        xb_delete = Delete()
        await xb_delete.delete_info(interaction, mode)

    @xbird_delete.command(name="hashtag", description="指定されたハッシュタグの通知を送信する設定を削除します")
    async def xbird_hashtag_delete(self, interaction: discord.Interaction):
        mode = "hashtag"

        xb_delete = Delete()
        await xb_delete.delete_info(interaction, mode)

    # /xbird list *
    xbird_list = app_commands.Group(name="list", description="現在通知が設定されているアカウントやハッシュタグの一覧を表示します。")
    
    @xbird_list.command(name="account", description="通知が設定されているアカウントの一覧を表示します")
    async def xbird_account_list(self, interaction: discord.Interaction):
        mode = "account"

        xb_list = List()
        await xb_list.list_info(interaction, mode)

    @xbird_list.command(name="hashtag", description="通知が設定されているハッシュタグの一覧を表示します")
    async def xbird_hashtag_list(self, interaction: discord.Interaction):
        mode = "hashtag"
        
        xb_list = List()
        await xb_list.list_info(interaction, mode)
    
async def setup(bot: commands.Bot):
    bot.tree.add_command(Xbird(bot, name="xbird"))