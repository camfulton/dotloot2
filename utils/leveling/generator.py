import constants
from utils import sounds
from utils.leveling import lvling_constants
from utils.leveling.item_progression import (
    generate_flask_progression,
    generate_weapon_progression,
)

LIKELY_ATTACKING = [
    "claws",
    "daggers",
    "one hand axes",
    "one hand maces",
    "thrusting one hand swords",
    "one hand swords",
    "two hand axes",
    "two hand maces",
    "two hand swords",
    "warstaves",
    "bows",
    "quivers",
]


def generate_currency(output_file_path):
    currency = ""

    # whet
    currency += (
        "# leveling/currency/whetstones\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['classes']} Currency\n"
        f"\t{constants.SYNTAX['bases']} \"Blacksmith's Whetstone\"\n"
        f"\t{constants.SYNTAX['say']} \"{sounds.get_or_create_sound(output_file_path, 'whet...')}\"\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )
    # scrap
    currency += (
        "# leveling/currency/scrap\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['classes']} Currency\n"
        f"\t{constants.SYNTAX['bases']} \"Armourer's Scrap\"\n"
        f"\t{constants.SYNTAX['say']} \"{sounds.get_or_create_sound(output_file_path, 'scrap...')}\"\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )
    # alt
    currency += (
        "# leveling/currency/alt\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['classes']} Currency\n"
        f"\t{constants.SYNTAX['bases']} \"Orb of Alteration\"\n"
        f"\t{constants.SYNTAX['say']} \"{sounds.get_or_create_sound(output_file_path, 'alt...')}\"\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )
    # trans
    currency += (
        "# leveling/currency/trans\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['classes']} Currency\n"
        f"\t{constants.SYNTAX['bases']} \"Orb of Transmutation\"\n"
        f"\t{constants.SYNTAX['say']} \"{sounds.get_or_create_sound(output_file_path, 'trans...')}\"\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )
    # chance
    currency += (
        "# leveling/currency/chance\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['classes']} Currency\n"
        f"\t{constants.SYNTAX['bases']} \"Orb of Chance\"\n"
        f"\t{constants.SYNTAX['say']} \"{sounds.get_or_create_sound(output_file_path, 'chance...')}\"\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )
    # essence
    currency += (
        "# leveling/currency/essence\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['classes']} Currency\n"
        f"\t{constants.SYNTAX['bases']} Essence\n"
        f"\t{constants.SYNTAX['say']} \"{sounds.get_or_create_sound(output_file_path, 'essence...')}\"\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )
    # chrome 2x2
    currency += (
        "# leveling/currency/2x2 chrome\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['colors']} RGB\n"
        f"\t{constants.SYNTAX['height']} 2\n"
        f"\t{constants.SYNTAX['width']} 2\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )
    # chrome 1x3
    currency += (
        "# leveling/currency/3x1 chrome\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['colors']} RGB\n"
        f"\t{constants.SYNTAX['height']} 3\n"
        f"\t{constants.SYNTAX['width']} 1\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    # the rest
    currency += (
        "# leveling/currency/the rest\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['classes']} Currency\n"
        f"\t{constants.SYNTAX['bases']} \"Scroll of Wisdom\" \"Portal Scroll\" \"Orb of Augmentation\"\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    return currency


def generate_attacking_stuff():
    # Shows iron rings and rustic sashes until act 2ish
    bases = '"Iron Ring" "Rustic Sash"'

    attacking_stuff = (
        "# leveling/attack items\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 24\n"
        f"\t{constants.SYNTAX['rarity']} Normal Magic\n"
        f"\t{constants.SYNTAX['bases']} == {bases}\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    return attacking_stuff


def generate_caster_stuff():
    # Shows caster ring craft items until act 2ish
    caster_stuff = ""
    bases = '"Iron Ring" "Ruby Ring" "Sapphire Ring" "Topaz Ring" "Two-Stone Ring"'

    caster_stuff += (
        "# leveling/caster items/caster crafting rings\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 24\n"
        f"\t{constants.SYNTAX['rarity']} Normal Magic\n"
        f"\t{constants.SYNTAX['bases']} == {bases}\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    return caster_stuff


def generate_misc_items(output_file_path):
    misc_items = ""

    misc_items += (
        "# leveling/misc items/quicksilver\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['icon']} 1 Red Diamond\n"
        f"\t{constants.SYNTAX['classes']} \"Utility Flasks\"\n"
        f"\t{constants.SYNTAX['bases']} Quicksilver\n"
        f"\t{constants.SYNTAX['say']} \"{sounds.get_or_create_sound(output_file_path, 'quicksilver...')}\"\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_FG}\n"
        f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_BORDER}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    misc_items += (
        "# leveling/misc items/utility flasks\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['classes']} \"Utility Flasks\"\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    misc_items += (
        "# leveling/misc items/gems\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['classes']} \"Gem\"\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    return misc_items


def generate_normal_items():
    # Shows amulets, rings, belts, and boots at magic until act 2ish
    normal_items = ""
    good_classes = '"Amulets" "Belts" "Rings" "Boots"'
    other_classes = '"Gloves" "Helmets" "Shields" "Body Armours"'

    normal_items += (
        "# leveling/magic items/desired\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 16\n"
        f"\t{constants.SYNTAX['rarity']} Normal\n"
        f"\t{constants.SYNTAX['classes']} == {good_classes}\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    normal_items += (
        "# leveling/magic items/other\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_XSM_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 12\n"
        f"\t{constants.SYNTAX['rarity']} Normal\n"
        f"\t{constants.SYNTAX['classes']} == {other_classes}\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_NORMAL_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    return normal_items


def generate_magic_items():
    # Shows amulets, rings, belts, and boots at magic until act 2ish
    magic_items = ""
    classes = '"Amulets" "Belts" "Rings" "Boots"'

    magic_items += (
        "# leveling/magic items/desired\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 24\n"
        f"\t{constants.SYNTAX['rarity']} Magic\n"
        f"\t{constants.SYNTAX['classes']} == {classes}\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_MAGIC_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    magic_items += (
        "# leveling/magic items/other\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_SM_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 16\n"
        f"\t{constants.SYNTAX['rarity']} Magic\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_MAGIC_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    return magic_items


def generate_rare_items():
    # Shows amulets, rings, belts, and boots at magic until act 2ish
    rare_items = ""
    classes = (
        '"Amulets" "Belts" "Rings" "Boots" "Gloves" "Helmets" "Shields" "Body Armours"'
    )

    # Good rares u want 2 see
    rare_items += (
        "# leveling/rare items/desired\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['rarity']} Rare\n"
        f"\t{constants.SYNTAX['classes']} == {classes}\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_RARE_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    # All other rares for vending purposes
    rare_items += (
        "# leveling/rare items/other\n"
        "Show\n"
        f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_SM_FONT_SIZE}\n"
        f"\t{constants.SYNTAX['alvl']} <= 68\n"
        f"\t{constants.SYNTAX['rarity']} Rare\n"
        f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_RARE_FG}\n"
        f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
    )

    return rare_items


def generate_links(links, output_file_path):
    link_output = ""

    for link in links:
        link_output += (
            f"# leveling/links/{link}\n"
            "Show\n"
            f"\t{constants.SYNTAX['fontsize']} {lvling_constants.LVLING_FONT_SIZE}\n"
            f"\t{constants.SYNTAX['colors']} {len(link)}{link.upper()}\n"
            f"\t{constants.SYNTAX['alvl']} <= 68\n"
            f"\t{constants.SYNTAX['icon']} 1 Blue Diamond\n"
            f"\t{constants.SYNTAX['fg']} {lvling_constants.LVLING_RARE_FG}\n"
            f"\t{constants.SYNTAX['border']} {lvling_constants.LVLING_RARE_FG}\n"
            f"\t{constants.SYNTAX['bg']} {lvling_constants.LVLING_BG}\n\n\n"
            f"\t{constants.SYNTAX['say']} \"{sounds.get_or_create_sound(output_file_path, f'{link}...')}\"\n"
        )

    return link_output


def generate_leveling_filter_blocks(block, output_file_path):
    the_leveling_filter = "# :: BEGIN LEVELING SECTION ::\n\n"
    weapons = block.lines[0]
    links = block.lines[1]

    # generate weapon progression - weapons are stored in block.lines for this bc lazy
    if weapons:
        classes_str = ""
        for cls in weapons:
            classes_str += f'"{cls.title()}" '
        the_leveling_filter += generate_weapon_progression(
            classes_str.strip(), output_file_path
        )

    # show iron rings and belts if we are dealing with attacky weapons
    for weapon in weapons:
        if weapon.strip().lower() in LIKELY_ATTACKING:
            the_leveling_filter += generate_attacking_stuff()
        else:
            the_leveling_filter += generate_caster_stuff()

    the_leveling_filter += generate_links(links, output_file_path)
    the_leveling_filter += generate_flask_progression()
    the_leveling_filter += generate_currency(output_file_path)
    the_leveling_filter += generate_misc_items(output_file_path)
    the_leveling_filter += generate_rare_items()
    the_leveling_filter += generate_magic_items()
    the_leveling_filter += generate_normal_items()

    return the_leveling_filter
