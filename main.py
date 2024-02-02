# Discord bot import
import os
import glob
import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv

# my program import
from task import Task

# Bot start
load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

#test_guild_id = your_guild_id

@bot.event
async def on_ready():

    # 接続時のメッセージ
    print("接続しました！")
    
    # 「～をプレイ中」を表示させる
    await bot.change_presence(activity=discord.Game(name="/help"))

    # スラッシュコマンドを同期
    await bot.load_extension("Cogs.xbird")
    await bot.load_extension("Cogs.help")

    await bot.tree.sync()
    print("グローバルコマンド同期完了！")
    #await bot.tree.sync(guild=discord.Object(test_guild_id)) 
    #print("ギルドコマンド同期完了！")

    # dataフォルダがあるかの確認
    files = glob.glob('./*')
    judge = 0
    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == "data"):
            print("dataファイルを確認しました！")
            judge = 1
            break

    if judge != 1:
        os.mkdir('data')
        print("dataファイルがなかったため作成しました！")

    # guild_jsonフォルダがあるかの確認
    files = glob.glob('./data/*')
    judge = 0
    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == "guild_json"):
            print("guild_jsonファイルを確認しました！")
            judge = 1
            break

    if judge != 1:
        os.mkdir('./data/guild_json')
        print("guild_jsonファイルがなかったため作成しました！")

    # data_jsonフォルダがあるかの確認
    files = glob.glob('./data/*')
    judge = 0
    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == "data_json"):
            print("data_jsonファイルを確認しました！")
            judge = 1
            break

    if judge != 1:
        os.mkdir('./data/data_json')
        print("data_jsonファイルがなかったため作成しました！")
    
    # 定期的に動かすループ処理の開始
    send_channel.start()
    print("ポストの確認を開始します！")

# サーバーからキック、BANされた場合に特定の処理をする
@bot.event
async def on_guild_remove(guild):

    # guild_jsonの中にあるndjsonファイルを削除
    files = glob.glob('./data/guild_json/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if os.path.split(files[i])[1] == str(guild.id) + ".ndjson":
            judge = 1
            break
    
    if judge == 1:
        os.remove("./data/guild_json/" + str(guild.id) + ".ndjson")
        print("キックまたはBANされたため、" + str(guild.id) + "のguild_jsonを削除しました。")
    
    # data_jsonの中にあるギルドフォルダを削除
    files = glob.glob('./data/data_json/*')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if os.path.split(files[i])[1] == str(guild.id):
            judge = 1
            break
    
    if judge == 1:
        os.remove("./data/data_json/" + str(guild.id))
        print("キックまたはBANされたため、" + str(guild.id) + "のdata_jsonを削除しました。")


@tasks.loop(seconds=60)
async def send_channel():
    task = Task()
    await task.send_discord(bot)

bot.run(os.environ['token'])