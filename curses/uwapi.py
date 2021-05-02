import requests

def get_start_position(game, variant='regular'):
    if game is None:
        return

    r = requests.get(f'https://nyc.cs.berkeley.edu/universal/v1/games/{game}')
    variants = r.json()['response']['variants']

    for v in variants:
        if v['variantId'] == variant:
            return v['startPosition']

    raise Exception(f'Starting position for game {game}, variant "{variant}" not found.')

def get_position(game, variant='regular', position=None):
    if game is None or position is None:
        return

    r = requests.get(f'https://nyc.cs.berkeley.edu/universal/v1/games/{game}/variants/{variant}/positions/{position}')

    return r.json()
