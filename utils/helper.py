"""Helper

This module provides helper functions.
"""

from typing import List, Tuple, Union

import disnake
from disnake.ext import commands

import utils.constants as constants

from .classes import DndClass


####################
## STRING BUILDER ##
####################
def classes_and_levels_builder(classes_and_levels: List[Tuple[DndClass, int]]) -> str:
    """Returns the formatted classes and levels string for the bot reply.

    Parameters
    ----------
    classes_and_levels : List[Tuple[DndClass, int]]
        A list of tuples wherein each element is the class and corresponding level.

    Returns
    -------
    str
        Formatted classes and levels string.
    """
    result = ""

    for class_and_level in classes_and_levels:
        result = result + f"{class_and_level[0].name} {class_and_level[1]} / "

    return result[:-3]


def alias_builder(alias_list: List[List[str]]) -> str:
    """Returns the formatted alias list for the bot reply.

    Parameters
    ----------
    alias_list : List[List[str]]
        The list of alias lists.

    Returns
    -------
    str
        Formatted alias list string.
    """
    result = ""

    for aliases in alias_list:
        result = result + f"- `{aliases[0]}` ("
        aliases.pop(0)
        for alias in aliases:
            result = result + f"`{alias}`, "

        result = result[:-2] + ")\n"

    return result[:-1]


def valron_doesnt_know(
    the_thing: str,
    ctx: commands.Context = None,
    inter: disnake.CommandInteraction = None,
) -> str:
    """Returns the bot's reply when it does not recognize an input.

    Parameters
    ----------
    the_thing : str
        _description_
    ctx : commands.Context, optional
        The context in which a command is being invoked under, by default None.
        See [this](https://docs.disnake.dev/en/latest/ext/commands/api/context.html#disnake.ext.commands.Context) for more info.
    inter : disnake.CommandInteraction, optional
        The slash command interaction, by default None.
        See [this](https://docs.disnake.dev/en/latest/api/interactions.html#disnake.ApplicationCommandInteraction) for more info.

    Returns
    -------
    str
        Formatted reply of the bot.
    """
    name = ""

    if ctx:
        name = ctx.author.mention

    if inter:
        name = inter.author.mention

    return (
        f"Oof! {name}, my friend, I don't know the {the_thing}! "
        + "My wife says to use `/options` to see your classes "
        + "or HP modifier options or `/help` for more information."
    )


###################
## OTHER HELPERS ##
###################
def update_guild_counter(num_guilds: int) -> disnake.Activity:
    """Updates status displaying the number of Discord servers the bot belongs in.

    Parameters
    ----------
    num_guilds : int
        The number of Discord servers the bot belongs in.

    Returns
    -------
    disnake.Activity
        The Discord activity.
    """
    return disnake.Activity(
        name=f"D&D 5e in {num_guilds} guilds | /help", type=disnake.ActivityType.playing
    )


def get_class(alias: str) -> Union[DndClass, None]:
    """Returns the D&D class given an alias.

    Parameters
    ----------
    alias : str
        An alias of the class.

    Returns
    -------
    DndClass
        The DndClass with the alias. Else, returns None.
    """
    dnd_class = None
    i = 0

    while i < len(constants.DND_CLASSES()):
        dnd_class = constants.DND_CLASSES()[i].get_class(alias)
        if dnd_class:
            break

        i += 1

    return dnd_class


def embed_builder(valron: str, description: str) -> disnake.Embed:
    """Return the base embed.

    Parameters
    ----------
    valron : str
        The bot's name.
    description : str
        The `description` field of the embed.

    Returns
    -------
    disnake.Embed
        A discord Embed.
    """
    embed = disnake.Embed(
        title="", url=constants.TOP_GG_LINK, description=description, color=0x1ABC9C
    )
    embed.set_author(
        name=f"{valron}", url=constants.TOP_GG_LINK, icon_url=f"{constants.IMG_LINK}"
    )
    embed.set_thumbnail(url=f"{constants.IMG_LINK}")

    return embed
