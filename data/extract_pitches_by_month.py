import statsapi
import pandas as pd
import argparse
import calendar


def main(year, month, limit):

    _, last_day = calendar.monthrange(year, month)
    sportId = 1
    venueIds = None
    start = f'{month:02}/01/{year}'
    end = f'{month:02}/{last_day:02}/{year}'
    games = statsapi.schedule(sportId, venueIds, start, end)

    pitches_month = []
    for game in games if limit < 0 else games[:limit]:
        pk = game['gamePk']
        print(f'downloading {pk}')
        gumbo_json = statsapi.fetch_gumbo_live_feed(pk)
        pitches_game = statsapi.extract_pitches(gumbo_json)

        pitches_month.extend(pitches_game)

    df = pd.DataFrame(pitches_month)
    df = df.drop(columns=['x', 'y', 'strikeZoneTop', 'strikeZoneBottom', 'zone', 'typeConfidence', 'breakAngle', 'breakLength', 'breakY'])
    df.to_csv(f'pitches_{year}_{month:02}.csv')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int)
    parser.add_argument('month', type=int)
    parser.add_argument('--limit', type=int, default=-1)
    args = parser.parse_args()
    main(args.year, args.month, args.limit)
