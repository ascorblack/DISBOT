import re
import random
import discord
from discord.ext import commands
from config import settings
import asyncio
import json

token = settings['TOKEN']
bot = commands.Bot(command_prefix=settings['PREFIX'])
bot.remove_command('help')
queue = []


#Все функции тут:
def check_admin(roles: list):
    result = False
    for role in roles:
        if role.name == 'Ботовод' or role.name == 'Админ' or role.name == 'Повелитель':
            result = True
    return result


#Ивенты
@bot.event
async def on_ready():
    print('Бот коннект!')
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':grimacing: Ой, что-то пошло не так...\nВведите "-помощь (команда)"')


#Мини-игры:
@bot.command()
async def рандом(text, a, b):
    if a > b:
        rand = random.randint(int(b), int(a))
        await text.send('Выпало число: ' + str(rand))
        exit
    elif a == b:
        await text.send('Невозможно получить число!')
    else:
        rand = random.randint(int(a), int(b))
        await text.send('Выпало число: ' + str(rand))
@bot.command()
async def перестрелка(ctx, user1, user2, ammo1, ammo2):
        chance = 50
        if int(ammo1) - int(ammo2) >= 5 and int(ammo1) - int(ammo2) < 15:
            chance = chance + 15
        elif int(ammo1) - int(ammo2) >= 15:
            chance = chance + 25
        elif int(ammo2) - int(ammo1) >= 5 and int(ammo2) - int(ammo1) < 15:
            chance = chance - 15
        elif int(ammo2) - int(ammo1) >= 15:
            chance = chance - 25
        else:
            chance = chance
        win = random.randint(0, 100)
        await ctx.send('Шанс выигрыша: ' + str(chance) + '/' + str(100-int(chance)))
        if win < chance:
            await ctx.send('Выиграл ' + user1 + '!')
        elif win == chance:
            await ctx.send('Ничья!')
        else:
            await ctx.send('Выиграл ' + user2 + '!')
@bot.command()
async def дуэль(ctx, user1, user2):
    await ctx.send('Шансы 50/50')
    win = random.randint(0, 100)
    if win < 50:
        await ctx.send('Выиграл ' + user1 + '!')
    elif win == 50:
        await ctx.send('Ничья!')
    else:
        await ctx.send('Выиграл ' + user2 + '!')


#Остальные команды:
@bot.command()
async def помощь(ctx, help=None):
    if help == 'перестрелка':
        emb = discord.Embed(title='Форма заполнения "-перестрелка":', color=discord.Colour.red(),
                    description='\nЕСЛИ НУЖНО, ЧТОБЫ ИМЯ СОДЕРЖАЛО БОЛЬШЕ ОДНОГО СЛОВА,Т.Е. ИМЕЛО ПРОБЕЛ, НУЖНО ЗАКЛЮЧИТЬ В __**КАВЫЧКИ**__! ("Джо Байден")'
                '\n\n-перестрелка (Имя 1-ого игрока) (Имя 2-ого игрока) (Кол-во патронов 1-ого Игрока) (Кол-во патронов 2-ого Игрока)'
                '\n\n**Правила увеличения шанса:**\nЕсли у игрока N патронов больше на 5-14, то его шанс выиграть увеличивается на 15%, если же разница больше 15, то на 25%')
        await ctx.send(embed=emb)
    elif help == 'шнюк':
        emb = discord.Embed(title='Инструкция по спам шнюку:', color=discord.Colour.dark_gold(), description='\n-шнюк (кол-во повторений) (любой текст)')
        await ctx.send(embed=emb)
    elif help == 'дуэль':
        emb = discord.Embed(title='Инструкция по комманде "-дуэль":', color=discord.Colour.blurple(), description='\n-дуэль (Имя 1-ого игрока) (Имя 2-ого игрока)'
                    '\n\nЕСЛИ НУЖНО, ЧТОБЫ ИМЯ СОДЕРЖАЛО БОЛЬШЕ ОДНОГО СЛОВА,Т.Е. ИМЕЛО ПРОБЕЛ, НУЖНО ЗАКЛЮЧИТЬ В __**КАВЫЧКИ**__! ("Джо Байден")')
        await ctx.send(embed=emb)
    else:
        exit
