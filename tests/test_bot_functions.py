"""Unit Tests"""

import pytest

from bot import (apply_hp_mods, calculate_base_hp, parse_input,
                 parse_input_hp_mods)
from utils.classes import Flags
from utils.helper import get_class

# (con_modifier, classes_and_levels) == (TEST_BUILDS[i][0], TEST_BUILDS[i][1])
TEST_BUILDS = [(4, [(get_class('rogue'), 3),
                    (get_class('warlock'), 2),
                    (get_class('paladin'), 7),
                    (get_class('bard'), 4)
                    ]),
               (2, [(get_class('dracsorc'), 3),
                    (get_class('fighter'), 4)
                    ]),
               (2, [(get_class('fighter'), 4),
                    (get_class('dracsorc'), 3)
                    ]),
               (1, [(get_class('artificer'), 1),
                    (get_class('barbarian'), 1),
                    (get_class('bard'), 1),
                    (get_class('cleric'), 1),
                    (get_class('druid'), 1),
                    (get_class('fighter'), 1),
                    (get_class('monk'), 1),
                    (get_class('paladin'), 1),
                    (get_class('ranger'), 1),
                    (get_class('rogue'), 1),
                    (get_class('sorcerer'), 1),
                    (get_class('warlock'), 1),
                    (get_class('wizard'), 1)
                    ]),
               (1, [(get_class('artificer'), 1),
                    (get_class('barbarian'), 1),
                    (get_class('bard'), 1),
                    (get_class('cleric'), 1),
                    (get_class('druid'), 1),
                    (get_class('fighter'), 1),
                    (get_class('monk'), 1),
                    (get_class('paladin'), 1),
                    (get_class('ranger'), 1),
                    (get_class('rogue'), 1),
                    (get_class('draconicsorcerer'), 1),
                    (get_class('warlock'), 1),
                    (get_class('wizard'), 1)
                    ]),
               (6, [(get_class('paladin'), 6),
                    (get_class('draconicsorcerer'), 14)
                    ])
               ]

FLAGS = [
    # No flag
    Flags(True, False, False, False),
    # Hill Dwarf flag
    Flags(True, True, False, False),
    # Berserker Axe flag
    Flags(True, False, True, False),
    # Tough Feat flag
    Flags(True, False, False, True),
    # Hill Dwarf / Berserker Axe flag
    Flags(True, True, True, False),
    # Hill Dwarf / Tough Feat flag
    Flags(True, True, False, True),
    # Berserker Axe / Tough Feat flag
    Flags(True, False, True, True),
    # Hill Dwarf / Berserker Axe / Tough Feat flag
    Flags(True, True, True, True)

]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "expected_classes_and_levels, expected_flags, input_classes_and_levels, input_hp_mods", [
        (TEST_BUILDS[0][1], FLAGS[0], "rogue3/warlock2/paladin7/bard4", None),
        (TEST_BUILDS[5][1], FLAGS[7], "p6/ds14", "t/hd/ba")
    ]
)
async def test_parse_input(expected_classes_and_levels, expected_flags,
                           input_classes_and_levels, input_hp_mods):
    """Test parsing input.

    Args:
        expected_classes_and_levels (list(Class, int)): The expected list of tuples wherein each
            element is the class and corresponding level.
        expected_flags (Flag): The expected HP modifier flags.
        input_classes_and_levels (str): The user input classes and levels.
        input_hp_mods (str): The user input HP modifiers.

    """
    (classes_and_levels, flags) = await parse_input(
        input_classes_and_levels, input_hp_mods)

    for (i, class_and_level) in enumerate(classes_and_levels):
        assert class_and_level[0].name == expected_classes_and_levels[i][0].name
        assert class_and_level[1] == expected_classes_and_levels[i][1]

    assert flags.no_error == expected_flags.no_error
    assert flags.is_hilldwarf == expected_flags.is_hilldwarf
    assert flags.axe_attuned == expected_flags.axe_attuned
    assert flags.is_tough == expected_flags.is_tough


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_hp_mods", [
        "random", "hilldwrf", "ax", "toug"
    ]
)
async def test_parse_incorrect_input_hp_mods(input_hp_mods):
    """Test parsing incorrect input HP modifiers.

    Args:
        input_hp_mods (str): The user input HP modifiers.

    """
    flags = await parse_input_hp_mods(input_hp_mods)
    assert flags.no_error is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_classes_and_levels", [
        "randomclass", "randomclass1", "paladin1/randomclass2", 'paladin 1'
    ]
)
async def test_parse_incorrect_input_classes_and_levels(input_classes_and_levels):
    """Test parsing incorrect input classes and levels.

    Args:
        input_classes_and_levels (str): The user input classes and levels.

    """
    (_, flags) = await parse_input(
        input_classes_and_levels, None)
    assert flags.no_error is False


@pytest.mark.parametrize(
    "expected_hps, con_modifier, classes_and_levels", [
        ([154, 170, 170, 186, 186, 202, 202, 218],
         TEST_BUILDS[0][0], TEST_BUILDS[0][1]),
        ([55, 62, 62, 69, 69, 76, 76, 83],
         TEST_BUILDS[1][0], TEST_BUILDS[1][1]),
        ([57, 64, 64, 71, 71, 78, 78, 85],
         TEST_BUILDS[2][0], TEST_BUILDS[2][1]),
        ([84, 97, 97, 110, 110, 123, 123, 136],
         TEST_BUILDS[3][0], TEST_BUILDS[3][1]),
        ([85, 98, 98, 111, 111, 124, 124, 137],
         TEST_BUILDS[4][0], TEST_BUILDS[4][1]),
        ([230, 250, 250, 270, 270, 290, 290, 310],
         TEST_BUILDS[5][0], TEST_BUILDS[5][1]),
    ]
)
def test_calculate_hp(expected_hps, con_modifier, classes_and_levels):
    """Test calculating HP.

    Args:
        expected_hps ([int, int, int, int, int, int, int]): The list of expected HPs.
        con_modifier (int): The constitution modifer.
        classes_and_levels (list(Class, int)): A list of tuples wherein each
            element is the class and corresponding level.

    """
    (partial_hp, total_level) = calculate_base_hp(
        classes_and_levels, con_modifier)

    for (i, flag) in enumerate(FLAGS):
        assert apply_hp_mods(
            partial_hp, total_level, flag) == expected_hps[i]
