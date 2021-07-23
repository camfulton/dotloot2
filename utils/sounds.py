import os
import platform
import re
import subprocess


def generate_filename(tosay):
    """Strips all non-alphanumeric (except whitespace) from tosay.

    Also cuts the output down to 50 characters in case one of you
    knuckleheads decides to `tosay` an entire essay.

    Args:
        tosay<str>: the text to be converted into a file name
    Returns:
        <str>: filename
    """
    sanitized = re.sub(r'\W+', '', tosay).strip()[:50]

    return f'{sanitized}.wav'


def generate_sound(full_path, tosay):
    """Calls espeak to generate some speech from your string.

    Args:
        full_path<os.path>: the full path to the file we will write
        tosay<str>: text to be said
    """
    # TODO - the path for espeak should be in config somewhere
    if platform.system() == 'Windows':
        espeak = 'C:\Program Files (x86)\eSpeak\command_line\espeak.exe'
    else:
        espeak = 'espeak'

    subprocess.call(
        [
            espeak,
            '-w',
            full_path,
            '-a',
            '200',
            tosay
        ]
    )


def get_or_create_sound(base_path, tosay):
    """Generates TTS output from the say parameter, returns full path to wav file.

    Does not generate if a file w/ name already exists.

    Strips non-alphanumeric to generate the file name. This can create naming
    conflicts in the event that you had, for example:
        -> `say: it's a mirror`
        and
        -> `say: its a mirror`
    Both would save as `itsamirror.wav`.

    I don't anticipate this being a huge problem, but worth noting.

    Args:
        base_path<os.path>: path to the folder you would like to save the output in
        tosay<str>: text to be said
    Returns:
        <str>: relative path to file (sounds/<filename>.wav)
    """

    filename = generate_filename(tosay)
    rel_path = f'sounds/{filename}'
    full_path = os.path.join(base_path, rel_path)

    if not os.path.exists(full_path):
        sounds_folder = os.path.dirname(full_path)

        if not os.path.exists(sounds_folder):
            os.makedirs(sounds_folder)

        generate_sound(full_path, tosay)

    return rel_path
