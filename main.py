import json
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from config import settings
import asyncio
import sqlite3

#Функции
def get_prefix(client, message):
    with open("data.json", 'r') as f:
        prefixes = json.load(f)
    return prefixes['servers'][str(message.guild.id)]['prefix']

bot = commands.Bot(command_prefix=get_prefix)
bot.owner_ids = [263708575241601024]
token = settings['TOKEN']
bot.remove_command('help')
queue = []
bot.eco_emoji = ':dollar:'

# РАБОТА С SQLITE3
# db = sqlite3.connect('data.db')
# sql = db.cursor()
# sql.execute("""CREATE TABLE IF NOT EXISTS prefixs (prefix TEXT)""")
# sql.execute("""CREATE TABLE IF NOT EXISTS lox (loxi TEXT)""")
# db.commit()


#Ивенты
@bot.event
async def on_ready():
    print('Бот коннект!')
    while True:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"suggestions"))
@bot.event
async def on_guild_join(guild):
    with open("data.json", 'r') as f:
        pref = json.load(f)
    if not 'servers' in pref:
        pref['servers'] = {}
    pref['servers'][str(guild.id)] = {}
    pref['servers'][str(guild.id)]['prefix'] = '-'
    with open("data.json", 'w') as f:
        json.dump(pref, f, indent=4)
@bot.event
async def on_guild_remove(guild):
    with open("data.json", 'r') as f:
        pref = json.load(f)
    del pref['servers'][str(guild.id)]
    with open("data.json", 'w') as f:
        json.dump(pref, f, indent=4)

#@bot.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.MissingRequiredArgument):
#        await ctx.send(':grimacing: Ой, кажется вы пропустили один или несколько аргументов...\nВведите "-помощь (команда)"')
#    if isinstance(error, commands.MissingPermissions):
#        emb = discord.Embed(description=f':no_entry_sign: У вас недостаточно прав!', color=discord.Colour.red())
#        await ctx.send(embed=emb)
#    if isinstance(error, commands.NotOwner):
#        emb = discord.Embed(description=f':no_entry_sign: У вас недостаточно прав!', color=discord.Colour.red())
#        await ctx.send(embed=emb)

#Мини-игры:
@bot.command(aliases=["random"])
async def рандом(ctx, *, arg=None):
    if arg == None:
        rand = random.randint(0, 100)
        emb = discord.Embed(title=f'Выпало число: __{str(rand)}__')
        await ctx.send(embed=emb)
    elif arg != None:
        atr = arg.split('/ ')
        num = len(atr)
        rand = random.randint(0, num-1)
        emb = discord.Embed(title=f'Выпало: __{atr[rand]}__')
        await ctx.send(embed=emb)
@bot.command(aliases=["shootout"])
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
@bot.command(aliases=["duel"])
async def дуэль(ctx, user1, user2):
    await ctx.send('Шансы 50/50')
    win = random.randint(0, 100)
    if win < 50:
        await ctx.send('Выиграл ' + user1 + '!')
    elif win == 50:
        await ctx.send('Ничья!')
    else:
        await ctx.send('Выиграл ' + user2 + '!')
@bot.command(name="CookeGame", aliases=["CG", "cg"])
async def CookeGame(ctx):
    emb = discord.Embed(title='Игра "Печенька"', color=discord.Colour.orange())
    emb.add_field(name='Правила', value='Кто первый нажмёт на реакцию - победил!')
    mess = await ctx.send(embed=emb)
    tim = random.randint(0, 5)
    await asyncio.sleep(tim)
    for i in reversed(range(0, 4)):
        emb = discord.Embed(title=f'{i}')
        await mess.edit(embed=emb)
        tim = random.randint(0, 1)
        await asyncio.sleep(tim)
    global message_id
    emb = discord.Embed(description='**!ЖМИ :cookie: НИЖЕ!**', color=discord.Colour.red())
    await mess.edit(embed=emb)
    emoji = '\N{cookie}'
    await mess.add_reaction(emoji)
    message_id = mess.id
    def check(reaction, user):
        return str(reaction.emoji) == emoji and user != bot.user
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
        emb = discord.Embed(description=f'**Выиграл: __{user}__**', color=discord.Colour.gold())
        await mess.edit(embed=emb)
    except asyncio.TimeoutError:
        emb = discord.Embed(description=f'**Время вышло!\nНикто не поставил реакцию:cry:**', color=discord.Colour.blue())
        await mess.edit(embed=emb)


