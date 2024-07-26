from dataclasses import dataclass

import constants
from utils import sounds
from utils.leveling import lvling_constants


@dataclass
class ItemAndDropLevel:
    ilvl: int
    dlvl: int


@dataclass
class Flask:
    bases: str
    alvl: int


ITEM_AND_DROP_LEVELS = [
    ItemAndDropLevel(9, 5),
    ItemAndDropLevel(15, 11),
    ItemAndDropLevel(18, 15),
    ItemAndDropLevel(22, 18),
    ItemAndDropLevel(26, 22),
    ItemAndDropLevel(30, 26),
    ItemAndDropLevel(34, 30),
    ItemAndDropLevel(40, 34),
    ItemAndDropLevel(44, 40),
    ItemAndDropLevel(48, 44),
    ItemAndDropLevel(52, 48),
    ItemAndDropLevel(56, 52),
    ItemAndDropLevel(60, 56),
    ItemAndDropLevel(64, 60),
    ItemAndDropLevel(68, 64),
]

FLASKS_TO_HIDE = [
    Flask('"Large" "Medium" "Small"', 15),
    Flask('"Grand" "Greater"', 30),
    Flask('"Colossal" "Giant" "Sacred"', 48),
    Flask('"Hallowed" "Sanctified"', 60),
]

FLASKS = [
    Flask('"Small"', 9),
    Flask('"Medium"', 13),
    Flask('"Large"', 17),
    Flask('"Greater"', 19),
    Flask('"Grand"', 25),
    Flask('"Giant"', 31),
    Flask('"Colossal"', 37),
    Flask('"Sacred"', 43),
    Flask('"Hallowed"', 51),
    Flask('"Sanctified"', 60),
    Flask('"Divine"', 68),
    Flask('"Eternal"', 68),
]


def generate_weapon_progression(item_classes, output_file_path):
    prog = ""

    for i, range in enumerate(ITEM_AND_DROP_LEVELS):
        # Normal
        prog += (
            f"# leveling/weapon progression/::{i + 1}/normal\n"
            "Show\n"
            f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
            f"\t{constants.SYNTAX['ilvl']} <= {range.ilvl}\n"
            f"\t{constants.SYNTAX['droplvl']} >= {range.dlvl}\n"
            f"\t{constants.SYNTAX['rarity']} Normal\n"
            f"\t{constants.SYNTAX['classes']} == {item_classes}\n"
            f"\t{constants.SYNTAX['icon']} 1 Green Diamond\n"
            f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_NORMAL_FG}\n"
            f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_BORDER}\n"
            f"\t{constants.SYNTAX['say']} \"{sounds.get_or_create_sound(output_file_path, 'normal weapon upgrade...')}\"\n"  # noqa
            f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
        )
        # Magic
        prog += (
            f"# leveling/weapon progression/::{i + 1}/magic\n"
            "Show\n"
            f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
            f"\t{constants.SYNTAX['ilvl']} <= {range.ilvl}\n"
            f"\t{constants.SYNTAX['droplvl']} >= {range.dlvl}\n"
            f"\t{constants.SYNTAX['rarity']} Magic\n"
            f"\t{constants.SYNTAX['classes']} == {item_classes}\n"
            f"\t{constants.SYNTAX['icon']} 1 Green Diamond\n"
            f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_MAGIC_FG}\n"
            f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_BORDER}\n"
            f"\t{constants.SYNTAX['say']} \"{sounds.get_or_create_sound(output_file_path, 'magic weapon upgrade...')}\"\n"  # noqa
            f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
        )
        # Rare
        prog += (
            f"# leveling/weapon progression/::{i + 1}/rare\n"
            "Show\n"
            f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
            f"\t{constants.SYNTAX['ilvl']} <= {range.ilvl}\n"
            f"\t{constants.SYNTAX['droplvl']} >= {range.dlvl}\n"
            f"\t{constants.SYNTAX['rarity']} Rare\n"
            f"\t{constants.SYNTAX['classes']} == {item_classes}\n"
            f"\t{constants.SYNTAX['icon']} 1 Green Diamond\n"
            f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_RARE_FG}\n"
            f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_BORDER}\n"
            f"\t{constants.SYNTAX['say']} \"{sounds.get_or_create_sound(output_file_path, 'rare weapon upgrade...')}\"\n"  # noqa
            f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
        )

    return prog


def generate_flask_progression():
    prog = ""
    classes = '"Life Flasks" "Mana Flasks"'

    for i, flask in enumerate(FLASKS_TO_HIDE):
        prog += (
            f"# leveling/flasks/hide outdated/::{i + 1}\n"
            "Hide\n"
            f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
            f"\t{constants.SYNTAX['alvl']} >= {flask.alvl}\n"
            f"\t{constants.SYNTAX['classes']} == {classes}\n"
            f"\t{constants.SYNTAX['bases']} {flask.bases}\n"
            f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_FG}\n"
            f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_BORDER}\n"
            f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n"
            "\tDisableDropSound True\n\n\n"
        )

    for i, flask in enumerate(FLASKS):
        prog += (
            f"# leveling/flasks/{flask.bases}\n"
            "Show\n"
            f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
            f"\t{constants.SYNTAX['alvl']} <= {flask.alvl}\n"
            f"\t{constants.SYNTAX['classes']} == {classes}\n"
            f"\t{constants.SYNTAX['bases']} {flask.bases}\n"
            f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_FG}\n"
            f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_BORDER}\n"
            f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
        )

    return prog
