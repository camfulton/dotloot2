import argparse

from config import config
from utils.filter_writer import save_filter
from utils.yaml_parser import Parser


argparser = argparse.ArgumentParser()

argparser.add_argument(
    "input",
    type=str,
    help="Relative path to the fitler yaml: filters\\leaguename\\cool_filter1.yaml",
)

argparser.add_argument(
    "--skip-lookups",
    action="store_true",
    help="If you would like to skip lookup blocks, for early league when there is no data. Defaults to False.",
)

argparser.add_argument(
    "--leveling",
    action="store_true",
    help="Generates a leveling section at the location of your `__leveling__` block. Defaults to False.",
)

argparser.add_argument(
    "-w",
    "--weapon",
    action="append",
    help="Generates weapon progression for the specified weapon type, can be set multiple times for multiple weapon types.",  # noqa
)

argparser.add_argument(
    "-l",
    "--links",
    action="append",
    help="Generates a filter that looks for RRG or GGGG etc., can be set multiple times for multiple links.",  # noqa
)

argparser.add_argument(
    "--earlygame",
    action="store_true",
    help="Enables blocks with the `earlygame` key. Defaults to False.",
)

argparser.add_argument(
    "--include-no-variant",
    action="store_true",
    help="Includes items without any variant in lookups. Defaults to False.",
)

argparser.add_argument(
    "--poe2",
    action="store_true",
    help="Output a poe2 filter",
)

args = argparser.parse_args()

input_file_path = args.input
skip_lookups = args.skip_lookups
leveling = args.leveling
weapons = args.weapon
links = args.links
earlygame = args.earlygame
include_no_variant = args.include_no_variant
poe2 = args.poe2

try:
    if poe2:
        output_path = config["poe2_output_path"]
    else:
        output_path = config["poe1_output_path"]
except KeyError:
    print("You must configure an output path in config.py")
    exit(0)

try:
    client = config["client"]

except KeyError:
    print("You must configure a client in config.py")
    exit(0)

yaml_parser = Parser(
    input_file_path,
    client,
    skip_lookups,
    leveling,
    weapons,
    links,
    earlygame,
    include_no_variant,
)
config = yaml_parser.load_config()
parsed_yaml_blocks = yaml_parser.parse_yaml_into_blocks()

yaml_parser.print_warnings()

save_filter(config, parsed_yaml_blocks, output_path)
