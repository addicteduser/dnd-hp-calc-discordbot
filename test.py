import re
import math

import constants
import helper

con_modifier = 4
input_classes_and_levels = "rogue3/warlock2/paladin7/bard4"
input_hp_mods = "t"

# Regex pattern for word##
regex = re.compile('([a-zA-Z]+)([0-9]+)')

no_error = True
is_hilldwarf = False
axe_attuned = False
is_tough = False


def parse_input(input_classes_and_levels, input_hp_mods):
    parse_input_hp_mods(input_hp_mods)
    return parse_input_classes_and_levels(input_classes_and_levels)


def parse_input_classes_and_levels(input_classes_and_levels):
    classes_and_levels = []

    # List of word##
    parsed_classes_and_levels = input_classes_and_levels.lower().split('/')

    # If there are parsed_classes_and_levels
    if parsed_classes_and_levels:

        # For each parsed_class_and_level, get class and level
        for parsed_class_and_level in parsed_classes_and_levels:
            class_and_level = parsed_class_and_level.strip()

            # If it follows word## pattern
            if re.match(regex, class_and_level):
                result = re.split(regex, class_and_level)
                matched_dnd_class = result[1]
                matched_level = int(result[2])

                # If matched_dnd_class exists in list of supported D&D classes
                dnd_class = helper.get_class(matched_dnd_class)
                if dnd_class:
                    # Track class name and level
                    classes_and_levels.append((dnd_class, matched_level))
                else:
                    await bot_typing(ctx, 1)
                    unknown = f'`{matched_dnd_class}` class'
                    await ctx.send((helper.valron_doesnt_know(ctx, unknown)))
                    helper.log_error(f'Unknown {unknown}.',
                                     ctx.message.content)
                    no_error = False
                    break

            # If it does not follow word## pattern
            else:
                await bot_typing(ctx, 1)
                await ctx.send(f'Oof! {ctx.author.mention}, my friend, kindly check your classes and levels! '
                               'It must look something like this `barb1/wizard2`. '
                               'My wife says to use `?help` for more information.')
                helper.log_error('Does not follow the classA##/classB##/etc format.',
                                 ctx.message.content)
                no_error = False
                break

    # If there are no parsed_classes_and_levels
    else:
        raise commands.MissingRequiredArgument

    return classes_and_levels


def parse_input_hp_mods(input_hp_mods):
    global is_hilldwarf
    global axe_attuned
    global is_tough
    print('here')
    # If there are input_hp_mods
    if input_hp_mods:
        input_hp_mods = input_hp_mods.lower()
        char_hp_mods = input_hp_mods.split('/')

        # For each char_hp_mod
        for char_hp_mod in char_hp_mods:
            # Check if valid char_hp_mod
            if char_hp_mod in constants.HP_MODS():
                if char_hp_mod in constants.HILLDWARF_MODS():
                    is_hilldwarf = True
                elif char_hp_mod in constants.BERSERKER_AXE_MODS():
                    axe_attuned = True
                elif char_hp_mod in constants.TOUGH_MODS():
                    print('hello')
                    is_tough = True
                    # print(is_tough)
            # If not valid char_hp_mod
            else:
                # await bot_typing(ctx, 1)
                # unknown = f'`{char_hp_mod}` HP modifier'
                # await ctx.send((helper.valron_doesnt_know(ctx, unknown)))
                # helper.log_error(f'Unknown {unknown}.',
                #                  ctx.message.content)
                # no_error = False
                # break
                print('unknown hp mod')


def calculate_base_hp(classes_and_levels):
    is_level_1 = True
    current_hp = 0
    total_level = 0

    for class_and_level in classes_and_levels:
        dnd_class = class_and_level[0]
        level = class_and_level[1]

        avg_hit_dice = math.floor(dnd_class.hit_die / 2) + 1

        # For the base class
        if is_level_1:
            # On 1st level: max_hit_die + con_modifier
            current_hp = current_hp + \
                dnd_class.hit_die + con_modifier
            # On every level above 1st: avg_hit_dice + con_modifier
            current_hp = current_hp + \
                ((avg_hit_dice + con_modifier) * (level - 1))
            is_level_1 = False

        # On every level above 1st: avg_hit_dice + con_modifier
        else:
            current_hp = current_hp + \
                ((avg_hit_dice + con_modifier) * level)

        # If matched_dnd_class is a Draconic Sorcerer
        if dnd_class.name == 'Draconic Sorcerer':
            current_hp = current_hp + level

        total_level = total_level + level

    return (current_hp, total_level)


def apply_hp_mods(current_hp, total_level):
    # print(is_tough)
    if is_hilldwarf:
        current_hp = current_hp + total_level

    if axe_attuned:
        current_hp = current_hp + total_level

    if is_tough:
        print('tough')
        current_hp = current_hp + (total_level * 2)

    return current_hp


classes_and_levels = parse_input(input_classes_and_levels, input_hp_mods)
(current_hp, total_level) = calculate_base_hp(classes_and_levels)
hp = apply_hp_mods(current_hp, total_level)
