CONFIG_KEYS = [
    'name',
    'league',
    'version'
]

# translate friendly syntax to filter syntax
SYNTAX = {
    'lookup': {
            'exclusive_uniques': 'BaseType',
            'uniques': 'BaseType',
    },
    'ilvl': 'ItemLevel',
    'droplvl': 'DropLevel',
    'quality': 'Quality',
    'rarity': 'Rarity',
    'classes': 'Class',
    'bases': 'BaseType',
    'prophecy': 'Prophecy',
    'sockets': 'Sockets',
    'links': 'LinkedSockets',
    'colors': 'SocketGroup',
    'height': 'Height',
    'width': 'Width',
    'explicit': 'HasExplicitMod',
    'enchanted': 'AnyEnchantment',
    'enchantments': 'HasEnchantment',
    'stacksize': 'StackSize',
    'gemlvl': 'GemLevel',
    'identified': 'Identified',
    'corrupted': 'Corrupted',
    'influence': 'HasInfluence',
    'elder': 'ElderItem',
    'shaper': 'ShaperItem',
    'fractured': 'FracturedItem',
    'synthesized': 'SynthesisedItem',
    'synthesised': 'SynthesisedItem',
    'shapedmap': 'ShapedMap',
    'eldermap': 'ElderMap',
    'blighted': 'BlightedMap',
    'maptier': 'MapTier',
    'border': 'SetBorderColor',
    'fg': 'SetTextColor',
    'bg': 'SetBackgroundColor',
    'fontsize': 'SetFontSize',
    'sound': 'PlayAlertSound',
    'positionalsound': 'PlayAlertSoundPositional',
    'customsound': 'CustomAlertSound',
    'icon': 'MinimapIcon',
    'beam': 'PlayEffect',
    'altquality': 'AlternateQuality',
    'replica': 'Replica',
}
# Avoid updating both if they change the customsound syntax
SYNTAX['say'] = SYNTAX['customsound']

# https://pathofexile.fandom.com/wiki/Public_stash_tab_API
FRAME_TYPES = {
    'NORMAL': 0,
    'MAGIC': 1,
    'RARE': 2,
    'UNIQUE': 3,
    'GEM': 4,
    'CURRENCY': 5,
    'DIVINATION_CARD': 6,
    'QUEST_ITEM': 7,
    'PROPHECY': 8,
    'RELIC': 9,

    0: 'NORMAL',
    1: 'MAGIC',
    2: 'RARE',
    3: 'UNIQUE',
    4: 'GEM',
    5: 'CURRENCY',
    6: 'DIVINATION_CARD',
    7: 'QUEST_ITEM',
    8: 'PROPHECY',
    9: 'RELIC',
}

# POE Ninja sometimes puts like 'Alva' in the variant line, which we do not care about
VARIANTS_THAT_MATTER_FOR_FILTERS = [
    'SHAPER',
    'ELDER',
    'REDEEMER',
    'HUNTER',
    'CRUSADER',
    'WARLORD'
]

# At time of writing, doing a standard filter can brick your filter if you lookup these items
BROKEN_ITEMS = [
    "A Gracious Master",
    "Ancient Rivalries I",
    "Brothers in Arms",
    "Echoes of Lost Love",
    "Echoes of Mutation",
    "The Aesthete's Spirit",
    "The Blacksmith",
    "The Emperor's Trove",

]

UNDROPPABLE = [
    # vendor
    "arborix",
    "duskdawn",
    "the goddess scorned",
    "the goddess unleashed",
    "kingmaker",
    "loreweave",
    "magna eclipsis",
    "the retch",
    "star of wraeclast",
    "the taming",
    # fated uniques (prophecy upgrade only)
    "amplification rod",
    "asenath's chant",
    "atziri's reflection",
    "cameria's avarice",
    "chaber cairn",
    "corona solaris",
    "cragfall",
    "crystal vault",
    "death's opus",
    "deidbellow",
    "doedre's malevolence",
    "doomfletch's prism",
    "dreadbeak",
    "dreadsurge",
    "duskblight",
    "ezomyte hold",
    "fox's fortune",
    "frostferno",
    "geofri's devotion",
    "geofri's legacy",
    "greedtrap",
    "hrimburn",
    "hrimnor's dirge",
    "hyrri's demise",
    "kaltensoul",
    "kaom's way",
    "karui charge",
    "malachai's awakening",
    "martyr's crown",
    "mirebough",
    "ngamahu tiki",
    "panquetzaliztli",
    "queen's escape",
    "realm ender",
    "sanguine gambol",
    "shavronne's gambit",
    "silverbough",
    "sunspite",
    "the cauteriser",
    "the dancing duo",
    "the effigon",
    "the gryphon",
    "the iron fortress",
    "the nomad",
    "the oak",
    "the signal fire",
    "the stormwall",
    "the tactician",
    "the tempest",
    "thirst for horrors",
    "timetwist",
    "voidheart",
    "wall of brambles",
    "whakatutuki o matua",
    "wildwrap",
    "windshriek",
    "winterweave",
    # blessed uniques (breach blessing upgrade only)
    "xoph's nurture",
    "the formless inferno",
    "xoph's blood",
    "tulfall",
    "the perfect form",
    "the pandemonius",
    "hand of wisdom and action",
    "esh's visage",
    "choir of the storm",
    "uul-netol's embrace",
    "the red trail",
    "the surrender",
    "united in dream",
    "skin of the lords",
    "presence of chayula",
    "the red nightmare",
    "the green nightmare",
    "the blue nightmare",
    # incursion temple upgrade only
    "transcendent flesh",
    "transcendent mind",
    "transcendent spirit",
    "soul ripper",
    "slavedriver's hand",
    "coward's legacy",
    "omeyocan",
    "fate of the vaal",
    "mask of the stitched demon",
    "apep's supremacy",
    "zerphi's heart",
    "shadowstitch",
    # harbinger uniques (always drop as pieces)
    "the flow untethered",
    "the fracturing spinner",
    "the tempest's binding",
    "the rippling thoughts",
    "the enmity divine",
    "the unshattered will",
    # corruption only
    "blood of corruption",
    "ancient waystones"
    "atziri's reign",
    "blood sacrifice",
    "brittle barrier",
    "chill of corruption",
    "combustibles",
    "corrupted energy",
    "fevered mind",
    "fragility",
    "hungry abyss",
    "mutated growth",
    "pacifism",
    "powerlessness",
    "sacrificial harvest",
    "self-flagellation",
    "vaal sentencing",
    "weight of sin",
]

ONLY_LINKED = [
    'tabula rasa',
    'skin of the lords',
    'skin of the loyal',
    'shadowstitch',
]
