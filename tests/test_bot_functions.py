"""Unit Tests"""

from bot import apply_hp_mods, calculate_base_hp
from utils import helper
from utils.classes import Flags


def test_calculate_base_hp():
    """Test calculating the base HP."""

    con_modifier = 4
    classes_and_levels = [
        (helper.get_class('rogue'), 3),
        (helper.get_class('warlock'), 2),
        (helper.get_class('paladin'), 7),
        (helper.get_class('bard'), 4)
    ]

    assert calculate_base_hp(classes_and_levels, con_modifier) == (154, 16)


def test_calculate_base_hp_dracsorc():
    """Test calculating the base HP of a draconic sorcerer."""

    con_modifier = 2

    base_classes_and_levels = [
        (helper.get_class('dracsorc'), 3),
        (helper.get_class('fighter'), 4)
    ]

    assert calculate_base_hp(base_classes_and_levels, con_modifier) == (55, 7)

    mc_classes_and_levels = [
        (helper.get_class('fighter'), 4),
        (helper.get_class('dracsorc'), 3)
    ]

    assert calculate_base_hp(mc_classes_and_levels, con_modifier) == (57, 7)


hd_flag = Flags(True, True, False, False)
axe_flag = Flags(True, False, True, False)
t_flag = Flags(True, False, False, True)
hd_axe_flag = Flags(True, True, True, False)
hd_t_flag = Flags(True, True, False, True)
axe_t_flag = Flags(True, False, True, True)
hd_axe_t_flag = Flags(True, True, True, True)


def test_calculate_with_hp_mods():
    """Test calculating with HP modifiers."""

    con_modifier = 4
    classes_and_levels = [
        (helper.get_class('rogue'), 3),
        (helper.get_class('warlock'), 2),
        (helper.get_class('paladin'), 7),
        (helper.get_class('bard'), 4)
    ]

    (partial_hp, total_level) = calculate_base_hp(
        classes_and_levels, con_modifier)

    assert apply_hp_mods(partial_hp, total_level, hd_flag) == 170
    assert apply_hp_mods(partial_hp, total_level, axe_flag) == 170
    assert apply_hp_mods(partial_hp, total_level, t_flag) == 186
    assert apply_hp_mods(partial_hp, total_level, hd_axe_flag) == 186
    assert apply_hp_mods(partial_hp, total_level, hd_t_flag) == 202
    assert apply_hp_mods(partial_hp, total_level, axe_t_flag) == 202
    assert apply_hp_mods(partial_hp, total_level, hd_axe_t_flag) == 218


def test_calculate_dracsroc_with_hp_mods():
    """Test calculating a draconic sorcerer with HP modifiers."""

    con_modifier = 2
    base_classes_and_levels = [
        (helper.get_class('dracsorc'), 3),
        (helper.get_class('fighter'), 4)
    ]

    (partial_hp, total_level) = calculate_base_hp(
        base_classes_and_levels, con_modifier)

    assert apply_hp_mods(partial_hp, total_level, hd_flag) == 62
    assert apply_hp_mods(partial_hp, total_level, axe_flag) == 62
    assert apply_hp_mods(partial_hp, total_level, t_flag) == 69
    assert apply_hp_mods(partial_hp, total_level, hd_axe_flag) == 69
    assert apply_hp_mods(partial_hp, total_level, hd_t_flag) == 76
    assert apply_hp_mods(partial_hp, total_level, axe_t_flag) == 76
    assert apply_hp_mods(partial_hp, total_level, hd_axe_t_flag) == 83

    ##########

    mc_classes_and_levels = [
        (helper.get_class('fighter'), 4),
        (helper.get_class('dracsorc'), 3)
    ]

    (partial_hp, total_level) = calculate_base_hp(
        mc_classes_and_levels, con_modifier)

    assert apply_hp_mods(partial_hp, total_level, hd_flag) == 64
    assert apply_hp_mods(partial_hp, total_level, axe_flag) == 64
    assert apply_hp_mods(partial_hp, total_level, t_flag) == 71
    assert apply_hp_mods(partial_hp, total_level, hd_axe_flag) == 71
    assert apply_hp_mods(partial_hp, total_level, hd_t_flag) == 78
    assert apply_hp_mods(partial_hp, total_level, axe_t_flag) == 78
    assert apply_hp_mods(partial_hp, total_level, hd_axe_t_flag) == 85