#Остальные команды:
@bot.command()
async def cocy(ctx):
    rand = random.randint(1, 100)
    if rand < 50:
        await ctx.send('Ну и соси :rage:')
    else:
        await ctx.send('Не в этот раз :smiling_imp: ')
@bot.command(aliases=["help"])
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
@bot.command(aliases=["commands"])
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
@bot.command(aliases=["avatar"])
async def аватар(ctx, member: discord.Member = None):
    if member == None:
        emb = discord.Embed(description=f'Неккоректные данные!')
        await ctx.send(embed=emb)
    elif member != None:
        emb = discord.Embed(title=f'Аватарка {member}')
        emb.set_image(url='{}'.format(member.avatar_url))
        await ctx.send(embed=emb)
@bot.command()
async def emb(ctx, title, color: discord.Colour = None, q: int = None, *, atr=None):
    if atr == None and q <= 1:
        await ctx.channel.purge(limit=1)
        emb = discord.Embed(title=f'{title}', color=color)
        await ctx.send(embed=emb)
    elif atr != None:
        atr = atr.split(' / ')
        n = 0
        i = 0
        await ctx.channel.purge(limit=1)
        emb = discord.Embed(title=f'{title}', color=color)
        if q > 1:
            name = 0
            value = 1
            inline = 2
            while i < q:
                emb.add_field(name=f'{atr[name]}', value=f'{atr[value]}', inline=atr[inline])
                name += 3
                value += 3
                inline += 3
                i += 1
            await ctx.send(embed=emb)
        else:
            nn = atr[n]
            nv = atr[n+1]
            ni = atr[n+2]
            emb.add_field(name=f'{nn}', value=f'{nv}', inline=ni)
            await ctx.send(embed=emb)
    # emb.add_field(name=f'{nn}', value=f'{nv}', inline=ni)
    # i += 1
    # await ctx.send(embed=emb)
@bot.command()
async def poll(ctx, *, atr):
    art = atr.split('\n')
    title = art[0]
    x = art[0]
    art.remove(x)
    des = '\n'.join(art)
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title=f'{title}', description=f'{des}', color=discord.Colour.orange())
    mess = await ctx.send(embed=emb)
    for polls in art:
        if polls.find('-'):
            poll = polls.split('-')
            emoji = poll[0].strip()
            await mess.add_reaction(emoji)
@bot.command(aliases=["top"])
async def топ(ctx, qua: int = 5):
    with open('data.json', 'r') as f:
        top = json.load(f)
    nam = []
    mon = []
    for member in top['money']:
        nam.append(top['money'][str(member)]['Name'])
        mon.append(top['money'][str(member)]['Money'])
    qu = len(nam)
    if qua > qu:
        qua = qu
    mon.sort(reverse=True)
    i = 0
    msg = ''
    while i < qu:
        for member in top['money']:
            if i >= qua:
                i += 1
                pass
            elif mon[i] == top['money'][str(member)]['Money']:
                if i <= 2:
                    msg += '**{0}. {1} — {2} {3}**\n'.format(i+1, top["money"][str(member)]["Name"], top["money"][str(member)]["Money"], bot.eco_emoji)
                if i > 2:
                    msg += '{0}. {1} — {2} {3}\n'.format(i+1, top["money"][str(member)]["Name"], top["money"][str(member)]["Money"], bot.eco_emoji)
                i += 1
            else:
                pass
    emb = discord.Embed(title=f'Список лидеров {bot.eco_emoji}', description=msg)
    await ctx.send(embed=emb)


