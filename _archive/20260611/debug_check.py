import json, sys
sys.path.insert(0, r'C:\Users\gjj\Desktop\v333')
from fit_score import score_data_confidence, score_injury_reliability, score_motivation_clarity
from lambda_calc import _confidence_scale, detect_cross_tournament_xg

d = json.load(open(r'C:\Users\gjj\Desktop\v333\data\match_info.json', encoding='utf-8'))
m = d['matches'][0]

print('=== P0-P4 置信度分析 ===')
for k in ['h2h_confidence','xg_last3_confidence','xg_season_confidence','roster_confidence',
          'injury_home_confidence','injury_away_confidence','injury_source_confidence','motivation_confidence']:
    print(f'  {k}: {m.get(k)}')

print()
for k in ['xg_home_sample','xg_away_sample','xg_last3_home_sample','xg_last3_away_sample']:
    print(f'  {k}: {m.get(k, 0)}')

print()
cp, reason = detect_cross_tournament_xg(m.get('xg_home_source_events',''), m.get('xg_away_source_events',''))
print(f'  跨赛事检测: mult={cp} reason="{reason}"')
sp = _confidence_scale(m.get('xg_home_sample',0), m.get('xg_away_sample',0), m.get('xg_last3_home_sample',0), m.get('xg_last3_away_sample',0))
print(f'  样本量系数: {sp}')

print()
s1 = score_data_confidence(m)
s2 = score_injury_reliability(m)
s3 = score_motivation_clarity(m)
print(f'  score_data_confidence (P0+P1+P2): {s1:.3f}')
print(f'  score_injury_reliability:          {s2:.1f}')
print(f'  score_motivation_clarity:          {s3:.1f}')

print()
print('--- 对比：旧二进制检查 ---')
old_score = 1.5
if m.get('h2h_missing',False): old_score -= 0.15
if m.get('xg_last3_missing',False): old_score -= 0.4
if m.get('xg_season_missing',False): old_score -= 0.25
print(f'  旧 score: {old_score}')
print(f'  新 score: {s1:.3f}')
print(f'  差值: {s1 - old_score:+.3f}')
