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
    # await ctx.send('>>> Command: `!hp <con_modifier> <classA#/classB#/etc> [hp_mod1/hp_mod2/etc]`\n'
    await ctx.send('>>> Command: `!hp <con_modifier> <classA#/classB#/etc>`\n'
                   '*Note: parameters enclosed in <> are required; those enclosed in [] are optional.*\n\n'
                   'Basic usage: `!hp 3 fighter1/barb2/paladin1`\n\n'
                   # 'Advanced usage: `!hp 3 fighter1/barb2/paladin1 tough/hilldwarf`\n'
                   # 'Possible `hp_mods`: `tough`, `hilldwarf`, `axe` (berserker axe)\n'
                   'List of possible `classes`:\n'
                   '`barbarian`/`barb`, `bard`, `cleric`, `druid`, '
                   '`fighter`/`fight`, `monk`, `paladin`/`pally`, `ranger`, '
                   '`rogue`, `sorcerer`/`sorc`, `warlock`/`lock`, `wizard`/`wiz`\n'
                   )


@bot.command()
async def hptest(ctx, con_modifier: int, input_classes_and_levels: str, input_hp_mods: typing.Optional[str]):
    dnd_classes = ['barbarian', 'barb', 'bard', 'cleric', 'druid', 'fighter',
                   'fight', 'monk', 'paladin', 'pally', 'ranger', 'rogue',
                   'sorcerer', 'sorc', 'warlock', 'lock', 'wizard', 'wiz']
    no_error = True
    current_level = 1
    current_hp = 0

    regex = re.compile('([a-zA-Z]+)([0-9]+)')
    char_classes = input_classes_and_levels.lower().split('/')

    # if there are char_classes
    if char_classes:
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
                    await ctx.send(f'{ctx.author.mention}: Oof! `{dnd_class}` does not exist! '
                                   'Check out `!hphelp` for more information :D')
                    no_error = False
                    break

            # if does not follows word## pattern
            else:
                await ctx.send(f'{ctx.author.mention}: Oof! Double check your classes and levels (example `barb1/wiz3`)! '
                               'Check out `!hphelp` for more information :D')
                no_error = False
                break

        if no_error:
            await ctx.send(f'{ctx.author.mention}: A `{input_classes_and_levels}` character with a Constitution modifier of `{con_modifier}` has `{current_hp}` hit points.')

        no_error = True
        current_level = 1
        current_hp = 0

    # if no char_classes
    else:
        raise commands.MissingRequiredArgument


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
        await ctx.send(f'{ctx.author.mention}: Oof! Something is missing! '
                       'Check out `!hphelp` for more information :D')
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send(f'{ctx.author.mention}: Oof! What is the constitution modiifier?')


if __name__ == '__main__':
    bot.run(token)
