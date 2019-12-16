from collections.abc import MutableMapping, Sequence
import requests


def flatten_dict(d, parent_key='', sep='_', chain_key_names=True):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if chain_key_names and parent_key else k
        if isinstance(v, MutableMapping):
            children = flatten_dict(
                    v, new_key, sep=sep, chain_key_names=chain_key_names
                    )
            items.extend(children.items())
        else:
            items.append((new_key, v))
    return dict(items)


def fetch_gumbo_live_feed(game_pk):
    url = f'https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live'
    return requests.get(url).json()


def extract_pitches(gumbo_json, which_plays='allPlays'):

    plays = gumbo_json['liveData']['plays'][which_plays]
    if not isinstance(plays, Sequence):
        plays = list(plays)

    pitches = []
    for play in plays:
        about = play['about']
        inning = about['inning']
        halfInning = about['halfInning']
        atBatIndex = about['atBatIndex']
        pitcherId = play['matchup']['pitcher']['id']
        pitchHand = play['matchup']['pitchHand']['code']

        play_events = play['playEvents']
        for ievent, event in enumerate(play_events):
            if event['type'] != 'pitch':
                continue
            try:
                pitch_type_code = event['details']['type']['code']
                pitch_data = event['pitchData']
                pitch_meas = flatten_dict(pitch_data, chain_key_names=False)
                pitch_flat = {
                        'gamePk': gumbo_json['gamePk'],
                        'inning': inning,
                        'halfInning': halfInning,
                        'atBatIndex': atBatIndex,
                        'pitchIndex': event['index'],
                        'pitchTypeCode': pitch_type_code,
                        'pitcherId': pitcherId,
                        'pitchHand': pitchHand,
                        'playId': event['playId'],
                        **pitch_meas,
                        }
                pitches.append(pitch_flat)
            except KeyError:
                continue

    return pitches


def schedule(sportId, venueIds, startMMDDYYYY, endMMDDYYYY, flatten=False):
    params = f'sportId={sportId}'
    if venueIds is not None:
        params += f'&venueIds={venueIds}'
    params += f'&startDate={startMMDDYYYY}'
    params += f'&endDate={endMMDDYYYY}'
    url = f'https://statsapi.mlb.com/api/v1/schedule/?{params}'
    r = requests.get(url)
    json = r.json()

    if flatten:
        def flat(d): return flatten_dict(d)
    else:
        def flat(d): return d

    games = []
    for date in json['dates']:
        games.extend([flat(game) for game in date['games']])

    return games