@bot.command()
async def команды(ctx):
    retStr = '-дуэль\n-перестрелка\n-рандом'
    retStr2 = '-помощь\n-чистка\n-шнюк\n-стоп\n-аватар'
    retStr3 = '-баланс\n-зп\n-купить_роль\n-заплатить'
    retStr4 = '-инвентарь\n-купить/передать_предмет\n-лот выставить/снять/изменить'
    emb = discord.Embed(title='Доступные команды:', color=discord.Colour.orange())
    emb.add_field(name='Действия с предметами:', value=retStr4, inline=True)
    emb.add_field(name='Действия балансом:', value=retStr3, inline=True)
    emb.add_field(name='Остальные команды:', value=retStr2, inline=True)
    emb.add_field(name='Мини-игры:', value=retStr, inline=True)
    await ctx.send(embed=emb)
@bot.command()
async def шнюк(ctx, k, *, text):
    i = 0
    while i <= int(k):
        i = i+1
        await ctx.send(text)
    exit
@bot.command()
async def аватар(ctx, member: discord.Member = None):
    if member == None:
        emb = discord.Embed(description=f'Неккоректные данные!')
        await ctx.send(embed=emb)
    elif member != None:
        emb = discord.Embed(title=f'Аватарка {member}')
        emb.set_image(url='{}'.format(member.avatar_url))
        await ctx.send(embed=emb)


#Деньги пользователей
@bot.command()
async def зп(ctx):
    with open('data.json', 'r') as f:
        money = json.load(f)
    if not str(ctx.author.id) in money['money']:
        money['money'][str(ctx.author.id)] = {}
        money['money'][str(ctx.author.id)]['Money'] = 0
    if not str(ctx.author.id) in queue:
        emb = discord.Embed(
            description=f'**{ctx.author}** Вы получили свои 150 :dollar:\nСледующее получение будет доступно только через 2 минуты')
        await ctx.send(embed=emb)
        money['money'][str(ctx.author.id)]['Money'] += 150
        queue.append(str(ctx.author.id))
        with open('data.json', 'w') as f:
            json.dump(money, f)
        await asyncio.sleep(120)
        queue.remove(str(ctx.author.id))
    if str(ctx.author.id) in queue:
        emb = discord.Embed(description=f'**{ctx.author}** Вы уже получили свою награду')
        await ctx.send(embed=emb)
@bot.command()
async def баланс(ctx, member: discord.Member = None):
    with open('data.json', 'r') as f:
        balance = json.load(f)
    if not str(ctx.author.id) in balance['money']:
        balance['money'][str(ctx.author.id)] = {}
        balance['money'][str(ctx.author.id)]['Money'] = 0
        with open('data.json', 'w') as f:
            json.dump(balance, f)
    if member == None:
        emb = discord.Embed(description=f'У вас на счету {balance["money"][str(ctx.author.id)]["Money"]} :dollar:', color=discord.Colour.dark_green())
        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    elif str(member.id) == str(ctx.author.id):
        emb = discord.Embed(description=f'У вас на счету {balance["money"][str(ctx.author.id)]["Money"]} :dollar:', color=discord.Colour.dark_green())
        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f'У **{member}** на счету {balance["money"][str(member.id)]["Money"]} :dollar:', color=discord.Colour.dark_green())
        emb.set_author(name=member.name, icon_url=member.avatar_url)
        await ctx.send(embed=emb)


#Магазин ролей/предметов:
@bot.command()
async def магазин(ctx, nam=None):
    with open('data.json', 'r') as f:
        shop = json.load(f)
    if nam == None:
        emb = discord.Embed(description=f'Выберите магазин, который хотите просмотреть введя:\n"**-магазин ролей**" либо "**-магазин предметов**"')
        await ctx.send(embed=emb)
    if nam == 'ролей' or nam == 'роль':
        emb = discord.Embed(title="Магазин Ролей")
        for role in shop['shop']['Role']:
            emb.add_field(name=f'Цена: {shop["shop"]["Role"][role]["Cost"]}', value=f'Роль: <@&{role}>\nКоличество: {shop["shop"]["Role"][role]["Quant"]}', inline=False)
        await ctx.send(embed=emb)
    if nam == 'предметов' or nam == 'предмет':
        emb = discord.Embed(title="Магазин Предметов")
        for user in shop['shop']['item']:
            for item in shop['shop']['item'][str(user)]:
                emb.add_field(name=f'Товар: {item}\n', value=f'**Цена: {shop["shop"]["item"][str(user)][item]["cost"]}** :dollar:\nКоличество: {shop["shop"]["item"][str(user)][item]["quant"]}\nВыставил: <@{user}>', inline=False)
        await ctx.send(embed=emb)
