# Discord bot import
import discord
import ndjson
import glob
import datetime
import os
import urllib.parse
import feedparser

# My program import
from webhook import webhook_sender

class Add:
    async def add_info(self, interaction, mode, word, webhook_url):
        
        await interaction.response.defer()

        # webhookを使う準備
        webhook_send = webhook_sender()
            
        # アカウント、ハッシュタグの正当性をライブラリを用いて確認
        nitter_url = os.environ.get('nitter_url')
        rss_url = ''

        if mode == 'account':
            rss_url = nitter_url + word + '/rss'
        else:
            word = urllib.parse.quote(word)
            rss_url = nitter_url + 'search/rss?f=tweets&q=%23' + word

        d = feedparser.parse(rss_url)

        try:
            print(d['entries'][0])
        except Exception:
            embed=discord.Embed(title="エラー！", description=":x:入力したアカウント名・またはハッシュタグを確認してください。:x:\n※このエラーが多発する場合、Nitterインスタンス側での問題が起こっている可能性があります。Bot管理者へ確認をお願いします。", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return

        # webhook URLが正当なものかを確認
        try:
            await webhook_send.webhook_send(webhook_url, "Test Webhook", "no", "Test message")

        except Exception as e:
            embed=discord.Embed(title="エラー！", description=":x:入力したDiscordのWebhookURLを確認してください。:x:", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return

        # ギルドのフォルダがあるかの確認
        judge = 0
        dir_data = os.listdir(path='./data/data_json')
        for i in range(0, len(dir_data)):
            if str(interaction.guild.id) == dir_data[i]:
                judge = 1
                break

        if judge != 1: # なければ作成する
            os.mkdir('./data/data_json/' + str(interaction.guild.id))
        
        # モードのファイルがあるかの確認
        judge = 0
        dir_data = os.listdir(path='./data/data_json/' + str(interaction.guild.id))
        for i in range(0, len(dir_data)):
            if mode == dir_data[i]:
                judge = 1
                break

        if judge != 1: # なければ作成する
            os.mkdir('./data/data_json/' + str(interaction.guild.id) + '/' + mode)
        

        # 指定のアカウント・ハッシュタグのndjsonファイルが存在しているかの確認
        files = glob.glob('./data/data_json/' + str(interaction.guild.id) + '/' + mode + '/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == word + ".ndjson"):
                #print("一致しました！")
                judge = 1
                break
        
        if judge != 1:
            # もし一致しなければ、アカウント・ハッシュタグの更新状況を保存する
            for entry in d.entries:
                url_split = entry.link.split("/")

                url_data = "/" + url_split[3] + "/" +  url_split[4] + "/" + url_split[5]

                url_split = url_data.split("#")
                url_data = url_split[0]
                
                content = {
                    "url_parts" : url_data,
                    "notification_end" : 'yes'
                }

                with open('./data/data_json/' + str(interaction.guild.id) + '/' + mode  + '/' + word + ".ndjson", 'a') as f:
                    writer = ndjson.writer(f)
                    writer.writerow(content)
        else:
            embed=discord.Embed(title="エラー！", description=":x:既に同じアカウント・ハッシュタグの通知設定が登録されています。:x:", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return
        
        # メンションの指定がなければ
        #if mention ==  None:
        #    mention_info = "Off"
        #else:
        #    mention_info = mention.id
        
        # メッセージの指定がなければ
        #if message == None:
        #    message = "更新されました！"
        

        # guild_jsonフォルダにサーバーidのフォルダを作成
        content = {
                "type" : mode,
                "name" : word,
                "latest_time": str(datetime.datetime.now()),
                "webhook_url": webhook_url
        }

        with open('./data/guild_json/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(content)
        
        # 結果表示
        if mode == 'account':
            print("登録しました!:" + word + "の入力されたアカウントの通知を設定しました。")
            embed=discord.Embed(title="登録しました!", description=word + "\nこの入力されたチャンネルの通知を設定しました。\n\nタイプ：" + mode + "\nアカウント名：@" + word, color=0x00ff7f) 
        else:
            word = urllib.parse.unquote(word)
            print("登録しました!:" + word + "の入力されたハッシュタグの通知を設定しました。")
            embed=discord.Embed(title="登録しました!", description=word + "\nこの入力されたチャンネルの通知を設定しました。\n\nタイプ：" + mode + "\nハッシュタグ：#" + word, color=0x00ff7f) 

        await interaction.followup.send(embed=embed)