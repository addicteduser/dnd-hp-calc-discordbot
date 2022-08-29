"""D&D HP Calculator Bot

This is the entry point of the application.
"""

# pylint: disable=C0103, W0622, E0237, R0913

import asyncio
import math
import os
import re

# import time
import typing

import disnake
from disnake.errors import HTTPException
from disnake.ext import commands
from disnake.utils import get
from dotenv import load_dotenv
from utils import constants, helper
from utils.classes import Flags

# Load environment variables
load_dotenv()

command_prefix = commands.when_mentioned
description = "A bot for calculating your D&D 5e character's average hit points."
intents = disnake.Intents.default()
bot = commands.Bot(
    case_insensitive=True,
    command_prefix=command_prefix,
    description=description,
    help_command=None,
    intents=intents,
)


##################
## HELP COMMAND ##
##################
async def build_help_embed():
    """Build the embed for the `help` command"""

    embed = helper.embed_builder(
        bot.user.name,
        "Hello, my friend! I am Valron. Below is a guide on "
        + "how I can help you compute for your AL D&D 5e character's hit points.",
    )
    embed.add_field(
        name="Command",
        value="`/hp <con_modifier> <classA#/classB#/etc> [hp_mod1/hp_mod2/etc]`",
        inline=False,
    )
    embed.add_field(name="Single Class Example", value="`/hp 3 fighter1`", inline=False)
    embed.add_field(
        name="Multiclass Example", value="`/hp 3 fighter1/barb2/paladin1`", inline=False
    )
    embed.add_field(
        name="Example with HP modifiers",
        value="`/hp 3 fighter1/barb2/paladin1 tough/hilldwarf`",
        inline=False,
    )
    embed.set_footer(
        text="/options - to see the list of supported classes and HP modifiers\n"
        + "/links - to view some helpful links"
    )

    return embed


@bot.command()
async def help(ctx: commands.Context):
    """Show a guide on how to use Valron"""
    embed = await build_help_embed()
    await bot_typing(ctx, 1)
    await ctx.send(embed=embed)


@bot.slash_command()
async def help(inter: disnake.CommandInteraction):
    """Show a guide on how to use Valron"""
    embed = await build_help_embed()
    await inter.send(embed=embed)


#####################
## OPTIONS COMMAND ##
#####################
async def build_options_embed():
    """Build the embed for the `options` command"""
    embed = helper.embed_builder(
        bot.user.name,
        "Hello, my friend! I am Valron. Here are the supported "
        + "classes and HP modifiers for your reference",
    )
    embed.add_field(
        name="List of supported classes",
        value=helper.alias_builder(constants.DND_ALIASES()),
        inline=False,
    )
    embed.add_field(
        name="List of supported HP modifiers",
        value=helper.alias_builder(constants.HP_MOD_ALIASES()),
        inline=False,
    )
    embed.set_footer(
        text="/help - main help command\n" + "/links - to view some helpful links"
    )

    return embed


@bot.command()
async def options(ctx: commands.Context):
    """Show list of supported classes and HP modifiers"""
    embed = await build_options_embed()
    await bot_typing(ctx, 1)
    await ctx.send(embed=embed)


@bot.slash_command()
async def options(inter: disnake.CommandInteraction):
    """Show list of supported classes and HP modifiers"""
    embed = await build_options_embed()
    await inter.send(embed=embed)


###################
## LINKS COMMAND ##
###################
async def build_links_embed():
    """Build the embed for the `links` command"""
    embed = helper.embed_builder(
        bot.user.name,
        "Hello, my friend! I am Valron. My wife has compiled a "
        + "list of helpful links for you.",
    )
    embed.add_field(
        name="Invite me to your server with this link",
        value=f"[Click me!]({constants.DISCORD_INVITE_LINK})",
        inline=False,
    )
    embed.add_field(
        name="Find out what's new with me from the support discord server",
        value=f"[Click me!]({constants.SUPPORT_SERVER_LINK})",
        inline=False,
    )
    embed.add_field(
        name="See how I was made",
        value=f"[Click me!]({constants.GITHUB_LINK})",
        inline=False,
    )
    embed.add_field(
        name="Want to support me and my wife?",
        value=f"Click any of these: [PayPal]({constants.PAYPAL_LINK}) "
        + f"| [Ko-Fi]({constants.KOFI_LINK}) | [GCash]({constants.GCASH_QR_CODE})",
        inline=False,
    )
    embed.set_footer(
        text="/help - main help command\n"
        + "/options - to see the list of supported classes and HP modifiers"
    )

    return embed


