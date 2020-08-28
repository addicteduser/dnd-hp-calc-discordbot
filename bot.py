import os
import re
import math
import discord
import typing
import time
from discord.ext import commands
from discord.utils import get
import helper

# for local development
from secrets import DISCORD_TOKEN
token = DISCORD_TOKEN

# for deployment
# token = os.environ['DISCORD_TOKEN']
bot = commands.Bot(command_prefix='??',
                   case_insensitive=True,
                   description='A bot for calculating an AL D&D 5e character\'s hit points.',
                   help_command=None)

#######################
## DISCORD BOT START ##
#######################


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    # print('Connected to the following Discord servers: ')
    # for guild in bot.guilds:
    #     print(f' >> {guild.name}')

    print(f'Connected to {len(bot.guilds)} Discord servers!')


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
                       'My wife says to use `?help` for more information.')
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send(f'Oof! {ctx.author.mention}, my friend, what is the constitution modifier?')

    log_error(error, ctx.message.content)


##################
## BOT COMMANDS ##
##################
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="",
                          url="https://github.com/addicteduser/dnd-hp-calc-discordbot",
                          description="Hello, my friend! I am Valron. Below is a guide on how I can help you compute for your AL D&D 5e character's hit points.",
                          color=0x1abc9c)
    embed.set_author(name="Valron the HP Calculator",
                     url="https://github.com/addicteduser/dnd-hp-calc-discordbot",
                     icon_url="https://i.imgur.com/0bByXQ4.png")
    embed.set_thumbnail(url="https://i.imgur.com/0bByXQ4.png")
    embed.add_field(name="Command",
                    value="`?hp <con_modifier> <classA#/classB#/etc> [hp_mod1/hp_mod2/etc]`",
                    inline=False)
    embed.add_field(name="Example",
                    value="`?hp 3 fighter1/barb2/paladin1`",
                    inline=False)
    embed.add_field(name="Example with HP modifiers",
                    value="`?hp 3 fighter1/barb2/paladin1 tough/hilldwarf`",
                    inline=False)
    embed.set_footer(
        text='?options - to see the list of supported classes and HP modifiers\n'
             '?links - to view some helpful links')
    await ctx.send(embed=embed)


@bot.command()
async def options(ctx):
    embed = discord.Embed(title="",
                          url="https://github.com/addicteduser/dnd-hp-calc-discordbot",
                          description="Hello, my friend! I am Valron. Here are the supported classes and HP modifiers for your reference.",
                          color=0x1abc9c)
    embed.set_author(name="Valron the HP Calculator",
                     url="https://github.com/addicteduser/dnd-hp-calc-discordbot",
                     icon_url="https://i.imgur.com/0bByXQ4.png")
    embed.set_thumbnail(url="https://i.imgur.com/0bByXQ4.png")
    embed.add_field(name="List of supported classes",
                    value='- `artificer` (`art`, `a`)\n'
                          '- `barbarian` (`barb`, `bb`)\n'
                          '- `bard` (`bd`)\n'
                          '- `cleric` (`cl`, `c`)\n'
                          '- `druid` (`dr`, `d`)\n'
                          '- `fighter` (`fight`, `f`)\n'
                          '- `monk` (`mk`, `m`)\n'
                          '- `paladin` (`pally`, `p`)\n'
                          '- `ranger` (`ra`)\n'
                          '- `rogue` (`ro`)\n'
                          '- `sorcerer` (`sorc`, `s`)\n'
                          '- `draconicsorcerer` (`draconicsorc`, `dracsorc`, `ds`)\n'
                          '- `warlock` (`lock`, `wr`)\n'
                          '- `wizard` (`wiz`, `wz`)',
                    inline=False)
    embed.add_field(name="List of supported HP modifiers",
                    value='- `hilldwarf` (`hdwarf`, `hd`)\n'
                          '- `berserkeraxe` (`axe`, `ba`)\n'
                          '- `tough` (`t`)',
                    inline=False)
    embed.set_footer(
        text='?help - main help command\n'
             '?links - to view some helpful links')
    await ctx.send(embed=embed)


@bot.command()
async def links(ctx):
    embed = discord.Embed(title="",
                          url="https://github.com/addicteduser/dnd-hp-calc-discordbot",
                          description="Hello, my friend! I am Valron. My wife has compiled a list of helpful links for you.",
                          color=0x1abc9c)
    embed.set_author(name="Valron the HP Calculator",
                     url="https://github.com/addicteduser/dnd-hp-calc-discordbot",
                     icon_url="https://i.imgur.com/0bByXQ4.png")
    embed.set_thumbnail(url="https://i.imgur.com/0bByXQ4.png")
    embed.add_field(name="Invite me to your server with this link",
                    value="[Click me!](https://discordapp.com/api/oauth2/authorize?client_id=666625461811413008&permissions=11264&scope=bot)",
                    inline=False)
    embed.add_field(name="Find out what's new with me from the support discord server",
                    value="[Click me!](https://discord.gg/waCBQuD)",
                    inline=False)
    embed.add_field(name="See how I was made",
                    value="[Click me!](https://github.com/addicteduser/dnd-hp-calc-discordbot)",
                    inline=False)
    embed.add_field(name="Want to support me and my wife?",
                    value="[Click me!](https://paypal.me/addicteduser)",
                    inline=False)
    embed.set_footer(
        text='?help - main help command\n'
             '?options - to see the list of supported classes and HP modifiers')
    await ctx.send(embed=embed)


