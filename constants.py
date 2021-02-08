from classes import Class

###################
## DATA BUILDERS ##
###################


def DND_CLASSES():
    """Returns the list of possible D&D classes.

    Returns:
        list(Class): A list of D&D classes.

    """
    classes = []

    classes.append(Class('Artificer', ['artificer', 'art', 'a'], 8))
    classes.append(Class('Barbarian', ['barbarian', 'barb', 'bb'], 12))
    classes.append(Class('Bard', ['bard', 'bd'], 8))
    classes.append(Class('Cleric', ['cleric', 'cl', 'c'], 8))
    classes.append(Class('Druid', ['druid', 'dr', 'd'], 8))
    classes.append(Class('Fighter', ['fighter', 'fight', 'f'], 10))
    classes.append(Class('Monk', ['monk', 'mk', 'm'], 8))
    classes.append(Class('Paladin', ['paladin', 'pal', 'p'], 10))
    classes.append(Class('Ranger', ['ranger', 'ra'], 10))
    classes.append(Class('Rogue', ['rogue', 'ro'], 8))
    classes.append(Class('Sorcerer', ['sorcerer', 'sorc', 's'], 6))
    classes.append(Class('Draconic Sorcerer', [
                   'draconicsorcerer', 'draconicsorc', 'dracsorc', 'ds'], 6))
    classes.append(Class('Warlock', ['warlock', 'lock', 'wr'], 8))
    classes.append(Class('Wizard', ['wizard', 'wiz', 'wz'], 6))

    return classes


def DND_ALIASES():
    """Returns the list of alias lists per D&D class.

    Returns:
        list(list(str)): The list of alias lists per D&D class.

    """
    aliases = []

    for dnd_class in DND_CLASSES():
        aliases.append(dnd_class.aliases)

    return aliases


###############
## CONSTANTS ##
###############

def HILLDWARF_MODS():
    return ['hilldwarf', 'hdwarf', 'hd']


def BERSERKER_AXE_MODS():
    return ['berserkeraxe', 'axe', 'ba']


def TOUGH_MODS():
    return ['tough', 't']


def HP_MODS():
    return HILLDWARF_MODS() + BERSERKER_AXE_MODS() + TOUGH_MODS()


def HP_MOD_ALIASES():
    return [HILLDWARF_MODS(), BERSERKER_AXE_MODS(), TOUGH_MODS()]


###########
## LINKS ##
###########
TOP_GG_LINK = 'https://top.gg/bot/666625461811413008'
GITHUB_LINK = 'https://github.com/addicteduser/dnd-hp-calc-discordbot'
IMG_LINK = 'https://i.imgur.com/0bByXQ4.png'

DISCORD_INVITE_LINK = 'https://discordapp.com/api/oauth2/authorize?client_id=666625461811413008&permissions=11264&scope=bot'
SUPPORT_SERVER_LINK = 'https://discord.gg/waCBQuD'

PAYPAL_LINK = 'https://paypal.me/addicteduser'
KOFI_LINK = 'https://ko-fi.com/addicteduser'
GCASH_QR_CODE = 'https://i.imgur.com/fnMORVa.jpg'
