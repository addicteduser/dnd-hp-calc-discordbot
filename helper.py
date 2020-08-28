class Class:
    def __init__(self, name, aliases, hit_die):
        self.name = name
        self.aliases = aliases
        self.hit_die = hit_die

    def get_class(self, alias):
        """Returns the class given one of its aliases.

        Args:
            alias (String): An alias of the class.

        Returns:
            String: The name of the class.

        """
        if alias in self.aliases:
            return self


def get_classes():
    classes = []

    classes.append(Class('Artificer', ['artificer', 'art', 'a'], 8))
    classes.append(Class('Barbarian', ['barbarian', 'barb', 'bb'], 12))
    classes.append(Class('Bard', ['bard', 'bd'], 8))
    classes.append(Class('Cleric', ['cleric', 'cl', 'c'], 8))
    classes.append(Class('Druid', ['druid', 'dr', 'd'], 8))
    classes.append(Class('Fighter', ['fighter', 'fight', 'f'], 10))
    classes.append(Class('Monk', ['monk', 'mk', 'm'], 8))
    classes.append(Class('Paladin', ['paladin', 'pally', 'p'], 10))
    classes.append(Class('Ranger', ['ranger', 'ra'], 10))
    classes.append(Class('Rogue', ['rogue', 'ro'], 8))
    classes.append(Class('Sorcerer', ['sorcerer', 'sorc', 's'], 6))
    classes.append(Class('Draconic Sorcerer', [
                   'draconicsorcerer', 'draconicsorc', 'dracsorc', 'ds'], 6))
    classes.append(Class('Warlock', ['warlock', 'lock', 'wr'], 8))
    classes.append(Class('Wizard', ['wizard', 'wiz', 'wz'], 6))

    return classes


###############
## CONSTANTS ##
###############
HILLDWARF_MODS = ['hilldwarf', 'hdwarf', 'hd']
BERSERKER_AXE_MODS = ['berserkeraxe', 'axe', 'ba']
TOUGH_MODS = ['tough', 't']
HP_MODS = HILLDWARF_MODS + BERSERKER_AXE_MODS + TOUGH_MODS
DND_CLASSES = get_classes()


def get_class(alias):
    dnd_class = None
    i = 0

    while i < len(DND_CLASSES):
        dnd_class = DND_CLASSES[i].get_class(alias)
        if dnd_class:
            break
        else:
            i += 1

    return dnd_class


def classes_and_levels_builder(classes_and_levels):
    result = ''

    for class_and_level in classes_and_levels:
        result = result + f'{class_and_level[0]} {class_and_level[1]} / '

    return result[:-3]


def log_error(error, msg):
    print(f'ERROR: {error}')
    print(f'COMMAND: {msg}')
