from bot import calculate_base_hp, apply_hp_mods
import helper
from classes import Flags


def test_calculate_base_hp():
    con_modifier = 4
    classes_and_levels = [
        (helper.get_class('rogue'), 3),
        (helper.get_class('warlock'), 2),
        (helper.get_class('paladin'), 7),
        (helper.get_class('bard'), 4)
    ]

    assert (154, 16) == calculate_base_hp(classes_and_levels, con_modifier)


def test_calculate_base_hp_dracsorc():
    con_modifier = 2

    base_classes_and_levels = [
        (helper.get_class('dracsorc'), 3),
        (helper.get_class('fighter'), 4)
    ]

    assert (55, 7) == calculate_base_hp(base_classes_and_levels, con_modifier)

    mc_classes_and_levels = [
        (helper.get_class('fighter'), 4),
        (helper.get_class('dracsorc'), 3)
    ]

    assert (57, 7) == calculate_base_hp(mc_classes_and_levels, con_modifier)


hd_flag = Flags(True, True, False, False)
axe_flag = Flags(True, False, True, False)
t_flag = Flags(True, False, False, True)
hd_axe_flag = Flags(True, True, True, False)
hd_t_flag = Flags(True, True, False, True)
axe_t_flag = Flags(True, False, True, True)
hd_axe_t_flag = Flags(True, True, True, True)


def test_calculate_with_hp_mods():
    con_modifier = 4
    classes_and_levels = [
        (helper.get_class('rogue'), 3),
        (helper.get_class('warlock'), 2),
        (helper.get_class('paladin'), 7),
        (helper.get_class('bard'), 4)
    ]

    (partial_hp, total_level) = calculate_base_hp(
        classes_and_levels, con_modifier)

    assert 170 == apply_hp_mods(partial_hp, total_level, hd_flag)
    assert 170 == apply_hp_mods(partial_hp, total_level, axe_flag)
    assert 186 == apply_hp_mods(partial_hp, total_level, t_flag)
    assert 186 == apply_hp_mods(partial_hp, total_level, hd_axe_flag)
    assert 202 == apply_hp_mods(partial_hp, total_level, hd_t_flag)
    assert 202 == apply_hp_mods(partial_hp, total_level, axe_t_flag)
    assert 218 == apply_hp_mods(partial_hp, total_level, hd_axe_t_flag)


def test_calculate_dracsroc_with_hp_mods():
    con_modifier = 2
    base_classes_and_levels = [
        (helper.get_class('dracsorc'), 3),
        (helper.get_class('fighter'), 4)
    ]

    (partial_hp, total_level) = calculate_base_hp(
        base_classes_and_levels, con_modifier)

    assert 62 == apply_hp_mods(partial_hp, total_level, hd_flag)
    assert 62 == apply_hp_mods(partial_hp, total_level, axe_flag)
    assert 69 == apply_hp_mods(partial_hp, total_level, t_flag)
    assert 69 == apply_hp_mods(partial_hp, total_level, hd_axe_flag)
    assert 76 == apply_hp_mods(partial_hp, total_level, hd_t_flag)
    assert 76 == apply_hp_mods(partial_hp, total_level, axe_t_flag)
    assert 83 == apply_hp_mods(partial_hp, total_level, hd_axe_t_flag)

    ##########

    mc_classes_and_levels = [
        (helper.get_class('fighter'), 4),
        (helper.get_class('dracsorc'), 3)
    ]

    (partial_hp, total_level) = calculate_base_hp(
        mc_classes_and_levels, con_modifier)

    assert 64 == apply_hp_mods(partial_hp, total_level, hd_flag)
    assert 64 == apply_hp_mods(partial_hp, total_level, axe_flag)
    assert 71 == apply_hp_mods(partial_hp, total_level, t_flag)
    assert 71 == apply_hp_mods(partial_hp, total_level, hd_axe_flag)
    assert 78 == apply_hp_mods(partial_hp, total_level, hd_t_flag)
    assert 78 == apply_hp_mods(partial_hp, total_level, axe_t_flag)
    assert 85 == apply_hp_mods(partial_hp, total_level, hd_axe_t_flag)
