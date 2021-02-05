import bot
import helper
from classes import Flags


def test_calculate_base_hp():
    classes_and_levels = [
        (helper.get_class('rogue'), 3),
        (helper.get_class('warlock'), 2),
        (helper.get_class('paladin'), 7),
        (helper.get_class('bard'), 4)
    ]
    con_modifier = 4

    assert (154, 16) == bot.calculate_base_hp(classes_and_levels, con_modifier)
