from exceptions import handle

import constants
from utils import sounds



def save_filter(config, parsed_yaml_blocks, output_file_path):
    print('  + Converting YAML to filter syntax')
    filter_blocks = convert_blocks_to_filter_blocks(parsed_yaml_blocks, output_file_path)

    version = f'_{config.version}' if config.version else ''
    file_name = f'{config.name}_{config.league}{version}'
    the_filter = '\n'.join(block for block in filter_blocks)

    with open(f'{output_file_path}/{file_name}.filter', 'w') as f:
        f.write(the_filter)

    print(f'  + Filter saved at {output_file_path}/{file_name}.filter')


def convert_blocks_to_filter_blocks(blocks, output_file_path):
    filter_blocks = []

    for block in blocks:
        filter_blocks.append(convert_block_to_filter_block(block, output_file_path))

    return filter_blocks


def convert_block_to_filter_block(block, output_file_path):
    nosound = any([block.nosound, 'DisableDropSound' in block.show])
    filter_block = f'{block.comment}{block.show}{block.nosound if block.nosound else ""}'

    for line in block.lines:
        if line_should_be_parsed(line, nosound):
            filter_block += parse_line(line, output_file_path)

    return filter_block


def parse_line(line, output_file_path):
    parameter = constants.SYNTAX.get(line.parameter)

    if not parameter:
        msg = (
            f'The filter parameter: {line.parameter} in {line.category_name}/{line.block_name} does not exist.\n'
            'Please check your spelling to make sure you are using the correct parameter name.'
        )

        handle(msg)

    value = get_parsed_value(line, output_file_path)

    return f'\t{parameter} {value}\n'


def get_parsed_value(line, output_file_path):
    # Copy sounds over to the destination sounds folder
    if line.parameter in ['customsound']:
        # Get existing path for custom sound, or copy it to destination_folder/sounds
        sound_path = sounds.get_or_copy_sound_file(output_file_path, line.value)

        return f'"{sound_path}"'

    # These all need quotes.
    if line.parameter in ['bases', 'classes', 'explicit']:
        return ' '.join([f'"{x.strip()}"' for x in line.value.split(',') if x.strip() not in constants.BROKEN_ITEMS])

    # This one is a special case.
    elif line.parameter in ['say']:
        wav_path = sounds.get_or_create_sound(output_file_path, line.value)

        return f'"{wav_path}"'

    # Handle ilvl ranges.
    elif line.parameter in ['ilvl']:
        if '..' in line.value:
            low, high = line.value.split('..')
            return f'>= {low}\n\t{consts.SYNTAX.get(line.parameter)} <= {high}'
        else:
            return line.value

    # These are all booleans that need to be strings.
    elif isinstance(line.value, bool):
        return str(line.value)

    # Everything else can just sit as is.
    return line.value


def line_should_be_parsed(line, nosound):
    cosmetic_lines = ['sound', 'customsound', 'positionalsound', 'icon', 'beam']

    written_from_block = line.parameter in ['show', 'nosound']
    skip_when_nosound = all([nosound, line.parameter in cosmetic_lines])

    if any([written_from_block, skip_when_nosound]):
        return False

    return True
