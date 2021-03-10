"""Unit Tests"""

import pytest

from bot import apply_hp_mods, calculate_base_hp
from utils.classes import Flags
from utils.helper import get_class

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
