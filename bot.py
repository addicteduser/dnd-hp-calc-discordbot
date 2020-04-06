import os
import re
import math
import discord
import typing
from discord.ext import commands
from discord.utils import get

# for local development
# from secrets import DISCORD_TOKEN
# token = DISCORD_TOKEN

# for deployment
token = os.environ['DISCORD_TOKEN']
bot = commands.Bot(command_prefix='?',
                   case_insensitive=True,
                   description='A bot for calculating an AL D&D 5e character\'s hit points.',
                   help_command=None)

#######################
## DISCORD BOT START ##
#######################


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    print('Connected to the following Discord servers: ')
    for guild in bot.guilds:
        print(f' >> {guild.name}')


#########################
## DISCORD BOT LOGGING ##
#########################
@bot.event
async def on_guild_join(guild):
    print(f'Joined {guild.name}!')


@bot.event
async def on_guild_remove(guild):
    print(f'Left {guild.name}...')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f'Oof! {ctx.author.mention}, my friend, something is missing! '
                       'Check out `?hphelp` for more information. Also, I have a wife!')
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send(f'Oof! {ctx.author.mention}, my friend, what is the constitution modifier?')

    log_error(error, ctx.message.content)

##################
## BOT COMMANDS ##
##################


@bot.command()
async def hphelp(ctx):
    await ctx.send('Hello, my friend! I am Valron. '
                   'Below is a guide on how I can help you compute for your AL D&D 5e character\'s hit points. '
                   'If you want to help improve me, my source code (and server invite!) can be found here: '
                   'https://github.com/addicteduser/dnd-hp-calc-discordbot.\n'
                   '>>> **Command**\n'
                   '`?hp <con_modifier> <classA#/classB#/etc> [hp_mod1/hp_mod2/etc]`\n\n'
                   '**Basic usage example**\n'
                   '`?hp 3 fighter1/barb2/paladin1`\n\n'
                   '**Advanced usage example**\n'
                   '`?hp 3 fighter1/barb2/paladin1 tough/hilldwarf`\n\n'
                   '**List of possible `classes`**\n'
                   '`barbarian`/`barb`, `bard`, `cleric`, `druid`, '
                   '`fighter`/`fight`, `monk`, `paladin`/`pally`, `ranger`, '
                   '`rogue`, `sorcerer`/`sorc`/`draconicsorc`/`dracsorc`, '
                   '`warlock`/`lock`, `wizard`/`wiz`\n\n'
                   '**List of possible `hp_mods`**\n'
                   '`hilldwarf`/`hdwarf`/`hd`, `berserkeraxe`/`axe`/`ba`, `tough`/`t`'
                   )


