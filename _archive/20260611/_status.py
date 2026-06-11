import csv, json, sqlite3, os

BASE = os.path.dirname(os.path.abspath(__file__))
HISTORY = os.path.join(BASE, "history.csv")
DB_ROOT = os.path.join(BASE, "framework.db")
DB = os.path.join(BASE, "data", "framework.db")
DATA = os.path.join(BASE, "data")
SCRIPT_DIR = r"C:\Users\gjj\Documents\New project"


def show_history():
    if not os.path.exists(HISTORY):
        print("  (no history)")
        return
    with open(HISTORY, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("  (empty)")
        return
    print(f"  Total {len(rows)} records:")
    print(f"  {'Date':<12} {'Home':<12} {'Away':<12} {'Dir':<6} {'Score':<8} {'Hit':<4}")
    print("  " + "-" * 54)
    for r in reversed(rows[-15:]):
        hit = r.get("hit", "")
        hs = "OK" if hit == "True" else ("NO" if hit == "False" else " -")
        d = r.get("date", "")[:10]
        h = r.get("home", "")[:10]
        a = r.get("away", "")[:10]
        dr = r.get("direction", "")[:6]
        sc = r.get("actual_score", "")[:8]
        print(f"  {d:<12} {h:<12} {a:<12} {dr:<6} {sc:<8} {hs:<4}")


def show_db():
    db_path = DB_ROOT if (os.path.exists(DB_ROOT) and os.path.getsize(DB_ROOT) > 0) else DB
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        print("  (DB empty or missing)")
        return
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        run = conn.execute("SELECT * FROM runs ORDER BY id DESC LIMIT 1").fetchone()
        if not run:
            print("  (no runs)")
            conn.close()
            return
        rid = run["id"]
        mc = conn.execute("SELECT COUNT(*) as c FROM matches WHERE run_id=?", (rid,)).fetchone()["c"]
        hc = conn.execute("SELECT COUNT(*) as c FROM matches WHERE run_id=? AND hit=1", (rid,)).fetchone()["c"]
        avg = run["avg_fit_score"]
        line = f"  Run #{rid} | {run['date']} | {run['run_type']}"
        if avg:
            line += f" | {mc} matches | {hc} hits | avg_fit={avg:.2f}"
        print(line)
        conn.close()
    except Exception as e:
        print(f"  (DB error: {e})")


def show_data_dir():
    if not os.path.exists(DATA):
        print("  (not found)")
        return
    for entry in sorted(os.listdir(DATA)):
        ep = os.path.join(DATA, entry)
        if os.path.isdir(ep):
            subs = os.listdir(ep) if os.path.exists(ep) else []
            print(f"  data/{entry}/  ({len(subs)} items)")
        else:
            sz = os.path.getsize(ep)
            if sz > 0 and not entry.startswith("."):
                print(f"  data/{entry}  ({sz} bytes)")


def show_scripts():
    if not os.path.exists(SCRIPT_DIR):
        print("  (not found)")
        return
    scripts = sorted(f for f in os.listdir(SCRIPT_DIR) if f.endswith(".py"))
    print(f"  Path: {SCRIPT_DIR}")
    print(f"  Count: {len(scripts)} scripts")
    for ks in ["fetch_jczq.py", "fetch_injuries.py", "fetch_season_data.py", "fetch_recent.py"]:
        ok = os.path.exists(os.path.join(SCRIPT_DIR, ks))
        print(f"  {'OK' if ok else '--'} {ks}")


def show_changes():
    cp = os.path.join(BASE, "_changes.json")
    if not os.path.exists(cp):
        print("  (no change log)")
        return
    try:
        data = json.loads(open(cp, "r", encoding="utf-8").read())
        changes = data.get("changes", [])
        if not changes:
            print("  (empty)")
            return
        print(f"  Total {len(changes)} records, showing last 8:")
        print(f"  {'Date':<16} {'By':<12} {'File':<28} {'Summary':<30}")
        print("  " + "-" * 86)
        for c in changes[-8:]:
            dt = c.get("at", "")[:14]
            by = c.get("by", "?")
            fn = c.get("file", "?")
            sm = c.get("summary", "")[:28]
            print(f"  {dt:<16} {by:<12} {fn:<28} {sm:<30}")
    except Exception as e:
        print(f"  (read error: {e})")


if __name__ == "__main__":
    print("=" * 62)
    print("  V3.3.3-Core Framework Status")
    print("=" * 62)

    print("\n[Recent Predictions]")
    show_history()

    print("\n[Latest DB Run]")
    show_db()

    print("\n[Data Dir]")
    show_data_dir()

    print("\n[Data Scripts]")
    show_scripts()

    print("\n[Change Log]")
    show_changes()

    # --- Journal / Task Context ---
    journal_path = os.path.join(BASE, '_journal.md')
    if os.path.exists(journal_path):
        journal = open(journal_path, 'r', encoding='utf-8').read()
        if '## 当前状态' in journal:
            state = journal[journal.index('## 当前状态'):]
            if '`' in state:
                state = state[:state.index('`')]
            print('\n[Current Task]')
            for line in state.strip().split('\n'):
                if line.strip():
                    print('  ' + line.strip())
        entries = [l for l in journal.split('\n## ') if l.strip().startswith('2026')][-3:]
        if entries:
            print('\n[Recent Journal]')
            for entry in entries:
                title = entry.split('\n')[0][:60]
                print('  ' + title)

    print("\n" + "=" * 62)
