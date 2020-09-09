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


TOP_GG_LINK = 'https://top.gg/bot/666625461811413008'
GITHUB_LINK = 'https://github.com/addicteduser/dnd-hp-calc-discordbot'
IMG_LINK = 'https://i.imgur.com/0bByXQ4.png'

DISCORD_INVITE_LINK = 'https://discordapp.com/api/oauth2/authorize?client_id=666625461811413008&permissions=11264&scope=bot'
SUPPORT_SERVER_LINK = 'https://discord.gg/waCBQuD'

PAYPAL_LINK = 'https://paypal.me/addicteduser'
KOFI_LINK = 'https://ko-fi.com/addicteduser'