@bot.command()
async def купить_роль(ctx, role: discord.Role):
    with open('data.json', 'r') as f:
        money = json.load(f)
    if not str(role.id) in money['shop']['Role']:
        await ctx.send('Такой роли не выставленно в магазине ролей')
    else:
        if str(role.id) in money['shop']['Role']:
            if money['shop']['Role'][str(role.id)]['Cost'] <= money['money'][str(ctx.author.id)]['Money']:
                if not role in ctx.author.roles:
                    buy = discord.utils.get(ctx.guild.roles, id=int(role.id))
                    await ctx.author.add_roles(buy)
                    money['shop']['Role'][str(role.id)]['Quant'] -= 1
                    money['money'][str(ctx.author.id)]['Money'] -= money['shop']['Role'][str(role.id)]['Cost']
                    if money['shop']['Role'][str(role.id)]['Quant'] == 0:
                        del money['shop']['Role'][str(role.id)]
                        await ctx.send('Вы купили последний слот!')
                    else:
                        await ctx.send('Вы купили роль!')
                else:
                    await ctx.send('У вас уже есть эта роль!')
            else:
                await ctx.send('У вас недостаточно денег!')
    with open('data.json', 'w') as f:
        json.dump(money, f)
@bot.command()
async def купить_предмет(ctx, item, member: discord.Member=None):
    with open('data.json', 'r') as f:
        buyi = json.load(f)
    if not str(ctx.author.id) in buyi['money']:
        buyi['money'][str(ctx.author.id)] = {}
        buyi['money'][str(ctx.author.id)]['Money'] = 0
    if not str(member.id) in buyi['money']:
        buyi['money'][str(member.id)] = {}
        buyi['money'][str(member.id)]['Money'] = 0
    if not str(member.id) in buyi['shop']['item']:
        emb = discord.Embed(description=f'Комманда введена неккоректно.\nНаберите "**-помощь купить**"')
        await ctx.send(embed=emb)
    elif not str(item) in buyi['shop']['item'][str(member.id)]:
        emb = discord.Embed(description=f'Комманда введена неккоректно.\nНаберите "**-помощь купить**"')
        await ctx.send(embed=emb)
    else:
        if buyi['shop']['item'][str(member.id)][item]['cost'] <= buyi['money'][str(ctx.author.id)]['Money']:
            buyi['money'][str(ctx.author.id)]['Money'] -= buyi['shop']['item'][str(member.id)][item]['cost']
            buyi['money'][str(member.id)]['Money'] += buyi['shop']['item'][str(member.id)][item]['cost']
            if not str(ctx.author.id) in buyi['inv']:
                buyi['inv'][str(ctx.author.id)] = {}
            buyi['inv'][str(ctx.author.id)][item] = {}
            buyi['inv'][str(ctx.author.id)][item]['quanti'] = buyi['shop']['item'][str(member.id)][item]['quant']
            emb = discord.Embed(description=f'Вы купили "{item}" в количестве {buyi["inv"][str(ctx.author.id)][item]["quanti"]} за {buyi["shop"]["item"][str(member.id)][item]["cost"]} :dollar:')
            del buyi['shop']['item'][str(member.id)][item]
            await ctx.send(embed=emb)
    with open('data.json', 'w') as f:
        json.dump(buyi, f)
