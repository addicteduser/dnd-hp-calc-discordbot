import discord
import constants


class Class:
    """Represents a D&D class.

    Args:
        name (str): The name of the class.
        aliases (list(str)): The list of aliases of the class.
        hit_die (int): The maximum hit die value.

    Attributes:
        name: The name of the class.
        aliases: The list of aliases of the class.
        hit_die: The maximum hit die value.

    """

    def __init__(self, name, aliases, hit_die):
        self.name = name
        self.aliases = aliases
        self.hit_die = hit_die

    def get_class(self, alias):
        """Returns the D&D class given an alias.

        Args:
            alias (str): An alias of the class.

        Returns:
            Class: A D&D class.

        """
        if alias in self.aliases:
            return self

###################
## DATA BUILDERS ##
###################


def get_classes():
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


def get_dnd_aliases():
    """Returns the list of alias lists per D&D class.

    Returns:
        list(list(str)): The list of alias lists per D&D class.

    """
    aliases = []

    for dnd_class in get_classes():
        aliases.append(dnd_class.aliases)

    return aliases


####################
## STRING BUILDER ##
####################
def classes_and_levels_builder(classes_and_levels):
    """Returns the formatted classes and levels string for the bot reply.

    Args:
        classes_and_levels (list((str, int))): A list of tuples, where one tuple
            has a value of `(Class.name, level)`.

    Returns:
        str: Formatted classes and levels string.

    """
    result = ''

    for class_and_level in classes_and_levels:
        result = result + f'{class_and_level[0]} {class_and_level[1]} / '

    return result[:-3]


def alias_builder(alias_list):
    """Returns the formatted alias list for the bot reply.

    Args:
        alias_list (list(list(str))): The list of alias lists.

    Returns:
        str: Formatted alias list string.

    """
    result = ''

    for aliases in alias_list:
        result = result + f'- `{aliases[0]}` ('
        aliases.pop(0)
        for alias in aliases:
            result = result + f'`{alias}`, '

        result = result[:-2] + ')\n'

    return result[:-1]


def valron_doesnt_know(ctx, the_thing):
    return (f'Oof! {ctx.author.mention}, my friend, I don\'t know the {the_thing}! '
            + 'My wife says to use `?options` to see your classes or HP modifier options or `?help` for more information.')


###################
## OTHER HELPERS ##
###################
def update_guild_counter(num_guilds):
    return discord.Activity(
        name=f'D&D 5e in {num_guilds} guilds | ?help',
        type=discord.ActivityType.playing)


def get_class(alias):
    """Returns the D&D class given an alias.

    Args:
        alias (str): An alias of the class.

    Returns:
        Class: A D&D class.

    """
    dnd_class = None
    i = 0

    while i < len(get_classes()):
        dnd_class = get_classes()[i].get_class(alias)
        if dnd_class:
            break
        else:
            i += 1

    return dnd_class


def embed_builder(valron, description):
    """Return the base embed.

    Args:
        valron (str): The bot's name.
        description (str): The `description` field of the embed.

    Returns:
        discord.Embed: A discord Embed.

    """
    embed = discord.Embed(title='',
                          url=constants.TOP_GG_LINK,
                          description=description,
                          color=0x1abc9c)
    embed.set_author(name=f'{valron}',
                     url=constants.TOP_GG_LINK,
                     icon_url=f'{constants.IMG_LINK}')
    embed.set_thumbnail(url=f'{constants.IMG_LINK}')

    return embed


def log_error(error, command):
    print(f'ERROR: {error}')
    print(f'COMMAND: {command}')
