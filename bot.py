import os
import re
import math
import discord
import typing
from discord.ext import commands

# for local development
from secrets import DISCORD_TOKEN
token = DISCORD_TOKEN

# for deployment
# token = os.environ['DISCORD_TOKEN']
bot = commands.Bot(command_prefix='!',
                   case_insensitive=True,
                   description='A bot for calculating an AL D&D 5e character\'s hit points.',
                   help_command=None)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command()
async def hphelp(ctx):
    await ctx.send('Hello, my friend! I am Valron. Here is a guide on how I can help you compute for your hit points.\n'
                   '>>> **Command**\n'
                   '`!hp <con_modifier> <classA#/classB#/etc> [hp_mod1/hp_mod2/etc]`\n\n'
                   '**Basic usage**\n'
                   '`!hp 3 fighter1/barb2/paladin1`\n\n'
                   '**Advanced usage**\n'
                   '`!hp 3 fighter1/barb2/paladin1 tough/hilldwarf`\n\n'
                   '**List of possible `hp_mods`**\n'
                   '`hilldwarf`/`hdwarf`/`hd`, `berserkeraxe`/`axe`/`ba`, `tough`/`t`\n\n'
                   '**List of possible `classes`**\n'
                   '`barbarian`/`barb`, `bard`, `cleric`, `druid`, '
                   '`fighter`/`fight`, `monk`, `paladin`/`pally`, `ranger`, '
                   '`rogue`, `sorcerer`/`sorc`, `warlock`/`lock`, `wizard`/`wiz`'
                   )


@bot.command()
async def hptest(ctx, con_modifier: int, input_classes_and_levels: str, input_hp_mods: typing.Optional[str] = None):
    dnd_classes = ['barbarian', 'barb', 'bard', 'cleric', 'druid', 'fighter',
                   'fight', 'monk', 'paladin', 'pally', 'ranger', 'rogue',
                   'sorcerer', 'sorc', 'warlock', 'lock', 'wizard', 'wiz']
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
    current_level = 1
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
                        print('loop')
                        # if first level: max_hp + con_modifier
                        if current_level == 1:
                            current_hp = current_hp + \
                                get_hit_dice(dnd_class) + con_modifier
                            current_level += 1
                            i += 1
                        # if not first level: avg_hd + con_modifier
                        else:
                            avg_hit_dice = math.floor(
                                get_hit_dice(dnd_class) / 2) + 1
                            current_hp = current_hp + \
                                avg_hit_dice + con_modifier
                            current_level += 1
                            i += 1

                # if dnd_class does not exist
                else:
                    await ctx.send(f'Oof! {ctx.author.mention}, my friend, I don\'t know the `{dnd_class}` class! '
                                   'Check out `!hphelp` for more information.')
                    no_error = False
                    break

            # if does not follows word## pattern
            else:
                await ctx.send(f'Oof! {ctx.author.mention}, my friend, double check your classes and levels (example `barb1/wiz3`)! '
                               'Check out `!hphelp` for more information.')
                no_error = False
                break

    # if no char_classes
    else:
        raise commands.MissingRequiredArgument

    # if there are input_hp_mods
    if input_hp_mods:
        input_hp_mods = input_hp_mods.lower()
        char_hp_mods = input_hp_mods.split('/')
        current_level = current_level - 1

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
                               'Check out `!hphelp` for more information.')
                no_error = False
                break

    if no_error:
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

        await ctx.send(bot_reply)
        print(bot_reply)

    # reset values
    no_error = True
    is_hilldwarf = False
    axe_attuned = False
    is_tough = False
    current_level = 1
    current_hp = 0


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
        'warlock': 8,
        'lock': 8,
        'wizard': 6,
        'wiz': 6
    }
    return switcher.get(dnd_class, 0)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f'Oof! {ctx.author.mention}, my friend, something is missing! '
                       'Check out `!hphelp` for more information :D')
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send(f'Oof! {ctx.author.mention}, my friend, what is the constitution modiifier?')


if __name__ == '__main__':
    bot.run(token)