@bot.command()
async def заплатить(ctx, why, member: discord.Member, arg: int, name=None):
    with open('data.json', 'r') as f:
        money = json.load(f)
    if why == 'деньги' and name == None:
        if not str(member.id) in money['money']:
            money['money'][str(member.id)] = {}
            money['money'][str(member.id)]['Money'] = 0
        if money['money'][str(ctx.author.id)]['Money'] >= arg:
            emb = discord.Embed(description=f'**{ctx.author}** подарил **{member}** **{arg}** :dollar:')
            money['money'][str(ctx.author.id)]['Money'] -= arg
            money['money'][str(member.id)]['Money'] += arg
            await ctx.send(embed=emb)
        else:
            await ctx.send('У вас недостаточно денег')
    elif why == 'предмет' and name != None:
        if not str(member.id) in money['inv']:
            money['inv'][str(member.id)] = {}
        if name in money['inv'][str(ctx.author.id)]:
            if arg > money['inv'][str(ctx.author.id)][name]['quanti']:
                emb = discord.Embed(description=f'Вы не можете передать больше, чем имеете!')
                await ctx.send(embed=emb)
            else:
                if arg < money['inv'][str(ctx.author.id)][name]['quanti']:
                    money['inv'][str(ctx.author.id)][name]['quanti'] -= arg
                if arg == money['inv'][str(ctx.author.id)][name]['quanti']:
                    del money['inv'][str(ctx.author.id)][name]
                if name in money['inv'][str(member.id)]:
                    money['inv'][str(member.id)][name]['quanti'] += arg
                    emb = discord.Embed(description=f'Вы передали {member} {arg} единиц "{name}"')
                    await ctx.send(embed=emb)
                else:
                    money['inv'][str(member.id)][name] = {}
                    money['inv'][str(member.id)][name]['quanti'] = arg
                    emb = discord.Embed(description=f'Вы передали {member} {arg} единиц "{name}"')
                    await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f'У вас нет этого предмета!')
            await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f'Введены неккорентые данные!\nДля помощи напишите "**-помощь передать**"')
        await ctx.send(embed=emb)
    with open('data.json', 'w') as f:
        json.dump(money, f)


#Система инвентаря
@bot.command()
async def лот(ctx, act, name, qu: int = None, cost: int = None):
    with open('data.json', 'r') as f:
        buyi = json.load(f)
    if act == 'изменить' and cost != None and qu == None:
        if not name in buyi['shop']['item'][str(ctx.author.id)]:
            emb = discord.Embed(description=f'Неккоректные данные')
            await ctx.send(embed=emb)
        if cost == None:
            emb = discord.Embed(description=f'Введите новую цену!')
            await ctx.send(embed=emb)
        else:
            buyi['shop']['item'][str(ctx.author.id)][name]['cost'] = cost
            emb = discord.Embed(description=f'Цена "{name}" была изменена\nТеперь она составляет **{buyi["shop"]["item"][str(ctx.author.id)][name]["cost"]} :dollar:**')
            await ctx.send(embed=emb)
    if act == 'снять' and cost == None:
        if not name in buyi['shop']['item'][str(ctx.author.id)]:
            emb = discord.Embed(description=f'Неккоректные данные')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f'Слот "{name}" был снят')
            await ctx.send(embed=emb)
            if not str(ctx.author.id) in buyi['inv']:
                buyi['inv'][str(ctx.author.id)] = {}
            buyi['inv'][str(ctx.author.id)] = {}
            buyi['inv'][str(ctx.author.id)][name] = {}
            buyi['inv'][str(ctx.author.id)][name]['cost'] = cost
            del buyi['shop']['item'][str(ctx.author.id)][name]
    if act == 'выставить' and cost != None and qu != None:
        if name in buyi['inv'][str(ctx.author.id)]:
            if buyi['inv'][str(ctx.author.id)][name]['quanti'] < qu:
                emb = discord.Embed(description=f'Вы пытаетесь выставить большее кол-во, чем имеете!')
                await ctx.send(embed=emb)
                pass
            if buyi['inv'][str(ctx.author.id)][name]['quanti'] > qu:
                buyi['inv'][str(ctx.author.id)][name]['quanti'] -= qu
                if not str(ctx.author.id) in buyi['shop']['item']:
                    buyi['shop']['item'][str(ctx.author.id)] = {}
                buyi['shop']['item'][str(ctx.author.id)][name] = {}
                buyi['shop']['item'][str(ctx.author.id)][name]['cost'] = cost
                buyi['shop']['item'][str(ctx.author.id)][name]['quant'] = qu
                emb = discord.Embed(
                    description=f'Вы выставили на продажу {qu} единиц "{name}" за общую стоимость {cost} :dollar:')
                await ctx.send(embed=emb)
            if buyi['inv'][str(ctx.author.id)][name]['quanti'] == qu:
                del buyi['inv'][str(ctx.author.id)][name]
                if not str(ctx.author.id) in buyi['shop']['item']:
                    buyi['shop']['item'][str(ctx.author.id)] = {}
                buyi['shop']['item'][str(ctx.author.id)][name] = {}
                buyi['shop']['item'][str(ctx.author.id)][name]['cost'] = cost
                buyi['shop']['item'][str(ctx.author.id)][name]['quant'] = qu
                emb = discord.Embed(
                    description=f'Вы выставили на продажу {qu} единиц "{name}" за общую стоимость {cost} :dollar:')
                await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f'Вы пытаетесь выставить предмет, которого нет у вас!')
            await ctx.send(embed=emb)
    with open('data.json', 'w') as f:
        json.dump(buyi, f)