@bot.command()
async def links(ctx: commands.Context):
    """Show invite link and means to support Valron's development"""
    embed = await build_links_embed()
    await bot_typing(ctx, 1)
    await ctx.send(embed=embed)


@bot.slash_command()
async def links(inter: disnake.CommandInteraction):
    """Show invite link and means to support Valron's development"""
    embed = await build_links_embed()
    await inter.send(embed=embed)


@bot.slash_command()
async def hp(
    inter: disnake.CommandInteraction,
    con_modifier: int,
    input_classes_and_levels: str,
    input_hp_mods: str = None,
):
    """Calculate my character's HP"""
    # tic = time.perf_counter()

    # Parse input
    (classes_and_levels, flags) = await parse_input(
        input_classes_and_levels, input_hp_mods, inter
    )

    # Get base HP
    (partial_hp, total_level) = calculate_base_hp(classes_and_levels, con_modifier)

    # Apply HP modifiers
    final_hp = apply_hp_mods(partial_hp, total_level, flags)

    # Send bot reply
    if flags.no_error:
        bot_reply = bot_reply_builder(
            con_modifier, classes_and_levels, total_level, final_hp, flags, inter
        )
        await inter.send(bot_reply)

    # toc = time.perf_counter()
    # print(f"Performance: {toc - tic:0.4f} seconds")


##################
## BOT COMMANDS ##
##################
# @bot.command()
# async def help2(ctx):
#     """Displays an embed on how to use the bot.

#     Args:
#         ctx (discord.ext.commands.Context): See discordpy docs.

#     Invoked via: ?help

#     """
#     embed = helper.embed_builder(
#         bot.user.name,
#         "Hello, my friend! I am Valron. Below is a guide on "
#         + "how I can help you compute for your AL D&D 5e character's hit points.",
#     )
#     embed.add_field(
#         name="Command",
#         value="`?hp <con_modifier> <classA#/classB#/etc> [hp_mod1/hp_mod2/etc]`",
#         inline=False,
#     )
#     embed.add_field(name="Single Class Example", value="`?hp 3 fighter1`", inline=False)
#     embed.add_field(
#         name="Multiclass Example", value="`?hp 3 fighter1/barb2/paladin1`", inline=False
#     )
#     embed.add_field(
#         name="Example with HP modifiers",
#         value="`?hp 3 fighter1/barb2/paladin1 tough/hilldwarf`",
#         inline=False,
#     )
#     embed.set_footer(
#         text="?options - to see the list of supported classes and HP modifiers\n"
#         "?links - to view some helpful links"
#     )
#     await bot_typing(ctx, 1)
#     await ctx.send(embed=embed)


# @bot.command()
# async def options(ctx):
#     """Displays an embed regarding the supported classes and HP modifiers.

#     Args:
#         ctx (discord.ext.commands.Context): See discordpy docs.

#     Invoked via: ?options

#     """
#     embed = helper.embed_builder(
#         bot.user.name,
#         "Hello, my friend! I am Valron. Here are the supported "
#         + "classes and HP modifiers for your reference",
#     )
#     embed.add_field(
#         name="List of supported classes",
#         value=helper.alias_builder(constants.DND_ALIASES()),
#         inline=False,
#     )
#     embed.add_field(
#         name="List of supported HP modifiers",
#         value=helper.alias_builder(constants.HP_MOD_ALIASES()),
#         inline=False,
#     )
#     embed.set_footer(
#         text="?help - main help command\n" "?links - to view some helpful links"
#     )
#     await bot_typing(ctx, 1)
#     await ctx.send(embed=embed)


# @bot.command()
# async def links(ctx):
#     """Displays an embed showing various links.

#     Args:
#         ctx (discord.ext.commands.Context): See discordpy docs.

#     Invoked via: ?links