@bot.command()
async def hp(ctx, con_modifier: int, input_classes_and_levels: str, input_hp_mods: typing.Optional[str] = None):
    dnd_classes = ['barbarian', 'barb', 'bard', 'cleric', 'druid', 'fighter',
                   'fight', 'monk', 'paladin', 'pally', 'ranger', 'rogue',
                   'sorcerer', 'sorc', 'draconicsorc', 'dracsorc',
                   'warlock', 'lock', 'wizard', 'wiz']
    hilldwarf_mods = ['hilldwarf', 'hdwarf', 'hd']
    berserker_axe_mods = ['berserkeraxe', 'axe', 'ba']
    tough_mods = ['tough', 't']
    hp_mods = hilldwarf_mods + berserker_axe_mods + tough_mods

    # flags
    no_error = True
    is_hilldwarf = False
    axe_attuned = False
    is_tough = False

    # character stats
    current_level = 0
    current_hp = 0

    regex = re.compile('([a-zA-Z]+)([0-9]+)')
    input_classes_and_levels = input_classes_and_levels.lower()
    char_classes = input_classes_and_levels.split('/')

    # if there are char_classes
    if char_classes:
        # for each char_class
        for char_class in char_classes:
            class_and_level = char_class.strip()
            match = re.match(regex, class_and_level)

            # if follows word## pattern
            if match:
                result = re.split(regex, class_and_level)
                dnd_class = result[1]
                level = int(result[2])

                # if dnd_class is in list of dnd_classes
                if dnd_class in dnd_classes:
                    i = 0
                    while i < level:
                        current_level += 1
                        i += 1

                        # if first level: max_hp + con_modifier
                        if current_level == 1:
                            current_hp = current_hp + \
                                get_hit_dice(dnd_class) + con_modifier

                        # if not first level: avg_hd + con_modifier
                        else:
                            avg_hit_dice = math.floor(
                                get_hit_dice(dnd_class) / 2) + 1
                            current_hp = current_hp + \
                                avg_hit_dice + con_modifier

                    # if dnd_class is a draconic sorcerer
                    if (dnd_class == 'draconicsorc' or dnd_class == 'dracsorc'):
                        current_hp = current_hp + level

                # if dnd_class does not exist
                else:
                    await ctx.send(f'Oof! {ctx.author.mention}, my friend, I don\'t know the `{dnd_class}` class! '
                                   'Check out `?hphelp` for more information. Also, I have a wife!')
                    log_error(f'Unknown `{dnd_class}` class.',
                              ctx.message.content)
                    no_error = False
                    break

            # if does not follows word## pattern
            else:
                await ctx.send(f'Oof! {ctx.author.mention}, my friend, double check your classes and levels (example `barb1/wiz3`)! '
                               'Check out `?hphelp` for more information. Also, I have a wife!')
                log_error('Does not follow the classA##/classB##/etc format.',
                          ctx.message.content)
                no_error = False
                break

    # if no char_classes
    else:
        raise commands.MissingRequiredArgument

    # if there are input_hp_mods
    if input_hp_mods:
        input_hp_mods = input_hp_mods.lower()
        char_hp_mods = input_hp_mods.split('/')

        # for each char_hp_mod
        for char_hp_mod in char_hp_mods:
            # if valid char_hp_mod
            if char_hp_mod in hp_mods:
                if char_hp_mod in hilldwarf_mods:
                    current_hp = current_hp + current_level
                    is_hilldwarf = True
                elif char_hp_mod in berserker_axe_mods:
                    current_hp = current_hp + current_level
                    axe_attuned = True
                elif char_hp_mod in tough_mods:
                    current_hp = current_hp + (current_level * 2)
                    is_tough = True
            # if not valid char_hp_mod
            else:
                await ctx.send(f'Oof! {ctx.author.mention}, my friend, I don\'t know the `{char_hp_mod}` HP modifier! '
                               'Check out `?hphelp` for more information. Also, I have a wife!')
                log_error(f'Unknown `{char_hp_mod}` HP modifier.',
                          ctx.message.content)
                no_error = False
                break

    if no_error:
        if current_level > 20:
            bot_reply = f'Oof! {ctx.author.mention}, my friend, you have a level `{current_level}` character? My wife says to double check its levels! But if you really want to know, a '
        else:
            bot_reply = f'{ctx.author.mention}, my friend, a '

        if is_hilldwarf:
            bot_reply = bot_reply + '`hilldwarf` '

        bot_reply = bot_reply + f'`{input_classes_and_levels}` character '

        if axe_attuned:
            bot_reply = bot_reply + '`attuned to a berserker axe` '

        bot_reply = bot_reply + \
            f'with a Constitution modifier of `{con_modifier}` '

        if is_tough:
            bot_reply = bot_reply + 'and `tough feat` '

        bot_reply = bot_reply + f'has `{current_hp}` hit points.'

        if((ctx.guild.name == 'Natural Newbie') and (con_modifier < 0)):
            summon = get(ctx.guild.members, name='corgibutt')
            bot_reply = bot_reply + '\n\nOof! You have a negative Constitution modifier! ' + \
                f'My wife tells me that I should summon {summon.mention}!'

        await ctx.send(bot_reply)

    # reset values
    no_error = True
    is_hilldwarf = False
    axe_attuned = False
    is_tough = False
    current_level = 1
    current_hp = 0


def log_error(error, msg):
    print(f'ERROR: {error}')
    print(f'COMMAND: {msg}')


def get_hit_dice(dnd_class):
    switcher = {
        'barbarian': 12,
        'barb': 12,
        'bard': 8,
        'cleric': 8,
        'druid': 8,
        'fighter': 10,
        'fight': 10,
        'monk': 8,
        'paladin': 10,
        'pally': 10,
        'ranger': 10,
        'rogue': 8,
        'sorcerer': 6,
        'sorc': 6,
        'draconicsorc': 6,
        'dracsorc': 6,
        'warlock': 8,
        'lock': 8,
        'wizard': 6,
        'wiz': 6
    }
    return switcher.get(dnd_class, 0)


if __name__ == '__main__':
    bot.run(token)