@bot.command()
async def инвентарь(ctx, member: discord.Member = None):
    with open('data.json', 'r') as f:
        invs = json.load(f)
    if member == None or str(member.id) == str(ctx.author.id):
        if not str(ctx.author.id) in invs['inv']:
            invs['inv'][str(ctx.author.id)] = {}
        emb = discord.Embed(title='Ваши предметы')
        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        for inv in invs.copy()['inv'][str(ctx.author.id)]:
            emb.add_field(name=f'Предмет: {inv}', value=f'Количество: {invs["inv"][str(ctx.author.id)][inv]["quanti"]}', inline=False)
        await ctx.send(embed=emb)
    elif member != None and member != ctx.author.id:
        if not str(member.id) in invs['inv']:
             invs['inv'][str(member.id)] = {}
        emb = discord.Embed(title=f'Его предметы')
        emb.set_author(name=f'Инвентарь {member.name}', icon_url=member.avatar_url)
        for inv in invs['inv'][str(member.id)]:
            emb.add_field(name=f'Предмет: {inv}', value=f'Количество: {invs["inv"][str(member.id)][inv]["quanti"]}', inline=False)
        await ctx.send(embed=emb)
    with open('data.json', 'w') as f:
        json.dump(invs, f)


#Админские комманды
@bot.command()
async def стоп(ctx):
    # await ctx.send(str(ctx.author.roles))
    if check_admin(ctx.author.roles):
        await ctx.send('Ну ББ, KEKW')
        await bot.logout()
    else:
        emb = discord.Embed(description=f'У вас недостаточно прав!', color=discord.Colour.red())
        await ctx.send(embed=emb)
@bot.command()
async def чистка(ctx, amount=5):
    if check_admin(ctx.author.roles):
        await ctx.channel.purge(limit=amount)
        emb = discord.Embed(color=discord.Colour.dark_grey(), description='Было отчищенно ' + str(amount) + ' сообщений!')
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f'У вас недостаточно прав!', color=discord.Colour.red())
        await ctx.send(embed=emb)
@bot.command(pass_context=True)
async def добавить_предмет(ctx, name, qu: int, member: discord.Member = None):
    if check_admin(ctx.author.roles):
        with open('data.json', 'r') as f:
            add = json.load(f)
        if member == None or str(member.id) == str(ctx.author.id):
            if not str(ctx.author.id) in add['inv']:
                add['inv'][str(ctx.author.id)] = {}
            if not name in add['inv'][str(ctx.author.id)]:
                add['inv'][str(ctx.author.id)][name] = {}
                add['inv'][str(ctx.author.id)][name]['quanti'] = qu
                emb = discord.Embed(description=f':white_check_mark: Вы добавили предмет "{name}" в количестве {str(qu)}')
                await ctx.send(embed=emb)
                if add['inv'][str(ctx.author.id)][name]['quanti'] <= 0:
                    del add['inv'][str(ctx.author.id)][name]
                    emb = discord.Embed(description=f'Данный предмет был удалён, т.к. был равен 0 или был меньше его!')
                    await ctx.send(embed=emb)
            else:
                add['inv'][str(ctx.author.id)][name]['quanti'] += qu
                if qu < 0:
                    emb = discord.Embed(description=f':white_check_mark: Вы уменьшили количество предмета "{name}" на {str(-qu)}')
                    await ctx.send(embed=emb)
                else:
                    emb = discord.Embed(description=f':white_check_mark: Вы увеличили количество предмета "{name}" на {str(qu)}')
                    await ctx.send(embed=emb)
                if add['inv'][str(ctx.author.id)][name]['quanti'] <= 0:
                    del add['inv'][str(ctx.author.id)][name]
                    emb = discord.Embed(description=f'Данный предмет был удалён, т.к. был равен 0 или был меньше его!')
                    await ctx.send(embed=emb)
        else:
            if not str(member.id) in add['inv']:
                 add['inv'][str(member.id)] = {}
            if not name in add['inv'][str(member.id)]:
                add['inv'][str(member.id)][name] = {}
                add['inv'][str(member.id)][name]['quanti'] = qu
                with open('data.json', 'w') as f:
                    json.dump(add, f)
                emb = discord.Embed(description=f':white_check_mark: Вы добавили **{member}** предмет "{name}", теперь у него {add["inv"][str(member.id)][name]["quanti"]} "{name}"')
                await ctx.send(embed=emb)
            else:
                add['inv'][str(member.id)][name]['quanti'] += qu
                with open('data.json', 'w') as f:
                    json.dump(add, f)
                emb = discord.Embed(description=f':white_check_mark: Вы прибавили **{member}** {qu} предмета "{name}"\nТеперь у него {add["inv"][str(member.id)][name]["quanti"]} "{name}"')
                await ctx.send(embed=emb)
        with open('data.json', 'w') as f:
            json.dump(add, f)
    else:
        emb = discord.Embed(description=f':no_entry_sign: У вас недостаточно прав!', color=discord.Colour.red())
        await ctx.send(embed=emb)
