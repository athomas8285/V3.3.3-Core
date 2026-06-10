import os, sys, json, shutil, tempfile, subprocess
BASE_DIR = r"C:\Users\gjj\Desktop\v333"
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def find_archived_runs():
    runs = []
    for d in sorted(os.listdir(PROCESSED_DIR)):
        dp = os.path.join(PROCESSED_DIR, d)
        if not os.path.isdir(dp): continue
        l = os.path.join(dp, "locked_data.json")
        f = os.path.join(dp, "factor_params.json")
        if os.path.exists(l) and os.path.exists(f):
            runs.append({"name": d, "locked": l, "factors": f})
    return runs

def main():
    import sys
    archived = find_archived_runs()
    if not archived:
        print("No archived runs")
        return
    print("Found " + str(len(archived)) + " archived runs:")
    for a in archived:
        print("  " + a["name"])
    
    from database import insert_run, insert_match
    
    for a in archived:
        print("\nBacktest: " + a["name"])
        tmp = tempfile.mkdtemp(prefix="bt_")
        try:
            shutil.copy(a["locked"], os.path.join(tmp, "locked_data.json"))
            shutil.copy(a["factors"], os.path.join(tmp, "factor_params.json"))
            
            with open(a["locked"], encoding="utf-8") as f:
                locked = json.load(f)
            
            info = []
            for m in locked["matches"]:
                info.append({
                    "id": m.get("id",""), "home": m.get("home",""), "away": m.get("away",""),
                    "event": m.get("event",""), "time": m.get("time",""),
                    "sp_home": m.get("sp_home"), "sp_draw": m.get("sp_draw"), "sp_away": m.get("sp_away"),
                    "initial_sp_home": m.get("initial_sp_home"), "initial_sp_draw": m.get("initial_sp_draw"),
                    "initial_sp_away": m.get("initial_sp_away"),
                    "asian_handicap": m.get("asian_handicap",0), "handicap_change": m.get("handicap_change",0),
                    "match_type": m.get("match_type",""), "is_home_life_death": m.get("is_home_life_death",False),
                    "lambda_diff": 0, "physical_direction": "home", "predicted_direction": "home",
                    "h2h_confidence": "api" if not m.get("h2h_missing") else "infer",
                    "xg_last3_confidence": "calc" if not m.get("xg_last3_missing") else "infer",
                    "xg_season_confidence": "api" if not m.get("xg_season_missing") else "infer",
                    "roster_confidence": "api" if not m.get("roster_missing") else "infer",
                    "injury_home_confidence": "api" if not m.get("injury_home_missing") else "infer",
                    "injury_away_confidence": "api" if not m.get("injury_away_missing") else "infer",
                    "injury_source_confidence": "calc" if not m.get("injury_source_unreliable") else "infer",
                    "motivation_confidence": "calc" if not m.get("motivation_ambiguous") else "infer",
                    "xg_home_sample": m.get("xg_home_sample",0),
                    "xg_away_sample": m.get("xg_away_sample",0),
                    "xg_last3_home_sample": m.get("xg_last3_home_sample",0),
                    "xg_last3_away_sample": m.get("xg_last3_away_sample",0),
                    "xg_home_source_events": m.get("xg_home_source_events",""),
                    "xg_away_source_events": m.get("xg_away_source_events",""),
                    "h2h_missing": m.get("h2h_missing",False),
                    "xg_last3_missing": m.get("xg_last3_missing",False),
                    "xg_season_missing": m.get("xg_season_missing",False),
                    "roster_missing": m.get("roster_missing",False),
                    "injury_home_missing": m.get("injury_home_missing",False),
                    "injury_away_missing": m.get("injury_away_missing",False),
                    "injury_source_unreliable": m.get("injury_source_unreliable",False),
                    "no_coach_statement": m.get("no_coach_statement",False),
                    "motivation_ambiguous": m.get("motivation_ambiguous",False),
                    "multi_team_linkage": m.get("multi_team_linkage",False),
                    "away_xg_missing": m.get("away_xg_missing",False),
                    "home_goals": m.get("home_goals", m.get("home_xg")),
                    "home_goals_conceded": m.get("home_goals_conceded", m.get("home_xga")),
                    "away_goals": m.get("away_goals", m.get("away_xg")),
                    "away_goals_conceded": m.get("away_goals_conceded", m.get("away_xga")),
                    "home_league": m.get("home_league",""), "away_league": m.get("away_league",""),
                })
            
            with open(os.path.join(tmp,"match_info.json"),"w",encoding="utf-8") as f:
                json.dump({"matches": info}, f, ensure_ascii=False, indent=2)
            
            ai = {"matches": [{"id": m["id"], "s7_score":0,"s7_reason":"",
                "opponent_predictability":1.0,"opponent_reason":"",
                "trap_analysis":"","key_risk":""} for m in info]}
            with open(os.path.join(tmp,"ai_judgment.json"),"w",encoding="utf-8") as f:
                json.dump(ai, f, ensure_ascii=False, indent=2)
            
            env = os.environ.copy()
            env["BACKTEST_TMPDIR"] = tmp
            r = subprocess.run([sys.executable, os.path.join(BASE_DIR,"run_all.py")],
                cwd=BASE_DIR, env=env, capture_output=True, text=True, timeout=120)
            if r.returncode != 0:
                print("  Error: " + str(r.stderr[:200]))
                continue
            
            mc = json.load(open(os.path.join(tmp,"monte_carlo_result.json"),encoding="utf-8"))
            ddi = json.load(open(os.path.join(tmp,"ddi_result.json"),encoding="utf-8"))
            fit = json.load(open(os.path.join(tmp,"fit_score_result.json"),encoding="utf-8"))
            rating = json.load(open(os.path.join(tmp,"rating_result.json"),encoding="utf-8"))
            
            ds = locked["matches"][0].get("time","")[:10] if locked.get("matches") else ""
            run_id = insert_run(ds, run_type="backtest")
            
            mc_map = {x["id"]:x for x in mc["matches"]}
            dd_map = {x["id"]:x for x in ddi["matches"]}
            fi_map = {x["id"]:x for x in fit["matches"]}
            ra_map = {x["id"]:x for x in rating["matches"]}
            lk_map = {x["id"]:x for x in locked["matches"]}
            valid = set(mc_map.keys()) & set(dd_map.keys()) & set(fi_map.keys()) & set(ra_map.keys())
            
            for mid in sorted(valid):
                lk = lk_map[mid]; mc_d = mc_map[mid]; dd_d = dd_map[mid]
                fi_d = fi_map[mid]["fit_score"]; ra_d = ra_map[mid]; ai_d = ai["matches"][0]
                m = {
                    "match_id": mid, "home": lk["home"], "away": lk["away"],
                    "event": lk.get("event",""), "match_time": lk.get("time",""),
                    "match_type": lk.get("match_type",""), "league": lk.get("home_league",""),
                    "asian_handicap": lk.get("asian_handicap"), "jc_handicap": lk.get("jc_handicap"),
                    "handicap_change": lk.get("handicap_change"),
                    "lambda_h_final": mc_d.get("lambda_h_final"), "lambda_a_final": mc_d.get("lambda_a_final"),
                    "lambda_diff": mc_d.get("lambda_diff"),
                    "physical_home_win": mc_d["physical"]["home_win"],
                    "physical_draw": mc_d["physical"]["draw"],
                    "physical_away_win": mc_d["physical"]["away_win"],
                    "market_home_win": dd_d.get("market",{}).get("home_win"),
                    "market_draw": dd_d.get("market",{}).get("draw"),
                    "market_away_win": dd_d.get("market",{}).get("away_win"),
                    "ddi_home_win": dd_d["ddi"]["home_win"],
                    "ddi_draw": dd_d["ddi"]["draw"],
                    "ddi_away_win": dd_d["ddi"]["away_win"],
                    "protection_triggered": dd_d.get("protection_triggered",False),
                    "sp_missing": dd_d.get("sp_missing",True),
                    "fit_score": fi_d["final_total"], "rating": ra_d["rating"],
                    "direction": ra_d["direction"],
                    "direction_warning": ra_d.get("direction_warning",False),
                    "downgrade_count": ra_d.get("downgrade_count",0),
                    "meltdown": ra_d.get("meltdown",False),
                    "scenario_type": ra_d.get("scenario_type",""),
                    "top2_total_goals": mc_d.get("top2_total_goals",[]),
                    "top2_half_full": mc_d.get("top2_half_full",[]),
                    "top3_scores": mc_d.get("top3_scores",[]),
                    "s7_score": ai_d.get("s7_score"), "s7_reason": ai_d.get("s7_reason",""),
                    "trap_analysis": ai_d.get("trap_analysis",""), "key_risk": ai_d.get("key_risk",""),
                }
                insert_match(run_id, m)
            
            print("  Run " + str(run_id) + ": " + str(len(valid)) + " matches")
            
            from database import get_db
            db = get_db()
            hits, total_check = 0, 0
            for mid in sorted(valid):
                lk = lk_map[mid]
                live = db.execute("SELECT actual_score FROM matches WHERE match_id=? AND home=? AND away=? AND actual_score IS NOT NULL LIMIT 1",
                    (mid, lk["home"], lk["away"])).fetchone()
                if not live or not live["actual_score"]: continue
                total_check += 1
                try: hg, ag = map(int, live["actual_score"].split("-"))
                except: continue
                ra_d = ra_map[mid]
                pred = ra_d["direction"]
                hit = False
                if pred == "胜": hit = hg > ag
                elif pred == "负": hit = hg < ag
                elif pred == "平": hit = hg == ag
                elif pred == "让胜": hit = (hg - ag + int(float(lk["jc_handicap"] or 0))) > 0
                if hit: hits += 1
                print("    [" + mid + "] " + lk["home"] + " vs " + lk["away"] + "  pred=" + pred + "  actual=" + live["actual_score"] + ("  HIT" if hit else "  MISS"))
            if total_check:
                print("  Result: " + str(hits) + "/" + str(total_check) + " hit (" + str(int(hits/total_check*100)) + "%)")
            db.close()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
