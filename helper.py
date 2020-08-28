from dnd_class import Class


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


def get_aliases():
    aliases = []
    for dnd_class in get_classes():
        aliases = aliases + dnd_class.aliases

    return aliases


def get_class(alias):
    dnd_class = None
    i = 0

    while i < len(get_classes()):
        dnd_class = get_classes()[i].get_class(alias)
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
