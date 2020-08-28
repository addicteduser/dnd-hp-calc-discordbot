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


def get_class_name(alias):
    not_found = True
    class_name = None
    i = 0

    while not_found:
        dnd_class = get_classes()[i]
        class_name = dnd_class.get_name(alias)
        if class_name:
            not_found = False
        else:
            i += 1

    return class_name


print(get_class_name('ds'))
# print(get_classes()[0].name)
