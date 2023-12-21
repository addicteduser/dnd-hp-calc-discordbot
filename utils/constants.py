"""Constants

This module provides the constant values.
"""

# pylint: disable=C0103

from typing import List

from .classes import DndClass

SHOW_PERF = False


###################
## DATA BUILDERS ##
###################
def DND_CLASSES() -> List[DndClass]:
    """Returns the list of possible D&D classes.

    Returns
    -------
    List[DndClass]
        The list of possible D&D classes.
    """
    classes = []

    classes.append(DndClass("Artificer", ["artificer", "art", "a"], 8))
    classes.append(DndClass("Barbarian", ["barbarian", "barb", "bb"], 12))
    classes.append(DndClass("Bard", ["bard", "bd"], 8))
    classes.append(DndClass("Cleric", ["cleric", "cl", "c"], 8))
    classes.append(DndClass("Druid", ["druid", "dr", "d"], 8))
    classes.append(DndClass("Fighter", ["fighter", "fight", "f"], 10))
    classes.append(DndClass("Monk", ["monk", "mk", "m"], 8))
    classes.append(DndClass("Paladin", ["paladin", "pal", "p"], 10))
    classes.append(DndClass("Ranger", ["ranger", "ra"], 10))
    classes.append(DndClass("Rogue", ["rogue", "ro"], 8))
    classes.append(DndClass("Sorcerer", ["sorcerer", "sorc", "s"], 6))
    classes.append(
        DndClass(
            "Draconic Sorcerer",
            ["draconicsorcerer", "draconicsorc", "dracsorc", "ds"],
            6,
        )
    )
    classes.append(DndClass("Warlock", ["warlock", "lock", "wr"], 8))
    classes.append(DndClass("Wizard", ["wizard", "wiz", "wz"], 6))

    return classes


def DND_ALIASES() -> List[List[str]]:
    """Returns the list of alias lists per D&D class.

    Returns
    -------
    List[List[str]]
        The list of alias lists per D&D class.
    """
    aliases = []

    for dnd_class in DND_CLASSES():
        aliases.append(dnd_class.aliases)

    return aliases


###############
## CONSTANTS ##
###############
def HILLDWARF_MODS():
    """Returns the Hill Dwarf HP modifier aliases."""
    return ["hilldwarf", "hdwarf", "hd"]


def BERSERKER_AXE_MODS():
    """Returns the Berserker Axe HP modifier aliases."""
    return ["berserkeraxe", "axe", "ba"]


def TOUGH_MODS():
    """Returns the Tough Feat HP modifier aliases."""
    return ["tough", "t"]


def HP_MODS():
    """Returns the list of HP modifier aliases."""
    return HILLDWARF_MODS() + BERSERKER_AXE_MODS() + TOUGH_MODS()


def HP_MOD_ALIASES():
    """Returns the list of list of HP modifer aliases."""
    return [HILLDWARF_MODS(), BERSERKER_AXE_MODS(), TOUGH_MODS()]


###########
## LINKS ##
###########
TOP_GG_LINK = "https://top.gg/bot/666625461811413008"
GITHUB_LINK = "https://github.com/addicteduser/dnd-hp-calc-discordbot"
IMG_LINK = "https://i.imgur.com/0bByXQ4.png"

DISCORD_INVITE_LINK = (
    "https://discordapp.com/api/oauth2/authorize?"
    + "client_id=666625461811413008&"
    + "permissions=11264&scope=bot"
)
SUPPORT_SERVER_LINK = "https://discord.gg/waCBQuD"

PAYPAL_LINK = "https://paypal.me/addicteduser"
KOFI_LINK = "https://ko-fi.com/addicteduser"
GCASH_QR_CODE = "https://i.imgur.com/fnMORVa.jpg"
