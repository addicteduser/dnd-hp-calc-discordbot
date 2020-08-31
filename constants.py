import helper

###############
## CONSTANTS ##
###############
HILLDWARF_MODS = ['hilldwarf', 'hdwarf', 'hd']
BERSERKER_AXE_MODS = ['berserkeraxe', 'axe', 'ba']
TOUGH_MODS = ['tough', 't']
HP_MODS = HILLDWARF_MODS + BERSERKER_AXE_MODS + TOUGH_MODS
HP_MOD_ALIASES = [HILLDWARF_MODS, BERSERKER_AXE_MODS, TOUGH_MODS]
DND_CLASSES = helper.get_classes()
CLASS_ALIASES = helper.get_dnd_aliases()
