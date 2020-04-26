import discord
import random
import time
import sqlite3
from discord.ext import commands

client = commands.Bot(command_prefix="삥 ")


# row[0] id
# row[1] 돈
# row[2] 월급시간
# row[3] 슬롯시간
# row[4]~row[13] 주식


stock_name = ["피아랜드", "몽몽애견", "으에상선", "지게사채", "영재게임", "구마맥주", "럼프카드", "진성역사", "우포만사", "아지호떡"]


@client.event
async def on_ready():
    print(client.user.id)
    print("준비 완료!")
    game = discord.Game("'삥 도움' 명령어를 통해 도움말을 받아보세요!")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.command()
async def 핑(message):
    await message.channel.send(
        ":ping_pong: 퐁! " + str(int(client.latency * 1000)) + "ms\n<@" + str(message.author.id) + ">")


@client.command()
async def 가입(message):
    conn = sqlite3.connect("Money.db")
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM Money'):
        if row[0] == int(message.author.id):
            await message.channel.send("```diff\n-이미 가입된 계좌입니다!```")
            conn.commit()
            conn.close()
            return
    cur.execute('INSERT INTO Money VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})'
                .format(message.author.id, 50000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    await message.channel.send("<@" + message.author.id + ">님, 어서오세요!")
    conn.commit()
    conn.close()


@client.command()
async def 월급(message):
    conn = sqlite3.connect("Money.db")
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM Money'):
        if int(row[0]) == int(message.author.id):
            if int(row[2]) <= int(time.time()) - 1800:
                cur.execute('UPDATE Money SET money = {} WHERE id = {}'.format(int(row[1]) + 50000, message.author.id))
                cur.execute(
                    'UPDATE Money SET paydaytime = {} WHERE id = {}'.format(int(time.time()), message.author.id))
                await message.channel.send("```diff\n+월급이 정상적으로 지급되었습니다.```")
                conn.commit()
                conn.close()
                return
            else:
                await message.channel.send("```diff\n-월급 시간이 아닙니다!\n남은 시간: "
                                           + str(int((1800 - int(time.time()) + int(row[2])) // 60)) + "분 "
                                           + str((1800 - int(time.time()) + int(row[2])) % 60) + "초```")
                conn.commit()
                conn.close()
                return
    await message.channel.send("```diff\n-'삥 가입' 명령어를 통해 가입을 진행해주세요!```")
    conn.commit()
    conn.close()
    return


@client.command()
async def 슬롯(message, *, amount: int):
    conn = sqlite3.connect("Money.db")
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM Money'):
        if int(row[0]) == int(message.author.id):
            if int(row[1]) >= amount:
                if int(row[3]) + 30 >= int(time.time()):
                    await message.channel.send("```diff\n-당신의 슬롯머신이 재정비 중입니다!\n"
                                               + "남은 시간: " + str(30 - int(time.time()) + int(row[3])) + "초```")
                    return
                cur.execute('UPDATE Money SET money = {} WHERE id = {}'.format(int(row[1]) - amount, message.author.id))
                conn.commit()
                await message.channel.send("슬롯머신이 돌아갑니다...")
                cur.execute('UPDATE Money SET slottime = {} WHERE id = {}'.format(int(time.time()), message.author.id))
                time.sleep(3)
                slot_no = random.randint(1, 1000)
                for slot in cur.execute('SELECT * FROM SlotMachine'):
                    if int(slot[3]) >= slot_no:
                        a = slot[0]
                        b = slot[1]
                        c = slot[2]
                        if int(slot[4]) == 0:
                            await message.channel.send("<@" + str(message.author.id) + ">님의 슬롯머신 결과입니다.\n"
                                                       + ":fast_forward:   " + a + b + c + "   :rewind:\n"
                                                       + "꽝! 다시 한 번 도전하세요ㅠㅠ")
                            break
                        if int(slot[4]) == 1:
                            await message.channel.send("<@" + str(message.author.id) + ">님의 슬롯머신 결과입니다.\n"
                                                       + ":fast_forward:   " + a + b + c + "   :rewind:\n"
                                                       + "같은 과일 2개에 나머지가 과일이네요. 반이라도 가져가시길..ㅠ")
                            cur.execute(
                                'UPDATE Money SET money = {} WHERE id = {}'.format(- int(amount * 0.5) + int(row[1]),
                                                                                   message.author.id))
                            break
                        if int(slot[4]) == 2:
                            await message.channel.send("<@" + str(message.author.id) + ">님의 슬롯머신 결과입니다.\n"
                                                       + ":fast_forward:   " + a + b + c + "   :rewind:\n"
                                                       + "같은 과일 2개에 럭키까지! 2배입니다!")
                            cur.execute(
                                'UPDATE Money SET money = {} WHERE id = {}'.format(int(amount) + int(row[1]),
                                                                                   message.author.id))
                            break
                        if int(slot[4]) == 3:
                            await message.channel.send("<@" + str(message.author.id) + ">님의 슬롯머신 결과입니다.\n"
                                                       + ":fast_forward:   " + a + b + c + "   :rewind:\n"
                                                       + "같은 럭키 2개! 3배입니다!")
                            cur.execute(
                                'UPDATE Money SET money = {} WHERE id = {}'.format(int(amount * 2) + int(row[1]),
                                                                                   message.author.id))
                            break
                        if int(slot[4]) == 4:
                            await message.channel.send("<@" + str(message.author.id) + ">님의 슬롯머신 결과입니다.\n"
                                                       + ":fast_forward:   " + a + b + c + "   :rewind:\n"
                                                       + "같은 과일 3개!! 10배 획득합니다!")
                            cur.execute(
                                'UPDATE Money SET money = {} WHERE id = {}'.format(int(amount * 9) + int(row[1]),
                                                                                   message.author.id))
                            break
                        if int(slot[4]) == 5:
                            await message.channel.send("<@" + str(message.author.id) + ">님의 슬롯머신 결과입니다.\n"
                                                       + ":fast_forward:   " + a + b + c + "   :rewind:\n"
                                                       + "같은 럭키 3개!! 50배 획득합니다!")
                            cur.execute(
                                'UPDATE Money SET money = {} WHERE id = {}'.format(int(amount * 49) + int(row[1]),
                                                                                   message.author.id))
                            break
                        if int(slot[4]) == 6:
                            await message.channel.send("<@" + str(message.author.id) + ">님의 슬롯머신 결과입니다.\n"
                                                       + ":fast_forward:   " + a + b + c + "   :rewind:\n"
                                                       + "777!!! 400배 획득합니다!")
                            cur.execute(
                                'UPDATE Money SET money = {} WHERE id = {}'.format(int(amount * 399) + int(row[1]),
                                                                                   message.author.id))
                            break
                conn.commit()
                conn.close()
                return
            else:
                await message.channel.send("```diff\n-돈이 부족합니다!\n현재 잔고: " + str(row[1]))
                return
    await message.channel.send("```diff\n-'삥 가입' 명령어를 통해 가입을 진행해주세요!```")
    conn.commit()
    conn.close()
    return


@client.command()
async def 정보(message):
    conn = sqlite3.connect("Money.db")
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM Money'):
        if int(row[0]) == int(message.author.id):
            embed = discord.Embed(
                title='내 정보 - 피아봇',
                description='피아봇에 오신 것을 환영합니다!',
                color=discord.Colour.red()
            )
            embed.set_footer(text='Pianory Bot v0.3.1 Made by Pianory. All Rights Reserved.')
            embed.set_author(name=message.author.name + '의 정보입니다.')
            embed.add_field(name="소지 현금", value=str(row[1]), inline=True)
            if time.time() - 1800 < int(row[2]):
                embed.add_field(name="월급날", value=str(
                    int((1800 - time.time() + int(row[2])) // 60)) + "분 "
                                                  + str(
                    int(1800 - time.time() + int(row[2])) % 60) + "초", inline=False)
            else:
                embed.add_field(name="월급날", value="월급을 받을 수 있습니다!", inline=False)
            embed.add_field(name="피아랜드", value=str(row[4]) + "주", inline=True)
            embed.add_field(name="몽몽애견", value=str(row[5]) + "주", inline=True)
            embed.add_field(name="으에상선", value=str(row[6]) + "주", inline=True)
            embed.add_field(name="지게사채", value=str(row[7]) + "주", inline=True)
            embed.add_field(name="영재게임", value=str(row[8]) + "주", inline=True)
            embed.add_field(name="구마맥주", value=str(row[9]) + "주", inline=True)
            embed.add_field(name="럼프카드", value=str(row[10]) + "주", inline=True)
            embed.add_field(name="진성역사", value=str(row[11]) + "주", inline=True)
            embed.add_field(name="우포만사", value=str(row[12]) + "주", inline=True)
            embed.add_field(name="아지호떡", value=str(row[13]) + "주", inline=True)
            embed.set_thumbnail(url=message.author.avatar_url)
            await message.channel.send(embed=embed)
            conn.commit()
            conn.close()
            return
    await message.channel.send("```diff\n-'삥 가입' 명령어를 통해 가입을 진행해주세요!```")
    conn.commit()
    conn.close()
    return


@client.command()
async def 도움(message):
    embed = discord.Embed(
        title="피아봇 도움말",
        description="피아봇을 사용할 때 쓰는 도움말입니다.",
        color=discord.Colour.red()
    )
    embed.add_field(name="삥 가입", value="피아봇에 가입합니다.")
    embed.add_field(name="삥 정보", value="본인의 정보를 확인합니다.")
    embed.add_field(name="삥 월급", value="월급 5만원을 획득합니다. (쿨타임 30분)")
    embed.add_field(name="삥 슬롯 [금액]", value="피아랜드의 슬롯머신을 사용합니다.")
    embed.add_field(name="삥 주식", value="피아봇 주식의 현재 가격을 알 수 있습니다.")
    embed.add_field(name="삥 매수 [주식명] [개수]", value="피아봇 주식을 구매할 수 있습니다.")
    embed.add_field(name="삥 매도 [주식명] [개수]", value="피아봇 주식을 판매할 수 있습니다.")
    embed.add_field(name="삥 지갑", value="소유 중인 피아봇 주식을 볼 수 있습니다.")
    embed.set_footer(text='Pianory Bot v0.3.1 Made by Pianory. All Rights Reserved.')
    await message.channel.send(embed=embed)


@client.command()
async def 주식(message):
    conn = sqlite3.connect("Money.db")
    cur = conn.cursor()
    value = []
    change = []
    up_down = []
    show = []
    for row in cur.execute('SELECT * FROM Stock'):
        value.append(row[1])
        change.append(row[2])
    conn.commit()
    conn.close()
    for i in range(0, len(value)):
        if change[i] > 0:
            up_down.append("+")
            show.append("▲")
        elif change[i] < 0:
            up_down.append("-")
            show.append("▼")
            change[i] = change[i] * -1
        else:
            up_down.append(" ")
            show.append("-")
    await message.channel.send("```diff\n현재 주식 가격 (" + time.strftime('%c', time.localtime(time.time())) + ")\n"
                               + up_down[0] + "피아랜드 " + str(value[0]) + "  (" + show[0] + str(change[0]) + ")\n"
                               + up_down[1] + "몽몽애견 " + str(value[1]) + "  (" + show[1] + str(change[1]) + ")\n"
                               + up_down[2] + "으에상선 " + str(value[2]) + "  (" + show[2] + str(change[2]) + ")\n"
                               + up_down[3] + "지게사채 " + str(value[3]) + "  (" + show[3] + str(change[3]) + ")\n"
                               + up_down[4] + "영재게임 " + str(value[4]) + "  (" + show[4] + str(change[4]) + ")\n"
                               + up_down[5] + "구마맥주 " + str(value[5]) + "  (" + show[5] + str(change[5]) + ")\n"
                               + up_down[6] + "럼프카드 " + str(value[6]) + "  (" + show[6] + str(change[6]) + ")\n"
                               + up_down[7] + "진성역사 " + str(value[7]) + "  (" + show[7] + str(change[7]) + ")\n"
                               + up_down[8] + "우포만사 " + str(value[8]) + "  (" + show[8] + str(change[8]) + ")\n"
                               + up_down[9] + "아지호떡 " + str(value[9]) + "  (" + show[9] + str(change[9]) + ")```")


@client.command()
async def 매수(message, name: str, amount: str):
    conn = sqlite3.connect("Money.db")
    cur = conn.cursor()
    if name == "피아랜드" or name == "피아":
        stock = 4
    elif name == "몽몽애견" or name == "몽몽":
        stock = 5
    elif name == "으에상선" or name == "으에":
        stock = 6
    elif name == "지게사채" or name == "지게":
        stock = 7
    elif name == "영재게임" or name == "영재":
        stock = 8
    elif name == "구마맥주" or name == "구마":
        stock = 9
    elif name == "럼프카드" or name == "럼프":
        stock = 10
    elif name == "진성역사" or name == "진성":
        stock = 11
    elif name == "우포만사" or name == "우포" or name == "만사":
        stock = 12
    elif name == "아지호떡" or name == "아지":
        stock = 13
    else:
        return
    for row in cur.execute('SELECT * FROM Stock WHERE name = {}'.format(stock)):
        price = row[1]
        if amount == "모두" or amount == "올인" or amount == "전부":
            for abc in cur.execute('SELECT * FROM Money WHERE id = {}'.format(message.author.id)):
                amount = int(abc[1]) // price
        else:
            amount = int(amount)
        for sss in cur.execute('SELECT * FROM Money WHERE id = {}'.format(message.author.id)):
            if int(sss[1]) >= amount * int(price):
                cur.execute('UPDATE Money SET money = {} WHERE id = {}'.format(int(sss[1]) - amount * int(price),
                                                                               message.author.id))
                cur.execute(
                    'UPDATE Money SET stock{} = {} WHERE id = {}'.format(int(stock - 3), int(sss[stock]) + amount,
                                                                         message.author.id))
                cur.execute('UPDATE Money SET price{} = {} WHERE id = {}'.format(int(stock - 3), int(int(sss[stock+10])+int(price)*amount), message.author.id))
                await message.channel.send("```diff\n+구매가 완료되었습니다!\n현재 소지량: " + str(int(sss[stock]) + amount) + "주```")
                conn.commit()
                conn.close()
                return
            else:
                await message.channel.send("```diff\n-소지금이 부족합니다!```")
                return
        await message.channel.send("```diff\n-'삥 가입' 명령어를 통해 가입을 진행해주세요!")
        return


@client.command()
async def 매도(message, name: str, amount: str):
    conn = sqlite3.connect("Money.db")
    cur = conn.cursor()
    if name == "피아랜드" or name == "피아":
        stock = 4
    elif name == "몽몽애견" or name == "몽몽":
        stock = 5
    elif name == "으에상선" or name == "으에":
        stock = 6
    elif name == "지게사채" or name == "지게":
        stock = 7
    elif name == "영재게임" or name == "영재":
        stock = 8
    elif name == "구마맥주" or name == "구마":
        stock = 9
    elif name == "럼프카드" or name == "럼프":
        stock = 10
    elif name == "진성역사" or name == "진성":
        stock = 11
    elif name == "우포만사" or name == "우포" or name == "만사":
        stock = 12
    elif name == "아지호떡" or name == "아지":
        stock = 13
    else:
        return
    if amount == "모두" or amount == "올인" or amount == "전부":
        for row in cur.execute('SELECT * FROM Money WHERE id = {}'.format(message.author.id)):
            amount = int(row[stock])
    else:
        amount = int(amount)
    for row in cur.execute('SELECT * FROM Stock WHERE name = {}'.format(stock)):
        price = row[1]
        for sss in cur.execute('SELECT * FROM Money WHERE id = {}'.format(message.author.id)):
            if int(sss[stock]) >= amount:
                cur.execute('UPDATE Money SET money = {} WHERE id = {}'.format(int(sss[1]) + amount * int(price),
                                                                               message.author.id))
                cur.execute(
                    'UPDATE Money SET stock{} = {} WHERE id = {}'.format(int(stock - 3), int(sss[stock]) - amount,
                                                                         message.author.id))
                cur.execute(
                    'UPDATE Money SET price{} = {} WHERE id = {}'.format(int(stock-3), int(sss[stock+10]*(1-amount/sss[stock])), message.author.id)
                )
                await message.channel.send(
                    "```diff\n+판매가 완료되었습니다!\n현재 소지금: " + str(int(sss[1]) + amount * int(price)) + "원```")
                conn.commit()
                conn.close()
                return
            else:
                await message.channel.send("```diff\n-소지 주식이 부족합니다!```")
                return
        await message.channel.send("```diff\n-'삥 가입' 명령어를 통해 가입을 진행해주세요!")
        return


@client.command()
async def 지갑(message):
    conn = sqlite3.connect("Money.db")
    cur = conn.cursor()
    have = []
    time_price = []
    say = []
    now_price = []
    for stock in range(4, 14):
        for row in cur.execute('SELECT * FROM Money WHERE id = {}'.format(message.author.id)):
            have.append(row[stock])
            time_price.append(row[stock + 10])
            for abc in cur.execute('SELECT * FROM Stock WHERE name = {}'.format(str(stock))):
                now_price.append(abc[1])
            if have[stock - 4] == 0:
                say.append("")
            else:
                say.append("\n" + stock_name[stock - 4] + ": " + str(have[stock - 4]) + "주 / 평가 손익: " + str(
                    now_price[stock - 4] * have[stock - 4] - time_price[stock - 4]) + "원")
    for mon in cur.execute('SELECT * FROM Money WHERE id = {}'.format(message.author.id)):
        money = mon[1]
        await message.channel.send("```현재 보유금: " + str(money) + "원"
                                   + say[0] + say[1] + say[2] + say[3] + say[4] + say[5] + say[6] + say[7] + say[8] +
                                   say[9] + "```")
        conn.commit()
        conn.close()
    await message.channel.send("```diff\n-'삥 가입' 명령어를 통해 가입을 진행해주세요!")
    return


client.run(token)