@bot.command()
async def удалить_предмет(ctx, name, qu=754325616, member: discord.Member = None):
    if check_admin(ctx.author.roles):
        with open('data.json', 'r') as f:
            rem = json.load(f)
        if member == None or str(member.id) == str(ctx.author.id):
            if not name in rem['inv'][str(ctx.author.id)]:
                await ctx.send(':no_entry_sign: у вас нет такого предмета в инвентаре!')
                exit
            else:
                if qu <= 0:
                    await ctx.send(':no_entry_sign: Невозможно удалить отрицательное/0 число!')
                    exit
                elif qu == 754325616:
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у себя {str(rem["inv"][str(ctx.author.id)][name]["quanti"])} предмета "{name}"')
                    await ctx.send(embed=emb)
                    del rem['inv'][str(ctx.author.id)][name]
                elif qu >= rem['inv'][str(ctx.author.id)][name]['quanti']:
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у себя {str(rem["inv"][str(ctx.author.id)][name]["quanti"])} предмета "{name}"')
                    await ctx.send(embed=emb)
                    del rem['inv'][str(ctx.author.id)][name]
                else:
                    rem['inv'][str(ctx.author.id)][name]['quanti'] -= qu
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у себя {str(qu)} предмета "{name}"')
                    await ctx.send(embed=emb)
        elif member != str(ctx.author.id):
            if not name in rem['inv'][str(member.id)]:
                emb = discord.Embed(description=f'У {member.mention} нет такого предмета в инвентаре')
                await ctx.send(embed=emb)
                exit
            else:
                if qu <= 0:
                    await ctx.send('Невозможно удалить отрицательное/0 число!')
                    exit
                elif qu >= rem['inv'][str(member.id)][name]['quanti']:
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у {member.mention} {str(rem["inv"][str(member.id)][name]["quanti"])} "{name}"')
                    await ctx.send(embed=emb)
                    del rem['inv'][str(member.id)][name]
                else:
                    rem['inv'][str(member.id)][name]['quanti'] -= qu
                    emb = discord.Embed(description=f':white_check_mark: Вы удалили у {member.mention} {str(qu)} "{name}"')
                    await ctx.send(embed=emb)
        with open('data.json', 'w') as f:
            json.dump(rem, f)
    else:
        emb = discord.Embed(description=f':no_entry_sign: У вас недостаточно прав!', color=discord.Colour.red())
        await ctx.send(embed=emb)
@bot.command()
async def выставить_роль(ctx, role: discord.Role, cost: int, quant=1):
    if check_admin(ctx.author.roles):
        if quant <= 0:
            await ctx.send(':no_entry_sign: Невозможно выставить отрицательное/нулеовое кол-во слотов!')
            pass
        else:
            with open('data.json', 'r') as f:
                add = json.load(f)
            if str(role.id) in add['shop']:
                await ctx.send(":no_entry_sign: Эта роль уже есть в магазине")
            if not str(role.id) in add['shop']:
                add['shop']['Role'][str(role.id)] = {}
                add['shop']['Role'][str(role.id)]['Cost'] = cost
                add['shop']['Role'][str(role.id)]['Quant'] = quant
                await ctx.send(':white_check_mark: Роль добавлена в магазин')
            with open('data.json', 'w') as f:
                json.dump(add, f)
    else:
        emb = discord.Embed(description=f':no_entry_sign: У вас недостаточно прав!', color=discord.Colour.red())
        await ctx.send(embed=emb)
