# bot.py
# import os
# import random
import re

from discord.ext import commands
# from dotenv import load_dotenv

# load_dotenv()
# token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='hp', help='Calculates HP.')
async def get_input(ctx, con_modifier: int, *char_classes):
    dnd_classes = ['barbarian', 'barb', 'bard', 'cleric', 'druid', 'fighter',
                   'fight', 'monk', 'paladin', 'pally', 'ranger', 'rogue',
                   'sorcerer', 'sorc', 'warlock', 'lock', 'wizard', 'wiz']
    no_error = True
    current_level = 1
    current_hp = 0

    regex = re.compile('([a-zA-Z]+)([0-9]+)')

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
                                get_max_hp(dnd_class) + con_modifier
                            current_level += 1
                            i += 1
                        # if not first level: avg_hd + con_modifier
                        else:
                            current_hp = current_hp + \
                                get_ave_hd(dnd_class) + con_modifier
                            current_level += 1
                            i += 1

                else:
                    await ctx.send(f'Oof! {dnd_class} does not exist!')
                    no_error = False
                    break
            else:
                await ctx.send('Oof! Double check your classes and levels (`class#`)! You can use the following: '
                               '`barbarian`, `barb`, `bard`, `cleric`, `druid`, `fighter`, '
                               '`fight`, `monk`, `paladin`, `pally`, `ranger`, `rogue`, '
                               '`sorcerer`, `sorc`, `warlock`, `lock`, `wizard`, `wiz`')
                no_error = False
                break

        if no_error:
            await ctx.send(f'A `{char_classes}` character with `{con_modifier}` CON modifier has `{current_hp}` hit points.')

        no_error = True
        current_level = 1
        current_hp = 0

    # if no char_classes
    else:
        await ctx.send('Oof!')


def get_max_hp(dnd_class):
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


def get_ave_hd(dnd_class):
    switcher = {
        'barbarian': 7,
        'barb': 7,
        'bard': 5,
        'cleric': 5,
        'druid': 5,
        'fighter': 6,
        'fight': 6,
        'monk': 5,
        'paladin': 6,
        'pally': 6,
        'ranger': 6,
        'rogue': 5,
        'sorcerer': 4,
        'sorc': 4,
        'warlock': 5,
        'lock': 5,
        'wizard': 4,
        'wiz': 4
    }
    return switcher.get(dnd_class, 0)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send('Missing CON_modifier parameter.')


if __name__ == '__main__':
    from secrets import DISCORD_TOKEN
    client.run(DISCORD_TOKEN)
