# Discord bot import
import ndjson
import glob
import os
import urllib.parse
import datetime
import asyncio
import traceback
import feedparser

# My program import
from webhook import webhook_sender

# 変数
# 文字列にした時間を計算できる形式に変換する時に使用
time_format = '%Y-%m-%d %H:%M:%S.%f'
# 時差はどのくらいあるのかを世界標準時基準で代入（単位：時間）
#utc_diff = 9

class Task:
    async def send_discord(self, bot):
        try:
            # webhookを使う準備
            webhook_send = webhook_sender()

            # guild_jsonのファイル一覧を取得
            files = glob.glob('./data/guild_json/*.ndjson')
            #print(files)
            
            # 1つのギルドごとに処理を開始
            for i in range(0, len(files)):
                # guildごとのndjsonファイルの読み込み
                with open(files[i]) as f:
                    guild_data = ndjson.load(f)

                for j in range(0, len(guild_data)):
                    # もし前回の更新から1時間経っていたら
                    update_time = datetime.datetime.strptime(guild_data[j]["latest_time"], time_format)
                    if (datetime.datetime.now() - update_time).total_seconds() >= 3600:
                        #print(os.path.split(files[i])[0])
                        #print(guild_data[j])
                        # 現在のdata_jsonの読込
                        with open('./data/data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + '/' + guild_data[j]["type"]  + '/' + guild_data[j]["name"] + ".ndjson") as f:
                            old_data = ndjson.load(f)

                        # 最新のデータを取ってくる
                        nitter_url = os.environ.get('nitter_url')
                        rss_url = ''

                        if guild_data[j]["type"] == 'account':
                            rss_url = nitter_url + guild_data[j]["name"] + '/rss'
                        else:
                            rss_url = nitter_url + 'search/rss?f=tweets&q=%23' + guild_data[j]["name"]

                        d = feedparser.parse(rss_url)

                        try:
                            print(d['entries'][0])
                        except Exception as e:
                            print('Nitterデータ取得でエラーが発生しました。')
                            continue

                        # データをjson形式で変数に入れる
                        now_data = []

                        for entry in d.entries:
                            url_split = entry.link.split("/")

                            url_data = "/" + url_split[3] + "/" +  url_split[4] + "/" + url_split[5]

                            url_split = url_data.split("#")
                            url_data = url_split[0]
                            
                            content = {
                                "url_parts" : url_data,
                                "notification_end" : 'no'
                            }

                            now_data.append(content)

                        # notification_end が yes の場合の引き継ぎ
                        for k in range(0, len(now_data)):
                                for l in range(0, len(old_data)):
                                    if now_data[k]["url_parts"] == old_data[l]["url_parts"] and old_data[l]["notification_end"] == "yes":
                                        now_data[k]["notification_end"] = "yes"

                        # 更新回数を数える
                        count = 0
                        for m in range(0, len(now_data)):
                            if(now_data[m]["notification_end"] == "no"):
                                count += 1
                            else:
                                break
                        
                        if count != 0:
                            for n in range(count-1, -1, -1):
                                # 通知の送信
                                await webhook_send.webhook_send(guild_data[j]["webhook_url"], "no", "no", "https://x.com" + now_data[n]["url_parts"])

                                # 通知を出したものはdata_jsonの「notification_end」をyesに変更する
                                now_data[n]["notification_end"] = "yes"

                        # 更新されたデータをdata_jsonに保存していく
                        os.remove('./data/data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + '/' + guild_data[j]["type"]  + '/' + guild_data[j]["name"] + ".ndjson")

                        with open('./data/data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + '/' + guild_data[j]["type"]  + '/' + guild_data[j]["name"] + ".ndjson", 'a') as f:
                            for n in range(0, len(now_data)):
                                writer = ndjson.writer(f)
                                writer.writerow(now_data[n])
        
                        # 時間も更新する
                        guild_data[j]["latest_time"] = str(datetime.datetime.now())

                        # 処理が終わったことをprint
                        if guild_data[j]["type"] != "hashtag":
                            print(guild_data[j]["type"] + ":@" + guild_data[j]["name"] + "の処理が終了しました。")
                        else:
                            word = urllib.parse.unquote(guild_data[j]["name"])
                            print(guild_data[j]["type"] + ":#" + word + "の処理が終了しました。")

                        # エラー防止のための処理を止める時間
                        await asyncio.sleep(5)
        
                # guild_jsonの更新
                os.remove(files[i])
                with open(files[i], 'a') as f:
                    for k in range(0, len(guild_data)):
                        writer = ndjson.writer(f)
                        writer.writerow(guild_data[k])
                
                # 処理が終了したprint
                print("* " + os.path.splitext(os.path.basename(files[i]))[0] + "の処理が終わりました。")
            
        except Exception as e:
            print("タスクエラー：タスクでエラーが発生しました。\n" + traceback.format_exc())