@bot.command()
async def удалить_роль(ctx, role: discord.Role, quant=None):
    if check_admin(ctx.author.roles):
        if quant == None:
            with open('data.json', 'r') as f:
                remove = json.load(f)
            if not str(role.id) in remove['shop']['Role']:
                await ctx.send(":no_entry_sign: Этой роли нет в магазине")
            if str(role.id) in remove['shop']['Role']:
                await ctx.send(':white_check_mark: Роль удалена из магазина')
                del remove['shop']['Role'][str(role.id)]
            with open('data.json', 'w') as f:
                json.dump(remove, f)
        else:
            with open('data.json', 'r') as f:
                remove = json.load(f)
            if not str(role.id) in remove['shop']['Role']:
                await ctx.send(":no_entry_sign: Этой роли нет в магазине")
            if int(quant) > remove['shop']['Role'][str(role.id)]['Quant']:
                with open('data.json', 'r') as f:
                    remove = json.load(f)
                if str(role.id) in remove['shop']['Role']:
                    await ctx.send(':white_check_mark: Роль удалена из магазина')
                    del remove['shop']['Role'][str(role.id)]
                with open('data.json', 'w') as f:
                    json.dump(remove, f)
            else:
                if str(role.id) in remove['shop']['Role']:
                    remove['shop']['Role'][str(role.id)]['Quant'] -= int(quant)
                    await ctx.send(':white_check_mark:  ' + str(quant) + ' выставленных слотов роли было удалено из магазина')
                with open('data.json', 'w') as f:
                    json.dump(remove, f)
    else:
        emb = discord.Embed(description=f':no_entry_sign: У вас недостаточно прав!', color=discord.Colour.red())
        await ctx.send(embed=emb)
@bot.command()
async def добавить_деньги(ctx, qu: int, member: discord.Member = None):
    if check_admin(ctx.author.roles):
        if qu > 0:
            with open('data.json', 'r') as f:
                money = json.load(f)
            if str(member.id) == str(ctx.author.id):
                if not str(ctx.author.id) in money['money']:
                    money['money'][str(ctx.author.id)] = {}
                    money['money'][str(ctx.author.id)]['Money'] = 0
                if str(member.id) in money['money']:
                    money['money'][str(ctx.author.id)]['Money'] += qu
                    emb = discord.Embed(description=f'Вы добавили на свой счёт {qu} :dollar:', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            else:
                if not str(member.id) in money['money']:
                    money['money'][str(member.id)] = {}
                    money['money'][str(member.id)]['Money'] = 0
                if str(member.id) in money['money']:
                    money['money'][str(member.id)]['Money'] += qu
                    emb = discord.Embed(description=f'Вы добавили на счёт **{member}** {qu} :dollar:', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            with open('data.json', 'w') as f:
                json.dump(money, f)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Вы не можете добавить отрицательно/нулевое количество :dollar:', color=discord.Colour.red())
            await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f':no_entry_sign: У вас недостаточно прав!', color=discord.Colour.red())
        await ctx.send(embed=emb)
@bot.command()
async def удалить_деньги(ctx, qu: int, member: discord.Member = None):
    if check_admin(ctx.author.roles):
        if qu > 0:
            with open('data.json', 'r') as f:
                money = json.load(f)
            if str(member.id) == str(ctx.author.id):
                if not str(ctx.author.id) in money['money']:
                    money['money'][str(ctx.author.id)] = {}
                    money['money'][str(ctx.author.id)]['Money'] = 0
                if str(member.id) in money['money']:
                    money['money'][str(ctx.author.id)]['Money'] -= qu
                    emb = discord.Embed(description=f'Вы удалили со своего счёта {qu} :dollar:', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            else:
                if not str(member.id) in money['money']:
                    money['money'][str(member.id)] = {}
                    money['money'][str(member.id)]['Money'] = 0
                if str(member.id) in money['money']:
                    money['money'][str(member.id)]['Money'] -= qu
                    emb = discord.Embed(description=f'Вы удалили со счёта **{member}** {qu} :dollar:', color=discord.Colour.dark_green())
                    await ctx.send(embed=emb)
            with open('data.json', 'w') as f:
                json.dump(money, f)
        else:
            emb = discord.Embed(description=f':no_entry_sign: Вы не можете удалить отрицательно/нулевое количество :dollar:', color=discord.Colour.red())
            await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f':no_entry_sign: У вас недостаточно прав!', color=discord.Colour.red())
        await ctx.send(embed=emb)


bot.run(settings['TOKEN'])