#     """
#     embed = helper.embed_builder(
#         bot.user.name,
#         "Hello, my friend! I am Valron. My wife has compiled a "
#         + "list of helpful links for you.",
#     )
#     embed.add_field(
#         name="Invite me to your server with this link",
#         value=f"[Click me!]({constants.DISCORD_INVITE_LINK})",
#         inline=False,
#     )
#     embed.add_field(
#         name="Find out what's new with me from the support discord server",
#         value=f"[Click me!]({constants.SUPPORT_SERVER_LINK})",
#         inline=False,
#     )
#     embed.add_field(
#         name="See how I was made",
#         value=f"[Click me!]({constants.GITHUB_LINK})",
#         inline=False,
#     )
#     embed.add_field(
#         name="Want to support me and my wife?",
#         value=f"Click any of these: [PayPal]({constants.PAYPAL_LINK}) "
#         + f"| [Ko-Fi]({constants.KOFI_LINK}) | [GCash]({constants.GCASH_QR_CODE})",
#         inline=False,
#     )
#     embed.set_footer(
#         text="?help - main help command\n"
#         "?options - to see the list of supported classes and HP modifiers"
#     )
#     await bot_typing(ctx, 1)
#     await ctx.send(embed=embed)


# @bot.command()
# async def hp(
#     ctx,
#     con_modifier: int,
#     input_classes_and_levels: str,
#     input_hp_mods: typing.Optional[str] = None,
# ):
#     """Shows the formatted string showing the classes, levels, HP mods, and calculated hit points.

#     Args:
#         ctx (discord.ext.commands.Context): See discordpy docs.
#         con_modifier (int): The constitution modifer.
#         input_classes_and_levels (str): The input classes and levels.
#         input_hp_mods (str): The input HP modifiers.

#     Invoked via: ?hp con_modifier input_classes_and_levels input_hp_mods

#     """
#     # tic = time.perf_counter()

#     # Parse input
#     (classes_and_levels, flags) = await parse_input(
#         input_classes_and_levels, input_hp_mods, ctx
#     )

#     # Get base HP
#     (partial_hp, total_level) = calculate_base_hp(classes_and_levels, con_modifier)

#     # Apply HP modifiers
#     final_hp = apply_hp_mods(partial_hp, total_level, flags)

#     # Send bot reply
#     if flags.no_error:
#         bot_reply = bot_reply_builder(
#             con_modifier, classes_and_levels, total_level, final_hp, flags, ctx
#         )
#         await bot_typing(ctx, 1)
#         await ctx.send(bot_reply)

#     # toc = time.perf_counter()
#     # print(f"Performance: {toc - tic:0.4f} seconds")


######################
## HELPER FUNCTIONS ##
######################
async def parse_input(
    input_classes_and_levels, input_hp_mods, inter: disnake.CommandInteraction = None
):
    """Parses the input_classes_and_levels and input_hp_mods.

    Args:
        input_classes_and_levels (str): The input classes and levels.
        input_hp_mods (str): The input HP modifiers.
        ctx (discord.ext.commands.Context): See discordpy docs.

    Returns:
        (list(Class, int), Flags): The first one is a list of tuples
            wherein each element is the Class and level. The second
            is the collection of HP modifier flags.

    """
    flags = await parse_input_hp_mods(input_hp_mods, inter)
    return await parse_input_classes_and_levels(input_classes_and_levels, flags, inter)


async def parse_input_hp_mods(input_hp_mods, inter: disnake.CommandInteraction = None):
    """Parses the input_hp_mods.

    Args:
        input_hp_mods (str): The input HP modifiers.
        ctx (discord.ext.commands.Context): See discordpy docs.

    Returns:
        Flags: The collection of HP modifier flags.

    """
    flags = Flags(True, False, False, False)

    # If there are input_hp_mods
    if input_hp_mods:
        input_hp_mods = input_hp_mods.lower()
        char_hp_mods = input_hp_mods.split("/")

        # For each char_hp_mod
        for char_hp_mod in char_hp_mods:

            # Check if valid char_hp_mod
            if char_hp_mod in constants.HP_MODS():
                if char_hp_mod in constants.HILLDWARF_MODS():
                    flags.is_hilldwarf = True
                elif char_hp_mod in constants.BERSERKER_AXE_MODS():
                    flags.axe_attuned = True
                elif char_hp_mod in constants.TOUGH_MODS():
                    flags.is_tough = True

            # If not valid char_hp_mod
            else:
                unknown = f"`{char_hp_mod}` HP modifier"

                if inter:
                    await inter.send((helper.valron_doesnt_know(inter, unknown)))

                flags.no_error = False
                break

    return flags