@bot.command()
async def hp(ctx, con_modifier: int, input_classes_and_levels: str, input_hp_mods: typing.Optional[str] = None):
    # await ctx.send(get_bot_reply(con_modifier, input_classes_and_levels, input_hp_mods))
    tic = time.perf_counter()
    ###############
    ## CONSTANTS ##
    ###############
    dnd_classes = helper.get_aliases()
    hilldwarf_mods = ['hilldwarf', 'hdwarf', 'hd']
    berserker_axe_mods = ['berserkeraxe', 'axe', 'ba']
    tough_mods = ['tough', 't']
    hp_mods = hilldwarf_mods + berserker_axe_mods + tough_mods

    ###########
    ## FLAGS ##
    ###########
    no_error = True
    is_hilldwarf = False
    axe_attuned = False
    is_tough = False

    #####################
    ## CHARACTER STATS ##
    #####################
    current_classes_and_levels = []
    current_level = 0
    current_hp = 0

    #########################
    ## BASE HP CALCULATION ##
    #########################
    # Regex pattern for word##
    regex = re.compile('([a-zA-Z]+)([0-9]+)')
    # List of word##
    parsed_classes_and_levels = input_classes_and_levels.lower().split('/')

    # If there are parsed_classes_and_levels
    if parsed_classes_and_levels:
        # Compute for the HP of each class
        for parsed_class_and_level in parsed_classes_and_levels:
            class_and_level = parsed_class_and_level.strip()

            # If it follows word## pattern
            if re.match(regex, class_and_level):
                result = re.split(regex, class_and_level)
                matched_dnd_class = result[1]
                matched_level = int(result[2])

                # If matched_dnd_class exists in list of supported D&D classes
                dnd_class = helper.get_class(matched_dnd_class)
                if dnd_class:
                    # Track class name and level
                    current_classes_and_levels.append(
                        (dnd_class.name, matched_level))

                    avg_hit_dice = math.floor(dnd_class.hit_die / 2) + 1

                    # For the base class
                    if current_level == 0:
                        # On 1st level: max_hit_die + con_modifier
                        current_hp = current_hp + \
                            dnd_class.hit_die + con_modifier
                        # On every level above 1st: avg_hit_dice + con_modifier
                        current_hp = current_hp + \
                            ((avg_hit_dice + con_modifier) * (matched_level - 1))

                    # On every level above 1st: avg_hit_dice + con_modifier
                    else:
                        current_hp = current_hp + \
                            ((avg_hit_dice + con_modifier) * matched_level)

                    # If matched_dnd_class is a Draconic Sorcerer
                    if dnd_class.name == 'Draconic Sorcerer':
                        current_hp = current_hp + matched_level

                    current_level = current_level + matched_level

                # If matched_dnd_class does not exist in list of supported D&D classes
                else:
                    await ctx.send(f'Oof! {ctx.author.mention}, my friend, I don\'t know the `{matched_dnd_class}` class! '
                                   'My wife says to use `?help` for more information.')
                    log_error(f'Unknown `{dnd_class}` class.',
                              ctx.message.content)
                    no_error = False
                    break

            # If it does not follow word## pattern
            else:
                await ctx.send(f'Oof! {ctx.author.mention}, my friend, kindly check your classes and levels! '
                               'It must look something like this `barb1/wizard2`. '
                               'My wife says to use `?help` for more information.')
                log_error('Does not follow the classA##/classB##/etc format.',
                          ctx.message.content)
                no_error = False
                break

    # If there are no parsed_classes_and_levels
    else:
        raise commands.MissingRequiredArgument

    #############################
    ## HP MODIFIER CALCULATION ##
    #############################
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
                               'My wife says to use `?help` for more information.')
                log_error(f'Unknown `{char_hp_mod}` HP modifier.',
                          ctx.message.content)
                no_error = False
                break

    #######################
    ## BOT REPLY BUILDER ##
    #######################
    if no_error:
        if current_level > 20:
            bot_reply = f'Oof! {ctx.author.mention}, my friend, you have a level `{current_level}` character? '
            'My wife says to double check its levels! But if you really want to know, a '
        else:
            bot_reply = f'{ctx.author.mention}, my friend, a '

        if is_hilldwarf:
            bot_reply = bot_reply + '`Hill Dwarf` '

        bot_reply = bot_reply + \
            f'`{helper.classes_and_levels_builder(current_classes_and_levels)}` character '

        if axe_attuned:
            bot_reply = bot_reply + '`attuned to a Berserker Axe` '

        bot_reply = bot_reply + \
            f'with a Constitution modifier of `{con_modifier}` '

        if is_tough:
            bot_reply = bot_reply + 'and `Tough feat` '

        bot_reply = bot_reply + f'has `{current_hp}` hit points.'

        # On NN server, summon corgi when there is negative con
        if((ctx.guild.name == 'Natural Newbie') and (con_modifier < 0)):
            summon = get(ctx.guild.members, name='corgibutt')
            bot_reply = bot_reply + '\n\nOof! You have a negative Constitution modifier! ' + \
                f'My wife tells me that I should summon {summon.mention}!'

        ####################
        ## SEND BOT REPLY ##
        ####################
        await ctx.send(bot_reply)

    toc = time.perf_counter()
    print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")


def log_error(error, msg):
    print(f'ERROR: {error}')
    print(f'COMMAND: {msg}')


if __name__ == '__main__':
    bot.run(token)
