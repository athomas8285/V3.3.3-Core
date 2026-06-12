import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(data, filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'  [OK] {filename}')

def calculate_avg_xg(xg_list):
    values = [m.get('xg_for') for m in xg_list if m.get('xg_for') is not None]
    if values:
        return round(sum(values) / len(values), 2)
    return None

def calculate_avg_xga(xg_list):
    values = [m.get('xg_against') for m in xg_list if m.get('xg_against') is not None]
    if values:
        return round(sum(values) / len(values), 2)
    return None

def main():
    locked = load_json('locked_data.json')
    sofa = load_json('sofascore_data.json')

    if not locked.get('matches'):
        print('[ERROR] No matches in locked_data.json')
        return

    if not sofa:
        print('[WARN] No sofascore_data.json found. Run fetch_sofascore_data.py first.')
        return

    updated = 0
    for m in locked.get('matches', []):
        mid = m.get('id', '')
        home = m.get('home', '')
        away = m.get('away', '')

        # Find matching SofaScore data by team names
        sd = None
        for smid, smd in sofa.items():
            if smd.get('home') == home and smd.get('away') == away:
                sd = smd
                break

        if not sd:
            continue

        s = sd.get('sofascore', sd)  # handle both formats
        event_id = s.get('event_id', s.get('eventId'))

        if not event_id:
            continue

        # Update data based on SofaScore
        # 1. Missing players / injuries
        missing_home = s.get('missing_home', s.get('missingPlayers', {}).get('home', []))
        missing_away = s.get('missing_away', s.get('missingPlayers', {}).get('away', []))

        if len(missing_home) > 0:
            m['injury_home_missing'] = False
        if len(missing_away) > 0:
            m['injury_away_missing'] = False
        # If we got lineup data at all, the source is reliable
        if s.get('has_lineups') or 'missing_home' in s or 'missing_away' in s or 'missingPlayers' in s:
            m['injury_source_unreliable'] = False
            m['roster_missing'] = False

        # 2. H2H
        h2h = s.get('h2h', [])
        if h2h:
            m['h2h_missing'] = False

        # 3. xG data
        xg_home = s.get('xg_home', [])
        xg_away = s.get('xg_away', [])

        if xg_home:
            avg_xg = calculate_avg_xg(xg_home)
            avg_xga = calculate_avg_xga(xg_home)
            if avg_xg is not None:
                m['home_xg'] = avg_xg
            if avg_xga is not None:
                m['home_xga'] = avg_xga
            m['xg_last3_missing'] = False
            m['xg_season_missing'] = False

        if xg_away:
            avg_xg = calculate_avg_xg(xg_away)
            avg_xga = calculate_avg_xga(xg_away)
            if avg_xg is not None:
                m['away_xg'] = avg_xg
            if avg_xga is not None:
                m['away_xga'] = avg_xga
            m['xg_last3_missing'] = False
            m['xg_season_missing'] = False

        # 4. Venue info could help determine motivation context
        # (not directly mappable to existing fields)

        updated += 1
        print(f'  {mid} {home} vs {away}: injuries={len(missing_home)}/{len(missing_away)}, '
              f'h2h={len(h2h)}, xg_home={len(xg_home)}, xg_away={len(xg_away)}')

    if updated > 0:
        save_json(locked, 'locked_data.json')
    print("Enriched " + str(updated) + "/" + str(len(locked.get("matches",[]))) + " matches with SofaScore data.")

if __name__ == '__main__':
    main()
