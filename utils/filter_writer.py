from exceptions import handle

import constants
from utils import sounds
from utils.leveling.generator import generate_leveling_filter_blocks

""" How this thing currently works - 7/25/2024

First, save_filter is called by dotloot.py - this is the entry point.
save_filter takes in parsed yaml blocks from a filter in /filters.

These parsed yaml blocks are `Block` namedtuples. They contain lines which
are `Line` namedtuples. These Lines contain params, values, categories, and block names.

The Blocks also contain metadata such as show, nosound, comment, category, and lookup.

These are the sort of confusing data primitives we work with here. Basically, a Block is
a unit of yaml to be converted into a filter and a Line is an actual line of yaml from
that block.

So first we convert raw yaml into these Block and Line things, then we use these
Blocks and Lines to generate filter syntax.


So, we call save_filter with our Blocks and convert those Blocks into filter blocks.

This process begins with metadata - we make a string with something like:
"comment\nshow or hide\nnosound?\n" in it and then append any relevant filter data
to that string for each block by parsing the lines - this is where we add things like
itemLevel, rarity, etc.

There are also checks for line parsing that trigger things like TTS generation etc.
"""


def save_filter(config, parsed_yaml_blocks, output_file_path):
    print("  + Converting YAML to filter syntax")
    filter_blocks = convert_blocks_to_filter_blocks(
        parsed_yaml_blocks, output_file_path
    )

    version = f"_{config.version}" if config.version else ""
    file_name = f"{config.name}_{config.league}{version}"
    the_filter = "\n".join(block for block in filter_blocks)
    extension = "ruthlessfilter" if "ruthless" in config.name else "filter"

    with open(f"{output_file_path}/{file_name}.{extension}", "w") as f:
        f.write(the_filter)

    print(f"  + Filter saved at {output_file_path}/{file_name}.{extension}")


def convert_blocks_to_filter_blocks(blocks, output_file_path):
    filter_blocks = []

    for block in blocks:
        filter_blocks.append(convert_block_to_filter_block(block, output_file_path))

    return filter_blocks


def convert_block_to_filter_block(block, output_file_path):
    nosound = any([block.nosound, "DisableDropSound" in block.show])
    filter_block = (
        f"{block.comment}{block.show}{block.nosound if block.nosound else ''}"
    )

    if "__leveling__" in block.comment:
        return generate_leveling_filter_blocks(block, output_file_path)

    for line in block.lines:
        if line_should_be_parsed(line, nosound):
            filter_block += parse_line(line, output_file_path)

    return filter_block


def parse_line(line, output_file_path):
    parameter = constants.SYNTAX.get(line.parameter)

    if not parameter:
        msg = (
            f"The filter parameter: {line.parameter} in {line.category_name}/{line.block_name} does not exist.\n"
            "Please check your spelling to make sure you are using the correct parameter name."
        )

        handle(msg)

    value = get_parsed_value(line, output_file_path)

    return f"\t{parameter} {value}\n"


def get_parsed_value(line, output_file_path):
    # Copy sounds over to the destination sounds folder
    if line.parameter in ["customsound"]:
        # Get existing path for custom sound, or copy it to destination_folder/sounds
        sound_path = sounds.get_or_copy_sound_file(output_file_path, line.value)

        return f'"{sound_path}"'

    # These all need quotes.
    if line.parameter in [
        "bases",
        "classes",
        "explicit",
        "nem",
        "clusterenchant",
        "influence",
    ]:
        return " ".join(
            [
                f'"{x.strip()}"'
                for x in line.value.split(",")
                if x.strip() not in constants.BROKEN_ITEMS
            ]
        )

    # This one is a special case.
    elif line.parameter in ["say"]:
        wav_path = sounds.get_or_create_sound(output_file_path, line.value)

        return f'"{wav_path}"'

    # Handle ilvl ranges.
    elif line.parameter in ["ilvl", "alvl", "droplevel"]:
        if ".." in line.value:
            low, high = line.value.split("..")
            return f">= {low}\n\t{constants.SYNTAX.get(line.parameter)} <= {high}"
        else:
            return line.value

    # These are all booleans that need to be strings.
    elif isinstance(line.value, bool):
        return str(line.value)

    # Everything else can just sit as is.
    return line.value


def line_should_be_parsed(line, nosound):
    cosmetic_lines = ["sound", "customsound", "positionalsound", "icon", "beam", "say"]
    config_lines = ["leveling", "earlygame"]

    written_from_block = line.parameter in ["show", "nosound"]
    config = line.parameter in config_lines
    skip_when_nosound = all([nosound, line.parameter in cosmetic_lines])

    if any([written_from_block, skip_when_nosound, config]):
        return False

    return True
