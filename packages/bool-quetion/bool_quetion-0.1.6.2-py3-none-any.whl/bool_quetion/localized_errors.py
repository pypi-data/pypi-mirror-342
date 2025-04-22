from pathlib import Path
from json import load as json_load
from os import environ

lang = environ.get('LANG', 'en')[:2]
file_path = Path(__file__).parent / 'errors.json'

with open(file_path, encoding='utf-8') as f:
    ERRORS = json_load(f)

def get_error(key):
    return ERRORS.get(key, {}).get(
            lang, ERRORS.get(key, {}).get(
                'en', f'[Missing error: {key}]'
                )
            )
