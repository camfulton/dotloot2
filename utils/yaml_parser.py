import yaml
from yaml.scanner import ScannerError

import constants
from exceptions import handle
from collections import namedtuple

# Stores the data from the `Config` block.
Config = namedtuple("Config", ["name", "league", "version"])

# Used to store filter data after parsing.
Block = namedtuple(
    "Block", ["lines", "show", "nosound", "comment", "category", "lookup"]
)

# A line in a block, these are written out to the filter.
Line = namedtuple("Line", ["parameter", "value", "category_name", "block_name"])


class Parser:
    def __init__(
        self,
        input_file_path,
        client,
        skip_lookups,
        leveling,
        weapons,
        links,
        earlygame,
        include_no_variant,
    ):
        self.input_file_path = input_file_path
        self.skip_lookups = skip_lookups
        self.yaml = self.load_yaml()
        self.leveling = leveling
        self.weapons = weapons
        self.links = links
        self.earlygame = earlygame
        self.include_no_variant = include_no_variant
        # TODO - Do we need this ont the object?
        self.config = self.load_config()
        self.client = client(league=self.config.league)
        self.warnings = []
        self.normal = constants.FRAME_TYPES["NORMAL"]
        self.magic = constants.FRAME_TYPES["MAGIC"]
        self.rare = constants.FRAME_TYPES["RARE"]
        self.unique = constants.FRAME_TYPES["UNIQUE"]
        self.gem = constants.FRAME_TYPES["GEM"]
        self.currency = constants.FRAME_TYPES["CURRENCY"]
        self.divination_card = constants.FRAME_TYPES["DIVINATION_CARD"]
        self.quest_item = constants.FRAME_TYPES["QUEST_ITEM"]
        self.relic = constants.FRAME_TYPES["RELIC"]
        self.show_string = "Show\n"

    def print_warnings(self):
        print("  |")
        print("  @@@ WARNINGS @@@")
        print("  |")
        for warning in self.warnings:
            print(warning)
        if not self.warnings:
            print("  | - No warnings :)")
        print("  |")

    def load_yaml(self):
        try:
            with open(self.input_file_path, "r") as f:
                yaml_data = yaml.load(f, Loader=yaml.SafeLoader)
                self._preflight_checks(yaml_data)
                return yaml_data
        except FileNotFoundError:
            msg = f"There is no file at: {self.input_file_path}"
            handle(msg)
        except ScannerError:
            msg = "There is a yaml syntax error somewhere in your filter file, see above traceback for more detail."
            handle(msg, stacktrace=True)

    def _preflight_checks(self, yaml_data):
        try:
            yaml_data["blocks"]
        except KeyError:
            msg = "You need a `blocks` section in your yaml.\n\nSee `filters/example.yaml` for example."
            handle(msg)

        try:
            yaml_data["config"]
        except KeyError:
            msg = "You need a `config` section in your yaml.\n\nSee `filters/example.yaml` for example."
            handle(msg)

        for config_key in constants.CONFIG_KEYS:
            try:
                yaml_data["config"][config_key]
            except KeyError:
                self._missing_config(config_key)

    def load_config(self):
        if not self.yaml:
            raise Exception("Ruh roh! No yaml to load the config from! Oh no!")

        yaml_config = self.yaml["config"]

        keys = {}

        for config_key in constants.CONFIG_KEYS:
            keys[config_key] = yaml_config[config_key]

        # TODO - do we actually need this on the object?
        self.config = Config(**keys)

        return Config(**keys)

    def parse_yaml_into_blocks(self):
        # Convert the raw YAML to our Blocks & Lines for easier processing.
        blocks = self.convert_yaml_to_blocks()

        # Perform lookups on all blocks w/ the lookup property set to True
        blocks = self.perform_lookups(blocks)

        return blocks

    def perform_lookups(self, blocks):
        """Handles: `lookup: <category> <value>` lines from filters

        Some of our blocks at this point will have lines like:
        Line(
            parameter: 'lookup',
            value: 'bases 50',
            category_name: '50c+ item bases',
            block_name: 'Bases'
        )

        These blocks will be tagged w/ block.lookup == True.

        We need to extract the lookup type, value, and (for uniques), exclusivity check
        and then break these blocks into (potentially) many blocks.

        In the case of a 50c+ base lookup we use the client to query the pricing website
        for all base types. We would then cycle through them and create a block with all
        the core elements (colors, beams, map icons, sounds) from the dummy Block, and
        then fill in stuff like ilvl, variant, etc. from the website data for any class
        of item that matches the price parameter.

        There is some additional logic for doing exclusive unique item lookup etc.
        """
        new_blocks = []

        for block in blocks:
            if not block.lookup:
                new_blocks.append(block)
                continue

            if not self.skip_lookups:
                item_groups = self.client.get_item_groups_for_block(block)

                for item_group in item_groups:
                    new_block = self.generate_block_from_lookup_result(
                        item_group, block
                    )

                    if new_block:
                        new_blocks.append(new_block)

        return new_blocks

    def generate_block_from_lookup_result(self, item_group, block):
        an_item = item_group[0] if item_group else None
        lines = []

        is_exclusive_lookup = (
            self.client.parse_lookup(block).type
            == self.client.ITEM_TYPES["exclusive uniques"].type
        )

        if not an_item and not is_exclusive_lookup:
            msg = (
                f"  ! Something went wrong when looking up <{block.lines[0].block_name}>, got no items back.\n"
                "  ! This category was skipped and will not appear in your filter."
            )
            self.warnings.append(msg)

            return None
        elif not an_item and is_exclusive_lookup:
            # Sometimes there aren't any unique bases that are always worth your min chaos threshold
            return None

        if not an_item:
            # satisfying the type checker, this should never execute
            raise Exception("UHHH WE GOT A PROBLEM HERE BUB")

        category_name = block.lines[0].category_name
        block_name = block.lines[0].block_name

        name_key = self.client.PROPERTY_SYNTAX["name"]
        frame_type_key = self.client.PROPERTY_SYNTAX["frame_type"]
        variant_key = self.client.QUALIFIER_SYNTAX["variant"]
        ilvl_key = self.client.QUALIFIER_SYNTAX["ilvl"]
        base_type_key = self.client.PROPERTY_SYNTAX["base_type"]

        variant = an_item.get(variant_key, "")
        ilvl = an_item.get(ilvl_key, 0)
        frame_type = an_item.get(frame_type_key)
        name = an_item.get(name_key)
        base_type = an_item.get(base_type_key)
        is_normal_magic_or_rare = frame_type in [self.normal, self.magic, self.rare]
        is_incubator = all([frame_type == self.currency, "incubator" in name.lower()])
        is_lure = all([frame_type == self.normal, "lure" in name.lower()])
        is_fossil = all([frame_type == self.currency, "fossil" in name.lower()])
        is_scarab = all([frame_type == self.normal, "scarab" in name.lower()])
        is_essence = all([frame_type == self.currency, "essence" in name.lower()])
        is_oil = all([frame_type == self.currency, "oil" in name.lower()])

        # Avoid things like Shaper/Hunter bases that do not naturally drop, for example.
        if self.is_awakener_orb_result(variant):
            return None
        if self.is_unknown_variant(variant, is_normal_magic_or_rare):
            # Only want to alert on things we really don't know about.
            if not self.is_awakener_orb_result(variant):
                print(
                    f"  ! Skipping unknown or no-drop variant: Item: {name} | Type: {constants.FRAME_TYPES[frame_type]} | Variant: {variant}"  # noqa
                )
            return None

        # Handle naturally occurring basetypes w/ variants or high item levels
        if all(
            [
                is_normal_magic_or_rare,
                any([variant, ilvl > 84, self.include_no_variant]),
            ]
        ):
            lines = [line for line in block.lines if line.parameter != "ilvl"]

            lines.append(Line("ilvl", f">= {ilvl}", category_name, block_name))

            if variant:
                lines.append(Line("influence", variant, category_name, block_name))

        elif frame_type == self.gem:
            gem_properties = ["quality", "gemlvl", "corrupted"]

            lines = [
                line for line in block.lines if line.parameter not in gem_properties
            ]

            quality_value = f'>= {an_item[self.client.QUALIFIER_SYNTAX["quality"]]}'
            lines.append(Line("quality", quality_value, category_name, block_name))

            gem_lvl_value = f'>= {an_item[self.client.QUALIFIER_SYNTAX["gemlvl"]]}'
            lines.append(Line("gemlvl", gem_lvl_value, category_name, block_name))

            corrupted_value = an_item[self.client.QUALIFIER_SYNTAX["corrupted"]]
            lines.append(Line("corrupted", corrupted_value, category_name, block_name))

        elif any(
            [
                frame_type == self.divination_card,
                is_oil,
                is_incubator,
                is_lure,
                is_fossil,
                is_scarab,
                is_essence,
            ]
        ):
            items = ",".join(
                set([item[name_key] for item in item_group if item.get(name_key)])
            )

            lines = [line for line in block.lines]

            lines.append(Line("bases", items, category_name, block_name))

        elif all([is_normal_magic_or_rare, not variant, not self.include_no_variant]):
            msg = (
                "  |\n"
                "  ! Skipping base items with no variant as they are almost always false flags.\n"
                "  ! If this is pissing you off, you should rerun with the --include_no_variant flag.\n"
                "  |\n"
                "  ! The following items were skipped as a result:\n"
                "  |\n"
            )

            for item in item_group:
                msg += f"  | ~ Item: {item[name_key]} | Type: {item[frame_type_key]} | Variant: {item.get(variant_key)} | ilvl: {item[ilvl_key]}\n"  # noqa

            # get rid of the final newline
            self.warnings.append(msg[:-1])

            return None

        elif not frame_type == self.unique:
            # If we fail to catch something here we should warn the user at the end of the script.
            # We handle uniques below in the basetype step, & so do not register those as a warning.
            msg = (
                "  |\n"
                f"  ! Failed to parse lookup result for {block_name}.\n"
                "  !\n"
                "  ! This could be a bug, it could also be\n"
                "  ! some kind of error w/ the client API you are using.\n"
                "  !\n"
                "  ! The following items were skipped as a result:\n"
                "  |\n"
            )

            for item in item_group:
                msg += (
                    f'  | ~ Item: {item.get(name_key, f"No item name found at key: {name_key}")}'
                    f' | Type: {item.get(frame_type_key, f"No item type found at key: {frame_type_key}")}'
                    f' | Variant: {item.get(variant_key, f"No item variant found at key: {variant_key}")}'
                    f' | ilvl: {item.get(ilvl_key, f"No item ilvl found at key: {ilvl_key}")}'
                    f' | frame_type: {frame_type})\n'
                )

            # get rid of the final newline
            self.warnings.append(msg[:-1])

            return None

        if base_type:
            # If we haven't hit any of the above then we need to copy all the lines over
            if not lines:
                lines = [line for line in block.lines]

            bases = ",".join(
                set([item["baseType"] for item in item_group if item.get("baseType")])
            )

            lines.append(Line("bases", bases, category_name, block_name))

        comment = self.header_comment(category_name, block_name, extras=[variant])

        return Block(lines, block.show, block.nosound, comment, block.category, True)

    def is_awakener_orb_result(self, variant):
        if "/" not in variant:
            return False
        awakener_orb_result = [
            1
            for kv in constants.VARIANTS_THAT_MATTER_FOR_FILTERS
            if kv in variant.upper()
        ]

        return bool(awakener_orb_result)

    def is_unknown_variant(self, variant, is_normal_magic_or_rare):
        unknown_variant = (
            variant.upper() not in constants.VARIANTS_THAT_MATTER_FOR_FILTERS
        )

        # If the item has a variant, that variant is not HUNTER/REDEEMER or similar, and it has a base of some kind
        # then we are probably dealing w/ the result of something unnatural and should alert on it.
        if all(
            [
                variant,
                unknown_variant,
                not self.is_awakener_orb_result(variant),
                is_normal_magic_or_rare,
            ]
        ):
            return True

        return False

    def convert_yaml_to_blocks(self):
        """Convert the yaml structure into blocks and lines.

        The filters are structured as:
        blocks:
            category:
                block_in_category:
                    attribute: true
                    ...
                block_in_category:
                    attribute: false
                    ...
                ...
            ...

        blocks:
            currency:                            <-- Referenced in the comment in the `Block` for debugging.
                great_currency:                            <-- Stored as a `Block`.
                    show: true                                      <-- Stored as a property on `Block`.
                    fg: 255 0 0 0                                      <-,
                    classes: Currency                                    |-- Stored as `Lines` in the `Block`.
                    bases: Mirror of Kalandra, Mirror Shard            <-`
                trash_currency:
                    show: false
                    classes: Currency
                    bases: Transmutation Shard, Scroll of Wisdom
        """
        print("- Converting yaml")
        blocks = []
        if not self.yaml:
            raise Exception("Ahhh! No yaml to convert to blocks! How???")

        yaml_blocks = self.yaml["blocks"]

        for category, blocks_in_category in yaml_blocks.items():
            print(f"  + Parsing: {category}")
            blocks.extend(self.convert_category_to_blocks(category, blocks_in_category))

        return blocks

    def convert_category_to_blocks(self, category, blocks_in_category):
        blocks = []

        for block_name, yaml_lines in blocks_in_category.items():
            print(f"  | - Reading lines for: {block_name}")
            if block_name == "__leveling__":
                # this is a little janky but whatever, storing the weapon & link lists as lines here
                blocks.append(
                    Block(
                        [self.weapons, self.links],
                        self.show_string,
                        False,
                        self.header_comment(category, block_name),
                        category,
                        False,
                    )
                )

                continue
            lines = []
            skip = False
            show = self.show_or_hide_and_disable_dropsound(yaml_lines)
            lookup = yaml_lines.get("lookup", False)
            nosound = self.disable_drop_sound(yaml_lines)
            comment = self.header_comment(category, block_name)

            for parameter, value in yaml_lines.items():
                # TODO -- Should we store them as lines?
                # We write these later from the Block, do not store as lines.
                if parameter in ["show", "lookup"]:
                    continue

                if parameter in ["leveling"] and not self.leveling:
                    print(
                        f"  ! Skipping block: {block_name} because it is tagged as a leveling block. Pass the --leveling flag to enable this block."  # noqa
                    )
                    skip = True

                if parameter in ["earlygame"] and not self.earlygame:
                    print(
                        f"  ! Skipping block: {block_name} because it is tagged as a leveling block. Pass the --earlygame flag to enable this block.\n\n\n\nNote to self: does this work or are you still seeing dogshit div cards etc? Might need to explicitly hide rather than not parse these blocks?"  # noqa
                    )
                    skip = True

                lines.append(Line(parameter, value, category, block_name))

            if not skip:
                blocks.append(Block(lines, show, nosound, comment, category, lookup))

        return blocks

    def show_or_hide_and_disable_dropsound(self, yaml_lines):
        return (
            self.show_string
            if yaml_lines.get("show", True)
            else "Hide\n\tDisableDropSound\n"
        )

    def disable_drop_sound(self, yaml_block_lines):
        return "\tDisableDropSound\n" if yaml_block_lines.get("nosound") else None

    def header_comment(self, category_name, block_name, extras=[]):
        line_end = "".join([f"/{extra}" for extra in extras]) + "\n"

        return f"\n# {category_name}/{block_name}{line_end}"

    def _missing_config(self, parameter):
        handle(
            f"Your filter needs to set `{parameter}` in its `config` section.\n"
            "See `filters/example.yaml` for example."
        )
