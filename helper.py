import discord
import constants


####################
## STRING BUILDER ##
####################
def classes_and_levels_builder(classes_and_levels):
    """Returns the formatted classes and levels string for the bot reply.

    Args:
        classes_and_levels (list((str, int))): A list of tuples, where one tuple
            has a value of `(Class, level)`.

    Returns:
        str: Formatted classes and levels string.

    """
    result = ''

    for class_and_level in classes_and_levels:
        result = result + f'{class_and_level[0].name} {class_and_level[1]} / '

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
    return (f'Oof! {ctx.author.mention}, my friend, I don\'t know the {the_thing}! ' +
            'My wife says to use `?options` to see your classes or HP modifier options or `?help` for more information.')


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

    while i < len(constants.DND_CLASSES()):
        dnd_class = constants.DND_CLASSES()[i].get_class(alias)
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