async def parse_input_classes_and_levels(
    input_classes_and_levels, flags, inter: disnake.CommandInteraction = None
):
    """Parses the input_classes_and_levels.

    Args:
        input_classes_and_levels (str): The input classes and levels.
        flags (Flags): The collection of HP modifier flags.
        ctx (discord.ext.commands.Context): See discordpy docs.

    Returns:
        (list(Class, int), Flags): The first one is a list of tuples
            wherein each element is the Class and level. The second
            is the collection of HP modifier flags.

    """
    classes_and_levels = []

    # List of word##
    parsed_classes_and_levels = input_classes_and_levels.lower().split("/")

    # If there are parsed_classes_and_levels
    if parsed_classes_and_levels:

        # For each parsed_class_and_level, get class and level
        for parsed_class_and_level in parsed_classes_and_levels:
            class_and_level = parsed_class_and_level.strip()

            # If it follows word## pattern
            regex = re.compile("([a-zA-Z]+)([0-9]+)")
            if re.match(regex, class_and_level):
                result = re.split(regex, class_and_level)
                matched_dnd_class = result[1]
                matched_level = int(result[2])

                # If matched_dnd_class exists in list of supported D&D classes
                dnd_class = helper.get_class(matched_dnd_class)
                if dnd_class:
                    # Track class name and level
                    classes_and_levels.append((dnd_class, matched_level))
                else:
                    unknown = f"`{matched_dnd_class}` class"

                    if inter:
                        await inter.send((helper.valron_doesnt_know(inter, unknown)))

                    flags.no_error = False
                    break

            # If it does not follow word## pattern
            else:
                if inter:
                    await inter.send(
                        f"Oof! {inter.author.mention}, my friend, "
                        "kindly check your classes and levels! "
                        "It must look something like this `barb1/wizard2`. "
                        "My wife says to use `?help` for more information."
                    )

                flags.no_error = False
                break

    # If there are no parsed_classes_and_levels
    else:
        raise commands.MissingRequiredArgument

    return (classes_and_levels, flags)


async def bot_typing(ctx, time):
    """Triggers 'Valron is typing...' in Discord.

    Args:
        ctx (discord.ext.commands.Context): See discordpy docs.
        time (int): Number of seconds to wait.

    """
    await ctx.trigger_typing()
    await asyncio.sleep(time)


def calculate_base_hp(classes_and_levels, con_modifier):
    """Calculates the base hit points given the classes, levels, and constitution modifier.

    Args:
        classes_and_levels (list(Class, int)): A list of tuples wherein each
            element is the class and corresponding level.
        con_modifier (int): The constitution modifer.

    Returns:
        (int, int): A tuple of the partial_hp and total character level.

    """
    is_level_1 = True
    current_hp = 0
    total_level = 0

    for class_and_level in classes_and_levels:
        dnd_class = class_and_level[0]
        level = class_and_level[1]

        avg_hit_dice = math.floor(dnd_class.hit_die / 2) + 1

        # For the base class
        if is_level_1:
            # On 1st level: max_hit_die + con_modifier
            current_hp = current_hp + dnd_class.hit_die + con_modifier
            # On every level above 1st: avg_hit_dice + con_modifier
            current_hp = current_hp + ((avg_hit_dice + con_modifier) * (level - 1))
            is_level_1 = False

        # On every level above 1st: avg_hit_dice + con_modifier
        else:
            current_hp = current_hp + ((avg_hit_dice + con_modifier) * level)

        # If matched_dnd_class is a Draconic Sorcerer
        if dnd_class.name == "Draconic Sorcerer":
            current_hp = current_hp + level

        total_level = total_level + level

    return (current_hp, total_level)


def apply_hp_mods(partial_hp, total_level, flags):
    """Calculates the hit points with the HP modifiers.

    Args:
        parital_hp (int): The base hit points.
        total_level (int): The total character level.
        flags (Flags): The collection of HP modifier flags

    Returns:
        int: The hit points with the HP modifiers.

    """
    if flags.is_hilldwarf:
        partial_hp = partial_hp + total_level

    if flags.axe_attuned:
        partial_hp = partial_hp + total_level

    if flags.is_tough:
        partial_hp = partial_hp + (total_level * 2)

    return partial_hp


