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

args = argparser.parse_args()

input_file_path = args.input

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

yaml_parser = Parser(input_file_path, client=client)
config = yaml_parser.load_config()
parsed_yaml_blocks = yaml_parser.parse_yaml_into_blocks()

yaml_parser.print_warnings()

save_filter(config, parsed_yaml_blocks, output_path)