#Деньги пользователей
@bot.command(aliases=["wages"])
async def зп(ctx):
    with open('data.json', 'r') as f:
        money = json.load(f)
    if not str(ctx.author.id) in money['money']:
        money['money'][str(ctx.author.id)] = {}
        money['money'][str(ctx.author.id)]['Money'] = 0
        money['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
    if not str(ctx.author.id) in queue:
        emb = discord.Embed(
            description=f'**{ctx.author}** Вы получили свои 150 {bot.eco_emoji}\nСледующее получение будет доступно только через 2 минуты')
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
@bot.command(aliases=["balance", "bal"])
async def баланс(ctx, member: discord.Member = None):
    with open('data.json', 'r') as f:
        balance = json.load(f)
    if not str(ctx.author.id) in balance['money']:
        balance['money'][str(ctx.author.id)] = {}
        balance['money'][str(ctx.author.id)]['Money'] = 0
        balance['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
        with open('data.json', 'w') as f:
            json.dump(balance, f)
    if member == None:
        emb = discord.Embed(description=f'У вас на счету {balance["money"][str(ctx.author.id)]["Money"]} {bot.eco_emoji}', color=discord.Colour.dark_green())
        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    elif str(member.id) == str(ctx.author.id):
        emb = discord.Embed(description=f'У вас на счету {balance["money"][str(ctx.author.id)]["Money"]} {bot.eco_emoji}', color=discord.Colour.dark_green())
        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    else:
        if not str(member.id) in balance['money']:
            balance['money'][str(member.id)] = {}
            balance['money'][str(member.id)]['Money'] = 0
            balance['money'][str(member.id)]['Name'] = str(member)
        emb = discord.Embed(description=f'У **{member}** на счету {balance["money"][str(member.id)]["Money"]} {bot.eco_emoji}', color=discord.Colour.dark_green())
        emb.set_author(name=member.name, icon_url=member.avatar_url)
        await ctx.send(embed=emb)


#Магазин ролей/предметов:
@bot.command(aliases=["shop"])
async def магазин(ctx, nam=None):
    with open('data.json', 'r') as f:
        shop = json.load(f)
    if nam == None:
        emb = discord.Embed(description=f'Выберите магазин, который хотите просмотреть введя:\n"**-магазин ролей**" либо "**-магазин предметов**"')
        await ctx.send(embed=emb)
    if nam == 'ролей' or nam == 'роль' or nam == 'role' or nam == 'roles':
        emb = discord.Embed(title="Магазин Ролей")
        for role in shop['shop']['Role']:
            emb.add_field(name=f'Цена: {shop["shop"]["Role"][role]["Cost"]} {bot.eco_emoji}', value=f'Роль: <@&{role}>\nКоличество: {shop["shop"]["Role"][role]["Quant"]}', inline=False)
        await ctx.send(embed=emb)
    if nam == 'предметов' or nam == 'предмет' or nam == 'item' or nam == 'items':
        emb = discord.Embed(title="Магазин Предметов")
        for user in shop['shop']['item']:
            for item in shop['shop']['item'][str(user)]:
                emb.add_field(name=f'Товар: {item}\n', value=f'**Цена: {shop["shop"]["item"][str(user)][item]["cost"]}** {bot.eco_emoji}\nКоличество: {shop["shop"]["item"][str(user)][item]["quant"]}\nВыставил: <@{user}>', inline=False)
        await ctx.send(embed=emb)
@bot.command(aliases=["buy-role", "купить-роль"])
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
@bot.command(aliases=["buy-item", "купить-предмет"])
async def купить_предмет(ctx, item, member: discord.Member=None):
    with open('data.json', 'r') as f:
        buyi = json.load(f)
    if not str(ctx.author.id) in buyi['money']:
        buyi['money'][str(ctx.author.id)] = {}
        buyi['money'][str(ctx.author.id)]['Money'] = 0
        buyi['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
    if not str(member.id) in buyi['money']:
        buyi['money'][str(member.id)] = {}
        buyi['money'][str(member.id)]['Money'] = 0
        buyi['money'][str(member.id)]['Name'] = str(member)
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
            emb = discord.Embed(description=f'Вы купили "{item}" в количестве {buyi["inv"][str(ctx.author.id)][item]["quanti"]} за {buyi["shop"]["item"][str(member.id)][item]["cost"]} {bot.eco_emoji}')
            del buyi['shop']['item'][str(member.id)][item]
            await ctx.send(embed=emb)
    with open('data.json', 'w') as f:
        json.dump(buyi, f)
@bot.command(aliases=["pay"])
async def заплатить(ctx, why, member: discord.Member, arg: int, name=None):
    with open('data.json', 'r') as f:
        money = json.load(f)
    if why == 'деньги' and name == None:
        if not str(member.id) in money['money']:
            money['money'][str(member.id)] = {}
            money['money'][str(member.id)]['Money'] = 0
        if money['money'][str(ctx.author.id)]['Money'] >= arg:
            emb = discord.Embed(description=f'**{ctx.author}** подарил **{member}** **{arg}** {bot.eco_emoji}')
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
@bot.command(aliases=["lot"])
async def лот(ctx, act, name, qu: int = None, cost: int = None):
    with open('data.json', 'r') as f:
        buyi = json.load(f)
    if (act == 'изменить' or act == 'change') and qu != None and cost == None:
        if not name in buyi['shop']['item'][str(ctx.author.id)]:
            emb = discord.Embed(description=f'Неккоректные данные')
            await ctx.send(embed=emb)
        if qu == None:
            emb = discord.Embed(description=f'Введите новую цену!')
            await ctx.send(embed=emb)
        else:
            buyi['shop']['item'][str(ctx.author.id)][name]['cost'] = qu
            emb = discord.Embed(description=f'Цена "{name}" была изменена\nТеперь она составляет **{buyi["shop"]["item"][str(ctx.author.id)][name]["cost"]} {bot.eco_emoji}**')
            await ctx.send(embed=emb)
    if (act == 'снять' or act == 'del') and qu == None and cost == None:
        if not name in buyi['shop']['item'][str(ctx.author.id)]:
            emb = discord.Embed(description=f'Неккоректные данные')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(description=f'Слот "{name}" был снят')
            await ctx.send(embed=emb)
            if not str(ctx.author.id) in buyi['inv']:
                buyi['inv'][str(ctx.author.id)] = {}
            if not name in buyi['inv'][str(ctx.author.id)]:
                buyi['inv'][str(ctx.author.id)][name] = {}
                buyi['inv'][str(ctx.author.id)][name]['quanti'] = buyi['shop']['item'][str(ctx.author.id)][name]['quant']
                del buyi['shop']['item'][str(ctx.author.id)][name]
            else:
                buyi['inv'][str(ctx.author.id)][name]['quanti'] += buyi['shop']['item'][str(ctx.author.id)][name]['quant']
                del buyi['shop']['item'][str(ctx.author.id)][name]
    if (act == 'выставить' or act == 'put') and cost != None and qu != None:
        if name in buyi['inv'][str(ctx.author.id)]:
            if buyi['inv'][str(ctx.author.id)][name]['quanti'] < qu:
                emb = discord.Embed(description=f'Вы пытаетесь выставить большее кол-во, чем имеете!')
                await ctx.send(embed=emb)
                exit
            if buyi['inv'][str(ctx.author.id)][name]['quanti'] > qu:
                buyi['inv'][str(ctx.author.id)][name]['quanti'] -= qu
                if not str(ctx.author.id) in buyi['shop']['item']:
                    buyi['shop']['item'][str(ctx.author.id)] = {}
                if not name in buyi['shop']['item'][str(ctx.author.id)]:
                    buyi['shop']['item'][str(ctx.author.id)][name] = {}
                    buyi['shop']['item'][str(ctx.author.id)][name]['cost'] = cost
                    buyi['shop']['item'][str(ctx.author.id)][name]['quant'] = qu
                    emb = discord.Embed(description=f'Вы выставили на продажу {qu} единиц "{name}" за общую стоимость {cost} {bot.eco_emoji}')
                    await ctx.send(embed=emb)
                    with open('data.json', 'w') as f:
                        json.dump(buyi, f)
                    exit
                else:
                    buyi['shop']['item'][str(ctx.author.id)][name]['cost'] += cost
                    buyi['shop']['item'][str(ctx.author.id)][name]['quant'] += qu
                    emb = discord.Embed(description=f'Вы добавили на продажу {qu} единиц "{name}" и добавили к стоимости {cost} {bot.eco_emoji}')
                    await ctx.send(embed=emb)
                    with open('data.json', 'w') as f:
                        json.dump(buyi, f)
                exit
            if buyi['inv'][str(ctx.author.id)][name]['quanti'] == qu:
                del buyi['inv'][str(ctx.author.id)][name]
                if not str(ctx.author.id) in buyi['shop']['item']:
                    buyi['shop']['item'][str(ctx.author.id)] = {}
                if not name in buyi['shop']['item'][str(ctx.author.id)]:
                    buyi['shop']['item'][str(ctx.author.id)][name] = {}
                    buyi['shop']['item'][str(ctx.author.id)][name]['cost'] = cost
                    buyi['shop']['item'][str(ctx.author.id)][name]['quant'] = qu
                    emb = discord.Embed(description=f'Вы выставили на продажу {qu} единиц "{name}" за общую стоимость {cost} {bot.eco_emoji}')
                    await ctx.send(embed=emb)
                    with open('data.json', 'w') as f:
                        json.dump(buyi, f)
                    exit
                else:
                    buyi['shop']['item'][str(ctx.author.id)][name]['cost'] += cost
                    buyi['shop']['item'][str(ctx.author.id)][name]['quant'] += qu
                    emb = discord.Embed(description=f'Вы добавили на продажу {qu} единиц "{name}" и добавили к стоимости {cost} {bot.eco_emoji}')
                    await ctx.send(embed=emb)
                    with open('data.json', 'w') as f:
                        json.dump(buyi, f)
                    exit
        else:
            emb = discord.Embed(description=f'Вы пытаетесь выставить предмет, которого нет у вас!')
            await ctx.send(embed=emb)
    with open('data.json', 'w') as f:
        json.dump(buyi, f)
@bot.command(aliases=["inv"])
async def инвентарь(ctx, member: discord.Member = None):
    with open('data.json', 'r') as f:
        invs = json.load(f)
    if member == None or str(member.id) == str(ctx.author.id):
        if not str(ctx.author.id) in invs['inv']:
            invs['inv'][str(ctx.author.id)] = {}
        emb = discord.Embed(title='Ваши предметы')
        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
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
@bot.command(name='stop', aliases=["стоп"], pass_context=True)
@has_permissions(administrator=True)
async def stop(ctx):
        await ctx.send('Ну ББ, KEKW')
        await bot.logout()
@bot.command(aliases=["clear"])
@has_permissions(administrator=True)
async def чистка(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    emb = discord.Embed(color=discord.Colour.dark_grey(), description='Было отчищенно ' + str(amount) + ' сообщений!')
    await ctx.send(embed=emb)
@bot.command(aliases=["spam"])
@commands.has_any_role("Повелитель")
async def шнюк(ctx, k, *, text):
    await ctx.channel.purge(limit=1)
    i = 0
    while i < int(k):
        await ctx.send(text)
        i += 1
@bot.command(aliases=["nuke"])
@commands.has_any_role("Повелитель")
async def нюк(ctx):
    await ctx.send('https://tenor.com/view/destory-eexplode-nuke-gif-6073338')
@bot.command()
@commands.is_owner()
async def say(ctx, *, text):
    await ctx.channel.purge(limit=1)
    await ctx.send(text)
@bot.command(aliases=["добавить-предмет", "add-item"])
@has_permissions(administrator=True)
async def добавить_предмет(ctx, name, qu: int, member: discord.Member = None):
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
@bot.command(aliases=["удалить-предмет", "del-item"])
@has_permissions(administrator=True)
async def удалить_предмет(ctx, name, qu=754325616, member: discord.Member = None):
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
@bot.command(aliases=["выставить-роль", "add-role"])
@has_permissions(administrator=True)
async def выставить_роль(ctx, role: discord.Role, cost: int, quant=1):
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
            await ctx.send(f':white_check_mark: Роль добавлена в магазин {role}')
        with open('data.json', 'w') as f:
            json.dump(add, f)
@bot.command(aliases=["удалить-роль", "del-role"])
@has_permissions(administrator=True)
async def удалить_роль(ctx, role: discord.Role, quant=None):
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
@bot.command(aliases=["добавить-деньги", "add-money"])
@has_permissions(administrator=True)
async def добавить_деньги(ctx, qu: int, member: discord.Member = None):
    if qu > 0:
        with open('data.json', 'r') as f:
            money = json.load(f)
        if str(member.id) == str(ctx.author.id):
            if not str(ctx.author.id) in money['money']:
                money['money'][str(ctx.author.id)] = {}
                money['money'][str(ctx.author.id)]['Money'] = 0
                money['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
            if str(member.id) in money['money']:
                money['money'][str(ctx.author.id)]['Money'] += qu
                emb = discord.Embed(description=f'Вы добавили на свой счёт {qu} {bot.eco_emoji}', color=discord.Colour.dark_green())
                await ctx.send(embed=emb)
        else:
            if not str(member.id) in money['money']:
                money['money'][str(member.id)] = {}
                money['money'][str(member.id)]['Money'] = 0
                money['money'][str(member.id)]['Name'] = str(member)
            if str(member.id) in money['money']:
                money['money'][str(member.id)]['Money'] += qu
                emb = discord.Embed(description=f'Вы добавили на счёт **{member}** {qu} {bot.eco_emoji}', color=discord.Colour.dark_green())
                await ctx.send(embed=emb)
        with open('data.json', 'w') as f:
            json.dump(money, f)
    else:
        emb = discord.Embed(description=f':no_entry_sign: Вы не можете добавить отрицательно/нулевое количество {bot.eco_emoji}', color=discord.Colour.red())
        await ctx.send(embed=emb)
@bot.command(aliases=["удалить-деньги", "del-money"])
@has_permissions(administrator=True)
async def удалить_деньги(ctx, qu: int, member: discord.Member = None):
    if qu > 0:
        with open('data.json', 'r') as f:
            money = json.load(f)
        if str(member.id) == str(ctx.author.id):
            if not str(ctx.author.id) in money['money']:
                money['money'][str(ctx.author.id)] = {}
                money['money'][str(ctx.author.id)]['Money'] = 0
                money['money'][str(ctx.author.id)]['Name'] = str(ctx.author)
            if str(member.id) in money['money']:
                money['money'][str(ctx.author.id)]['Money'] -= qu
                emb = discord.Embed(description=f'Вы удалили со своего счёта {qu} {bot.eco_emoji}', color=discord.Colour.dark_green())
                await ctx.send(embed=emb)
        else:
            if not str(member.id) in money['money']:
                money['money'][str(member.id)] = {}
                money['money'][str(member.id)]['Money'] = 0
                money['money'][str(member.id)]['Name'] = str(member)
            if str(member.id) in money['money']:
                money['money'][str(member.id)]['Money'] -= qu
                emb = discord.Embed(description=f'Вы удалили со счёта **{member}** {qu} {bot.eco_emoji}', color=discord.Colour.dark_green())
                await ctx.send(embed=emb)
        with open('data.json', 'w') as f:
            json.dump(money, f)
    else:
        emb = discord.Embed(description=f':no_entry_sign: Вы не можете удалить отрицательно/нулевое количество {bot.eco_emoji}', color=discord.Colour.red())
        await ctx.send(embed=emb)
@bot.command(aliases=["бан"])
@commands.has_any_role("Повелитель")
async def ban(ctx, member: discord.User = None, reason = None):
    mess = member.name
    if member == None or str(member.id) == str(ctx.author.id):
        emb = discord.Embed(description=f'<@{ctx.author.id}> Дурак совсем?')
        await ctx.send(embed=emb)
        exit
    if reason == None:
        reason = "по рофлу"
    emb = discord.Embed(description=f'Вы забанили **{mess}**\n Причина: __{reason}__')
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(embed=emb)
@bot.command(aliases=["разбан"])
@commands.has_any_role("Повелитель")
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    emb = discord.Embed(description=f'Вы разбанили {user.mention}')
    await ctx.send(embed=emb)
@bot.command(aliases=["setprefix", "prefixset", "pref"])
@commands.is_owner()
async def prefix(ctx, prefix):
    with open('data.json', 'r') as f:
        pref = json.load(f)
    if prefix != pref['servers'][str(ctx.guild.id)]:
        pref['servers'][str(ctx.guild.id)]['prefix'] = prefix
        with open('data.json', 'w') as f:
            json.dump(pref, f)
        emb = discord.Embed(description=f':white_check_mark: Вы сменили префикс на "**{pref["servers"][str(ctx.guild.id)]["prefix"]}**"')
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f':no_entry_sign: Префикс "**{pref["servers"][str(ctx.guild.id)]["prefix"]}**" уже используется')
        await ctx.send(embed=emb)
@bot.command(aliases=["ecoemoji"])
@commands.is_owner()
async def ecemoji(ctx, emoji):
    if not emoji == bot.eco_emoji:
        bot.eco_emoji = emoji
        emb = discord.Embed(description=f':white_check_mark: Эмодзи валюты был успешно изменён на {bot.eco_emoji} до конца сеанса')
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f'{bot.eco_emoji} уже используется в качестве обозначения валюты!')
        await ctx.send(embed=emb)

bot.run(settings['TOKEN'])