def bot_reply_builder(
    con_modifier,
    classes_and_levels,
    total_level,
    final_hp,
    flags,
    inter: disnake.CommandInteraction,
):
    """Returns the formatted reply of the bot.

    Args:
        con_modifier (int): The constitution modifer.
        classes_and_levels (list(Class, int)): A list of tuples wherein each
            element is the class and corresponding level.
        final_hp: The calculated hit points.
        total_level (int): The total character level.
        flags (Flags): The collection of HP modifier flags
        ctx (discord.ext.commands.Context): See discordpy docs.

    Returns:
        str: Formatted reply of the bot.

    """
    if total_level > 20:
        bot_reply = (
            f"Oof! {inter.author.mention}, my friend, you have a level "
            + f"`{total_level}` character?  My wife says to double check its "
            + "levels! But if you really want to know, a "
        )
    else:
        bot_reply = f"{inter.author.mention}, my friend, a "

    if flags.is_hilldwarf:
        bot_reply = bot_reply + "`Hill Dwarf` "

    bot_reply = (
        bot_reply
        + f"`{helper.classes_and_levels_builder(classes_and_levels)}` character "
    )

    if flags.axe_attuned:
        bot_reply = bot_reply + "`attuned to a Berserker Axe` "

    bot_reply = bot_reply + f"with a Constitution modifier of `{con_modifier}` "

    if flags.is_tough:
        bot_reply = bot_reply + "and `Tough feat` "

    bot_reply = bot_reply + f"has `{final_hp}` hit points."

    # guilds = os.getenv("GUILDS")
    # member = os.getenv("MEMBER1")
    # if guilds:
    #     if (str(ctx.guild.id) in guilds) and (con_modifier < 0):
    #         try:
    #             summon = await ctx.guild.fetch_member(int(member))
    #             if summon:
    #                 bot_reply = (
    #                     bot_reply
    #                     + "\n\nOof! You have a negative Constitution modifier! "
    #                     + f"My wife tells me that I should summon {summon.mention}!"
    #                 )
    #         except HTTPException:
    #             pass

    return bot_reply


########################
## DISCORD BOT EVENTS ##
########################


# @bot.event
# async def on_connect():
#     """See https://discordpy.readthedocs.io/en/latest/api.html#event-reference"""
#     print(f"{bot.user.name} has connected to Discord!")

#     print(f"Connected to {len(bot.guilds)} Discord servers!")
#     await bot.change_presence(activity=helper.update_guild_counter(len(bot.guilds)))


@bot.event
async def on_ready():
    """See https://discordpy.readthedocs.io/en/latest/api.html#event-reference"""
    print(f"{bot.user.name} is ready to serve!")

    # print('Connected to the following Discord servers: ')
    # for guild in bot.guilds:
    #     print(f' >> {guild.name}')


# @bot.event
# async def on_guild_join(guild):
#     """See https://discordpy.readthedocs.io/en/latest/api.html#event-reference"""
#     print(f"Joined {guild.name}!")
#     await bot.change_presence(activity=helper.update_guild_counter(len(bot.guilds)))


# @bot.event
# async def on_guild_remove(guild):
#     """See https://discordpy.readthedocs.io/en/latest/api.html#event-reference"""
#     print(f"Left {guild.name}...")
#     await bot.change_presence(activity=helper.update_guild_counter(len(bot.guilds)))


# @bot.event
# async def on_command_error(ctx, error):
#     """See https://discordpy.readthedocs.io/en/latest/api.html#event-reference"""
#     if isinstance(error, commands.errors.MissingRequiredArgument):
#         await bot_typing(ctx, 1)
#         await ctx.send(
#             f"Oof! {ctx.author.mention}, my friend, something is missing! "
#             "My wife says to use `?help` for more information."
#         )
#     if isinstance(error, commands.errors.BadArgument):
#         await bot_typing(ctx, 1)
#         await ctx.send(
#             f"Oof! {ctx.author.mention}, my friend, what is the constitution modifier?"
#             "My wife says to use `?help` for more information."
#         )


#######################
## DISCORD BOT START ##
#######################
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)
