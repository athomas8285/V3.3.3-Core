"""
live_odds.py - 竞彩网赔率实时更新模块
赛前30分钟自动获取最新SP/让球赔率，更新 match_info.json
"""
import json, os, threading, time, logging
from datetime import datetime, timedelta, timezone
import requests

logging.basicConfig(level=logging.INFO, format="[live_odds] %(message)s")
log = logging.getLogger("live_odds")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MATCH_INFO = os.path.join(DATA_DIR, "match_info.json")
CACHE_FILE = os.path.join(DATA_DIR, "odds_cache.json")

JCZQ_URL = (
    "https://webapi.sporttery.cn/gateway/uniform/football/"
    "getMatchCalculatorV1.qry?channel=c&poolCode=hhad,had,ttg,crs,hafu"
)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.sporttery.cn/",
}

BJT = timezone(timedelta(hours=8))  # 北京时间

_updated_ids = set()
_updated_lock = threading.Lock()
_scheduler_active = False


def fetch_odds():
    """从竞彩网API获取最新赔率，返回 {match_id: {sp_home,sp_draw,sp_away,jc_handicap,jc_hhad_win,jc_hhad_draw,jc_hhad_lose}}"""
    try:
        resp = requests.get(JCZQ_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        log.warning("请求竞彩网失败: %s", e)
        return None

    result = {}
    match_days = data.get("value", {}).get("matchInfoList", [])
    for day in match_days:
        for m in day.get("subMatchList", []):
            mid = m.get("matchNumStr", "").strip()
            if not mid:
                continue

            had = m.get("had", {})
            hhad = m.get("hhad", {})
            gl = m.get("goalLine", 0)

            odds = {}
            for key, src in [("sp_home", had), ("sp_draw", had), ("sp_away", had),
                              ("jc_hhad_win", hhad), ("jc_hhad_draw", hhad), ("jc_hhad_lose", hhad)]:
                raw = src.get({"sp_home": "h", "sp_draw": "d", "sp_away": "a",
                               "jc_hhad_win": "h", "jc_hhad_draw": "d", "jc_hhad_lose": "a"}[key])
                try:
                    odds[key] = float(raw) if raw is not None else None
                except (TypeError, ValueError):
                    odds[key] = None
            odds["jc_handicap"] = int(gl) if gl is not None else 0
            result[mid] = odds
    log.info("竞彩网返回 %d 场比赛数据", len(result))
    return result


def update_match_info(odds_map):
    """用竞彩网数据更新 match_info.json，记录有变动的比赛ID"""
    if not odds_map:
        return

    try:
        with open(MATCH_INFO, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        log.warning("读取 match_info.json 失败: %s", e)
        return

    updated = []
    for m in data.get("matches", []):
        mid = m.get("id", "")
        odds = odds_map.get(mid)
        if not odds:
            continue

        changed = False
        for key in ["sp_home", "sp_draw", "sp_away", "jc_handicap",
                     "jc_hhad_win", "jc_hhad_draw", "jc_hhad_lose"]:
            if odds.get(key) is not None:
                old = m.get(key)
                if old != odds[key]:
                    m[key] = odds[key]
                    changed = True

        if changed:
            updated.append(mid)

    if updated:
        with open(MATCH_INFO, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        with _updated_lock:
            _updated_ids.update(updated)
        log.info("已更新 %d 场比赛赔率: %s", len(updated), updated)
    else:
        log.info("赔率无变化")


def get_updated_ids():
    """返回最近更新的比赛ID列表并清空"""
    with _updated_lock:
        ids = list(_updated_ids)
        _updated_ids.clear()
    return ids


def _schedule_loop():
    """后台循环：检查最近30分钟内的比赛，执行一次更新"""
    global _scheduler_active
    _scheduler_active = True

    try:
        with open(MATCH_INFO, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        _scheduler_active = False
        return

    now = datetime.now(BJT)
    matches = data.get("matches", [])

    for m in matches:
        time_str = m.get("time", "")
        if not time_str or len(time_str) < 16:
            continue
        try:
            kickoff = datetime.strptime(time_str, "%Y-%m-%d %H:%M").replace(tzinfo=BJT)
        except ValueError:
            continue

        # 赛前30分钟 ~ 开赛期间
        delta = (kickoff - now).total_seconds()
        if 0 <= delta <= 3600:  # 开赛后1小时内也更新
            log.info("比赛 %s %s 即将开始(%.0f分钟)，开始更新赔率",
                     m.get("id",""), m.get("home",""), delta/60)
            odds = fetch_odds()
            if odds:
                update_match_info(odds)
            break  # 一次只处理一场（避免请求过于频繁）

    # 下次检查：30秒后
    if _scheduler_active:
        threading.Timer(30, _schedule_loop).start()


def start():
    """启动后台更新线程"""
    log.info("启动赔率实时更新（赛前30分钟自动获取）")
    _schedule_loop()


def stop():
    global _scheduler_active
    _scheduler_active = False
    log.info("赔率更新已停止")
