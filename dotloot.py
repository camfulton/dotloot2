import argparse

from config import config
from utils.filter_writer import save_filter
from utils.yaml_parser import Parser



argparser = argparse.ArgumentParser()

argparser.add_argument(
    'input',
    type=str,
    help='Relative path to the fitler yaml: filters\\leaguename\\cool_filter1.yaml'
)

argparser.add_argument(
    '--skip-lookups',
    action='store_true',
    help='If you would like to skip lookup blocks, for early league when there is no data.'
)

argparser.add_argument(
    '--leveling',
    action='store_true',
    help='Enables blocks with the `leveling` key.'
)

argparser.add_argument(
    '--earlygame',
    action='store_true',
    help='Enables blocks with the `earlygame` key.'
)

argparser.add_argument(
    '--include-no-variant',
    action='store_true',
    help='Includes items without any variant in lookups.'
)

args = argparser.parse_args()

input_file_path = args.input
skip_lookups = args.skip_lookups
leveling = args.leveling
earlygame = args.earlygame
include_no_variant = args.include_no_variant

try:
    output_path = config['output_path']
except KeyError as e:
    print('You must configure an output_path in config.py')
    exit(0)

try:
    client = config['client']

except KeyError as e:
    print('You must configure a client in config.py')
    exit(0)

yaml_parser = Parser(input_file_path, client, skip_lookups, leveling, earlygame, include_no_variant)
config = yaml_parser.load_config()
parsed_yaml_blocks = yaml_parser.parse_yaml_into_blocks()

yaml_parser.print_warnings()

save_filter(config, parsed_yaml_blocks, output_path)
