import discord
import ndjson
import glob
import asyncio
import os
import urllib.parse

class Delete:
    async def delete_info(self, interaction, mode):
        
        await interaction.response.defer()

        # ボタンで制御する時に使う用
        global mode1
        mode1 = mode

        # サーバーのデータが存在しているかを確認
        files = glob.glob('./data/guild_json/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                #print("一致しました！")
                judge = 1
                break
        
        if judge != 1:
                embed=discord.Embed(title="エラー！", description=":x:このサーバーのデータが存在していません。:x:", color=0xff0000)
                await interaction.followup.send(embed=embed)
                return
        
        # ボタン
        view = discord.ui.View()
        delete_button = DeleteButton(interaction.user)  # コマンドを呼んだユーザを渡す
        view.add_item(delete_button)  
        with open('./data/guild_json/' + str(interaction.guild.id) + ".ndjson") as f:
            read_data = ndjson.load(f)
        
        # embedを出すための処理
        search_num = 0
        for i in range(0, len(read_data)):
            if read_data[i]["type"] == mode:
                search_num += 1
        
        if search_num == 0:
            embed=discord.Embed(title="エラー！", description=":x:このサーバーの "+ mode +" のデータが存在していません。:x:", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return

        embed=discord.Embed(title="登録されている通知（" + mode + "）", color=0x00ff7f)

        global count
        count = 0
        cut = 10
        for j in range(0, len(read_data)):
            # メンションの表示を指定
            #mention_view = ' '
            #if read_data[i]["mention"] == 'Off':
            #    mention_view = read_data[i]["mention"]
            #else:
            #    mention_view = '<@&' + str(read_data[i]["mention"]) + '>'
            if read_data[j]["type"] == mode:
                if mode == 'hashtag':
                    word = urllib.parse.unquote(read_data[j]["name"])
                    embed.add_field(name=str(count+1) + '. #' + word, value="", inline=False)
                else:
                    embed.add_field(name=str(count+1) + '. @' + read_data[j]["name"], value="", inline=False)
                
                count = count + 1
                
            if j == len(read_data) - 1:
                #表示させる
                await interaction.followup.send(embed=embed,view=view)
                return
            
            if count + 1 == cut:
                cut = cut + 25
                #表示させる
                await interaction.followup.send(embed=embed)
                embed=discord.Embed(title="")
                
                # DiscordのWebhook送信制限に引っかからないための対策　※効果があるかは不明
                await asyncio.sleep(2)

# モーダルボタンのクラス
class DeleteButton(discord.ui.Button):
    # コンストラクタの引数に user を追加
    def __init__(self, user: discord.User, style=discord.ButtonStyle.green, label='Next >>', **kwargs):
        self.user_id = user.id  # クラス変数にユーザ ID を保存
        super().__init__(style=style, label=label, **kwargs)

    async def callback(self, interaction: discord.Interaction):
        # 保存したユーザとボタンを押したユーザが同じかどうか
        if self.user_id == interaction.user.id:

            # 番号を入力するためのウィンドウを表示する
            await interaction.response.send_modal(answer_input())

            #await interaction.message.delete()

# モーダルウィンドウ用のクラス
class answer_input(discord.ui.Modal, title='削除したい通知の番号を入力してください。'):

    answer_number = discord.ui.TextInput(
        label='Number',
        placeholder='例：1',
    )

    async def on_submit(self, interaction: discord.Interaction):
        # 入力されたものが数字であるかどうか
        try:
            answer = int(self.answer_number.value)
            print(answer)
        except Exception as e:
            embed=discord.Embed(title="エラー！", description=":x:入力されたものが数字ではありません。\nもう一度コマンドを実行しなおしてください。:x:", color=0xff0000)
            await interaction.message.delete()
            await interaction.response.send_message(embed=embed)
            return
        
        # 入力された数字が範囲内にあるか
        print(count)
        if answer < 1 or answer > count:
            embed=discord.Embed(title="エラー！", description=":x:入力された数字が有効ではありません。\nもう一度コマンドを実行しなおしてください。:x:", color=0xff0000)
            await interaction.message.delete()
            await interaction.response.send_message(embed=embed)
            return

        # data_jsonから削除する
        with open('./data/guild_json/' + str(interaction.guild.id) + ".ndjson") as f:
                read_data = ndjson.load(f)

        search_count = 0
        data_name = ' '
        for i in range(0, len(read_data)):
            if read_data[i]["type"] == mode1:
                search_count += 1

                if search_count == answer:
                    # データ削除用に保管
                    # あとは削除した後にDiscordに表示させるメッセージ用にチャンネル名のみ保存しておく
                    data_name = read_data[i]["name"]
                    break
        
        try:
            os.remove('./data/data_json/' + str(interaction.guild.id) + "/" + mode1 + "/" + data_name + ".ndjson")
        except Exception as e:
            print("ファイルが存在しなかったため、" + data_name + "のdata_jsonを削除できませんでした。")
        
        # guild_jsonから削除する
        with open('./data/guild_json/' + str(interaction.guild.id) + ".ndjson") as f:
                read_data = ndjson.load(f)
        
        # もしguild_jsonの中身が1つだけだったらファイルごと削除をする
        if len(read_data) == 1:
            os.remove('./data/guild_json/' + str(interaction.guild.id) + ".ndjson")
        else:
            del_count = 0
            for j in range(0, len(read_data)):
                if read_data[j]["type"] == mode1:
                    del_count += 1

                    if del_count == answer:
                        del read_data[j]
                        break
            
            os.remove('./data/guild_json/' + str(interaction.guild.id) + ".ndjson")

            for k in range(0, len(read_data)):
                with open('./data/guild_json/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
                    writer = ndjson.writer(f)
                    writer.writerow(read_data[k])

        await interaction.message.delete()

        if mode1 == 'hashtag':
            data_name = urllib.parse.unquote(data_name)
            embed=discord.Embed(title="削除が完了しました！", description="#" + data_name + "を削除しました\nまた通知を受け取りたい場合は、登録しなおしてください！", color=0x00ff7f)
        else:
            embed=discord.Embed(title="削除が完了しました！", description="@" + data_name + "を削除しました\nまた通知を受け取りたい場合は、登録しなおしてください！", color=0x00ff7f)
        
        await interaction.response.send_message(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('エラーが発生しました。', ephemeral=False)

        #traceback.print_exception(type(error), error, error.__traceback__)