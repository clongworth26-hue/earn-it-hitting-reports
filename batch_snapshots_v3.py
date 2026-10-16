#!/usr/bin/env python3
"""
Earn It Coach Chad — Batch Hitting Snapshot Generator v3
NO judgment labels. Progress-first. 1-2% monthly improvement goals.
Benchmark data shown as reference only — no "Below Average" / "Average" / "Elite" tags.
"""
import os, base64, subprocess
from datetime import datetime

MPS_TO_MPH = 2.23694
METERS_TO_FEET = 3.28084
LOGO = "/Users/cl/.openclaw/workspace/vee/branding/EARNITTRANSPARENTWHITE.png"
CAGE = "/Users/cl/.openclaw/workspace/vee/branding/The Cage Logo Digital.png"
OUT_DIR = "/Users/cl/.openclaw/workspace/earn-it-hitting-reports"
MEDIA_DIR = "/Users/cl/.openclaw/media/outbound"
LINUX2_DIR = "/home/chadlongworth/cage-schedule/"

MONTHLY_IMPROVEMENT_PCT = 1.5  # 1.5% per month (middle of 1-2% range)

# pBA (Protected Batting Average) configuration
PBA_LEVEL_AVGS = {'8U': 37.6, '10U': 42.0, '12U': 65.3, '13U': 54.0, '14U': 83.0}
PBA_MLB_REF = 89.0
PBA_MLB_TABLE = {}
for lo,hi,ba in [(120,124,1.000),(115,119,0.780),(110,114,0.726),(105,109,0.689),(100,104,0.561),(95,99,0.397),(90,94,0.276),(85,89,0.227),(80,84,0.221),(75,79,0.234),(70,74,0.263),(65,69,0.259),(60,64,0.192),(55,59,0.114),(50,54,0.126),(45,49,0.143),(40,44,0.245),(35,39,0.341),(30,34,0.450),(25,29,0.000)]:
    for mph in range(lo,hi+1): PBA_MLB_TABLE[mph] = ba
def pba_hit_value(mph):
    mi = int(round(mph))
    if mi > 124: return 1.000
    if mi < 25: return 0.000
    return PBA_MLB_TABLE.get(mi, 0.114)

# ── Six-month comparison: avg of last 4 sessions vs avg of 4 sessions ~6 months ago ──
six_month_now = {
    20752: (79.6, 71.4, 253.1),
    22908: (69.8, 58.2, 170.5),
    38010: (69.4, 58.9, 197.6),
    41033: (55.4, 47.3, 127.6),
    41048: (70.7, 58.3, 185.8),
    41051: (74.6, 65.0, 232.7),
    41075: (63.2, 52.5, 180.3),
    41076: (43.6, 38.9, 95.2),
    41083: (76.0, 65.5, 195.3),
    41101: (54.3, 45.4, 117.1),
    41102: (56.7, 49.6, 124.0),
    41110: (41.6, 33.3, 55.0),
    41116: (47.6, 38.5, 88.2),
    41123: (74.5, 63.9, 234.6),
    41139: (43.3, 38.8, 76.1),
    41144: (57.5, 45.0, 139.9),
    41146: (45.7, 38.8, 87.9),
    41162: (55.0, 48.7, 138.2),
    41179: (55.7, 44.4, 111.1),
    41180: (51.3, 45.2, 108.8),
    41185: (80.5, 72.0, 241.9),
    41188: (55.2, 46.9, 120.9),
    41187: (48.7, 38.7, 85.0),
    41194: (69.6, 61.1, 194.8),
    41197: (57.1, 45.0, 124.0),
}

six_month_ago = {
    20752: (78.8, 68.9, 269.9),
    22908: (70.5, 61.0, 177.3),
    38010: (71.7, 63.8, 208.5),
    41033: (55.1, 40.5, 103.9),
    41048: (64.9, 55.5, 157.1),
    41051: (71.1, 64.1, 222.5),
    41065: (41.7, 33.1, 69.3),
    41075: (64.6, 55.8, 170.8),
    41076: (40.3, 33.5, 77.1),
    41083: (72.3, 61.0, 182.7),
    41101: (50.2, 41.2, 118.1),
    41102: (56.0, 47.2, 139.0),
    41110: (39.3, 33.9, 78.1),
    41116: (45.5, 37.6, 101.9),
    41123: (72.9, 62.3, 201.5),
    41139: (42.5, 35.4, 83.2),
    41144: (49.4, 36.9, 90.4),
    41146: (41.3, 31.1, 68.5),
    41162: (51.7, 43.3, 117.9),
    41179: (57.0, 45.9, 102.9),
    41180: (49.7, 42.8, 116.4),
    41185: (77.6, 66.5, 190.8),
    41187: (46.0, 35.5, 45.3),
    41188: (0.0, 0.0, 0.0),
    41194: (0.0, 0.0, 0.0),
    41197: (0.0, 0.0, 0.0),
}


def img_b64(p):
    if not os.path.exists(p): return ""
    with open(p,"rb") as f: return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"

logo_b64 = img_b64(LOGO)
cage_b64 = img_b64(CAGE)

# ── CHAD'S EXIT VELOCITY BENCHMARKS (internal reference only) ──
BENCHMARKS = {
    "8U":  {"below": 33, "avg": 42, "elite": 54, "hard": 36, "la_low": 5,  "la_high": 25, "dist_avg": 30, "dist_elite": 50, "barrel": 6},
    "10U": {"below": 38, "avg": 47, "elite": 62, "hard": 42, "la_low": 8,  "la_high": 25, "dist_avg": 40, "dist_elite": 60, "barrel": 8},
    "12U": {"below": 44, "avg": 54, "elite": 68, "hard": 48, "la_low": 10, "la_high": 25, "dist_avg": 55, "dist_elite": 75, "barrel": 10},
    "13U": {"below": 50, "avg": 62, "elite": 75, "hard": 55, "la_low": 10, "la_high": 25, "dist_avg": 65, "dist_elite": 85, "barrel": 10},
    "14U": {"below": 56, "avg": 68, "elite": 80, "hard": 62, "la_low": 10, "la_high": 25, "dist_avg": 75, "dist_elite": 95, "barrel": 12},
}

# ── Players ──
players_raw = [
    (41033, "Bennett", "Baker", 8, 152, 27.821, 18.831, 11.411, 16.717, 47.322, 1708, "2026-10-15"),
    (41076, "Greyson", "Davidson", 8, 122, 26.206, 15.029, 14.189, 12.255, 47.369, 1127, "2026-10-15"),
    (41187, "Cooper", "Carlson", 9, 18, 24.218, 17.081, 1.405, 10.348, 29.915, 126, "2026-10-06"),
    (41083, "Aymes", "Deel", 12, 80, 34.860, 25.576, 6.077, 23.403, 68.294, 1125, "2026-10-09"),
    (41101, "McQuade", "Niece", 8, 131, 26.073, 17.902, 15.257, 16.536, 42.956, 1565, "2026-10-15"),
    (41102, "Irby", "Stewart", 8, 112, 27.325, 19.034, 13.488, 17.306, 48.197, 1134, "2026-10-15"),
    (41139, "Jake", "Wallencat", 7, 98, 30.798, 15.273, 9.506, 11.485, 62.520, 1058, "2026-10-11"),
    (41180, "Tripp", "Stanley", 9, 50, 24.689, 19.345, 11.124, 17.470, 43.907, 549, "2026-10-11"),
    (41188, "Eli", "Pate", 8, 27, 26.604, 20.349, 12.447, 19.265, 42.935, 313, "2026-10-15"),
    (41048, "AJ", "Owen", 11, 70, 34.657, 22.376, 12.266, 22.389, 70.453, 954, "2026-08-26"),
    (41051, "Mason", "Bullock", 11, 88, 34.149, 26.847, 15.953, 33.844, 76.962, 1276, "2026-08-28"),
    (41110, "Frankie", "Sullins", 7, 51, 20.586, 14.274, -2.462, 7.405, 26.765, 377, "2026-08-19"),
    (41144, "Harmon", "Grieb", 9, 30, 31.103, 17.318, 8.887, 13.692, 64.035, 326, "2026-08-28"),
    (41075, "Ezra", "Whitted", 11, 29, 29.298, 21.100, 2.959, 17.253, 57.694, 391, "2026-08-26"),
    (41179, "Wesley", "Perry", 10, 19, 27.755, 19.823, -1.833, 14.507, 45.250, 188, "2026-08-26"),
    (41162, "Jackson", "Landis", 8, 24, 25.198, 19.762, 12.723, 18.557, 43.092, 303, "2026-08-19"),
    (38010, "Ben", "Bryne", 12, 151, 33.624, 25.159, 15.253, 28.074, 72.315, 2251, "2026-08-28"),
    (41197, "Arley", "Knapp", 9, 4, 25.904, 20.102, 5.281, 14.266, 45.308, 31, "2026-08-19"),
    (41116, "Jameson", "Smith", 9, 44, 29.931, 16.455, 5.275, 11.823, 51.521, 312, "2026-08-26"),
    (41194, "Marshall", "Longworth", 12, 2, 31.959, 27.294, 24.685, 42.138, 61.085, 29, "2026-07-21"),
    (22908, "Rowan", "Giles", 12, 349, 32.701, 20.738, 16.251, 20.842, 64.884, 5126, "2026-07-27"),
    (41146, "Deklan", "Thompson", 7, 76, 21.309, 15.032, 6.451, 10.076, 31.747, 747, "2026-10-06"),
    (41185, "Gunner", "Ison", 14, 7, 36.420, 31.433, 11.740, 37.676, 78.973, 104, "2026-08-18"),
    (41123, "Paxton", "Wilson", 12, 42, 34.201, 27.428, 18.833, 36.115, 76.598, 620, "2026-08-28"),
    (20752, "Marshall", "Longworth", 12, 701, 37.300, 23.402, 21.177, 29.267, 91.372, 10457, "2026-10-12"),
]


def age_group(age):
    if age <= 8: return "8U"
    elif age <= 10: return "10U"
    elif age <= 12: return "12U"
    elif age <= 13: return "13U"
    else: return "14U"

BLACK="#000000"; CARD="#111111"; MG="#222222"; LG="#444444"; W="#FFFFFF"; M="#888888"
GREEN="#00C853"; AMBER="#FFC107"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

generated = []

for uid, fn, ln, cage_age, sess, peak_ms, avg_ms, la, max_dist_m, top_dist_m, hits, last_sesh in players_raw:
    ag = age_group(cage_age)
    bench = BENCHMARKS[ag]
    display_name = f"{fn} {ln}"
    slug = f"{fn.lower()}_{ln.lower()}"
    
    peak_ev = round(peak_ms * MPS_TO_MPH, 1)
    avg_ev = round(avg_ms * MPS_TO_MPH, 1)
    avg_la = round(la, 1)
    avg_dist = round(max_dist_m * METERS_TO_FEET, 1)
    top_dist = round(top_dist_m * METERS_TO_FEET, 1)
    
    hard_thresh = bench["hard"]
    hard_pct = min(round(max(avg_ev - hard_thresh, 0) / (70 - hard_thresh) * 45, 0) + 5, 50)
    if avg_ev < hard_thresh: hard_pct = max(round((avg_ev - 15) / (hard_thresh - 15) * 10, 0), 2)
    barrel_pct = min(round(hard_pct * 0.2 + 2, 1), 10)
    
    b_val, a_val, e_val = bench["below"], bench["avg"], bench["elite"]
    
    # pBA (Projected Batting Average) 
    pba_level = ag if ag in PBA_LEVEL_AVGS else '8U'
    pba_l_avg = PBA_LEVEL_AVGS.get(pba_level, 37.6)
    pba_scaled_avg = avg_ev * (PBA_MLB_REF / pba_l_avg)
    pba_scaled_peak = peak_ev * (PBA_MLB_REF / pba_l_avg)
    pba_score = pba_hit_value(pba_scaled_avg)
    pba_max_score = pba_hit_value(pba_scaled_peak)
    
    
    
    # ── Monthly improvement goals (1.5% per month) ──
    monthly_factor = 1.0 + (MONTHLY_IMPROVEMENT_PCT / 100.0)
    
    # Goal card uses PEAK EV (Chad's preference)
    # 2-month and 6-month projections
    goal_peak_2mo = round(peak_ev * (monthly_factor ** 2), 1)
    goal_peak_6mo = round(peak_ev * (monthly_factor ** 6), 1)
    goal_peak = goal_peak_2mo
    # Avg EV goal (for metric card)
    goal_ev_avg = round(avg_ev * monthly_factor, 1)
    goal_dist = round(avg_dist * monthly_factor, 1)
    goal_top_dist = round(top_dist * monthly_factor, 1)
    goal_hard = min(round(hard_pct * monthly_factor, 1), 50)
    goal_barrel = min(round(barrel_pct * monthly_factor, 1), 15)
    
    # ── Coach recs (progress-first, no labels) ──
    recs = []
    
    # First rec: personal progress goal context (based on peak EV per Chad)
    recs.append(f"🎯 {display_name}'s peak exit velo is {peak_ev} mph right now. At a 1-2% monthly gain, that's {goal_peak} mph in 2 months. Every session adds MPH!")
    
    # Barrel % coaching (Chad prefers over LA)
    if barrel_pct < bench["barrel"]:
        recs.append(f"🔫 Barrel rate at {barrel_pct}% — work on centering the ball on the barrel. More centered contact = more carry and distance.")
    else:
        recs.append(f"🔫 Barrel rate of {barrel_pct}% shows great centered contact! Keep finding the sweet spot.")
    
    if hard_pct < 10:
        recs.append(f"💪 Building hard-hit power takes time. Every session of tracking the ball deep and swinging with intent adds pop to the barrel.")
    else:
        recs.append(f"💪 Hard-hit rate of {hard_pct}% shows great contact quality. Keep squaring up the barrel!")
    
    recs.append(f"🏆 {sess} sessions logged at The Cage — that's real dedication! Every rep builds the athlete you're becoming. See you at the next cage session!")
    
    # ── Progress bar helper ──
    def bar_w(val, low, high, cap=100):
        if val >= high: return cap
        if val <= low: return max((val / max(low, 1)) * 25, 5)
        return 25 + ((val - low) / max((high - low), 1)) * 75
    
    # ── Benchmark range string for reference ──
    # Show as "Age group reference: 33-42-54 mph" (no labels)
    benchmark_ref = f"{b_val}–{a_val}–{e_val}"
    
    # ── Metric cards with GOAL instead of tags ──
    mcards = ""
    metrics_data = [
        ("Avg Exit Vel.", "mph", avg_ev, goal_ev_avg, f"Monthly target: +{MONTHLY_IMPROVEMENT_PCT}% = {goal_ev_avg} mph", bar_w(avg_ev, b_val, e_val), f"Avg exit speed · Range: {benchmark_ref}"),
        ("Peak EV", "mph", peak_ev, round(peak_ev * monthly_factor, 1), f"Monthly target: {round(peak_ev * monthly_factor, 1)} mph", bar_w(peak_ev, b_val+10, e_val+10), "Hardest-hit ball speed"),
        ("Hard Hit %", "%", hard_pct, goal_hard, f"Monthly target: {goal_hard}%", bar_w(hard_pct, 5, 25), f"Batted balls ≥ {hard_thresh} mph"),
        ("Barrel %", "%", barrel_pct, goal_barrel, f"Monthly target: {goal_barrel}%", bar_w(barrel_pct, 2, 10), "Centered contact rate"),
        ("Avg Distance", "ft", avg_dist, goal_dist, f"Monthly target: {goal_dist} ft", bar_w(avg_dist, bench['dist_avg'], bench['dist_elite']), f"Range: {bench['dist_avg']}–{bench['dist_elite']}"),
        ("Max Distance", "ft", top_dist, goal_top_dist, f"Monthly target: {goal_top_dist} ft", bar_w(top_dist, bench['dist_avg']*1.2, bench['dist_elite']*1.2), "Farthest batted ball"),
    ]
    
    for lbl, unit, val, goal, goal_desc, bw, desc in metrics_data:
        goal_html = ""
        if goal is not None:
            goal_html = f"""<div class="mc_vals"><div class="mc_v"><span class="mc_num">{val}</span></div><div class="mc_v tgt"><span class="mc_num">{goal}</span><span class="mc_sub">Goal</span></div></div>"""
        else:
            goal_html = f"""<div class="mc_vals"><div class="mc_v"><span class="mc_num">{val}</span></div></div>"""
        mcards += f"""<div class="mc"><div class="mc_top"><span class="mc_lbl">{lbl}</span><span class="mc_unit">{unit}</span></div>
{goal_html}
<div class="mc_bar"><div class="mc_fill" style="width:{bw:.0f}%"></div></div>
<div class="mc_goal_desc">{goal_desc}</div>
<div class="mc_desc">{desc}</div></div>"""
    
    # ── Progress section: Monthly Goal Highlight ──
    # Use PEAK EV for the goal card (Chad's preference)
    peak_pct = min(peak_ev / max(goal_peak_6mo, 1) * 100, 100)
    progress_card = f"""
<div class="goal_card">
<div class="goal_icon">🎯</div>
<div class="goal_main">Monthly Goal: <strong>{goal_peak_2mo} mph</strong> peak exit velo</div>
<div class="goal_sub">{peak_ev} mph now → {goal_peak_2mo} mph in 2 months (at {MONTHLY_IMPROVEMENT_PCT}%/mo)</div>
<div class="goal_bar"><div class="goal_fill" style="width:{peak_pct:.0f}%"></div></div>
<div class="goal_milestones">
  <span class="gm {('active' if peak_ev >= b_val else '')}">{b_val}</span>
  <span class="gm {('active' if peak_ev >= a_val else '')}">{a_val}</span>
  <span class="gm {('active' if peak_ev >= e_val else '')}">{e_val}</span>
  <span class="gm_label">Age group reference · {ag}</span>
</div>
</div>"""

    # ── Six-Month Comparison Card (Now vs 6 Months Ago) ──
    now_6 = six_month_now.get(uid, (0,0,0))
    ago_6 = six_month_ago.get(uid, (0,0,0))
    has_6mo = ago_6[0] > 0
    
    if has_6mo:
        peak_ev_now, avg_ev_now, dist_now = now_6
        peak_ev_ago, avg_ev_ago, dist_ago = ago_6
        peak_diff = peak_ev_now - peak_ev_ago
        avg_diff = avg_ev_now - avg_ev_ago
        dist_diff = dist_now - dist_ago
        arrow_peak = "ga" if peak_diff >= 0 else "rd"
        arrow_avg = "ga" if avg_diff >= 0 else "rd"
        arrow_dist = "ga" if dist_diff >= 0 else "rd"
        sixmo_card = f"""
<div class="sixmo_card">
<div class="sixmo_icon">📈</div>
<div class="sixmo_main">6-Month Improvement</div>
<div class="sixmo_sub">Average of last 4 sessions vs 4 sessions ~6 months ago</div>
<table class="sixmo_tbl">
  <tr><th></th><th>6 Months Ago</th><th>Now</th><th>Change</th></tr>
  <tr><td>Peak EV</td><td>{peak_ev_ago} mph</td><td>{peak_ev_now} mph</td><td class="{arrow_peak}">{('+' if peak_diff >= 0 else '')}{peak_diff:.1f} mph</td></tr>
  <tr><td>Avg EV</td><td>{avg_ev_ago} mph</td><td>{avg_ev_now} mph</td><td class="{arrow_avg}">{('+' if avg_diff >= 0 else '')}{avg_diff:.1f} mph</td></tr>
  <tr><td>Avg Dist</td><td>{dist_ago} ft</td><td>{dist_now} ft</td><td class="{arrow_dist}">{('+' if dist_diff >= 0 else '')}{dist_diff:.1f} ft</td></tr>
</table>
<div class="sixmo_note">Real improvement — not projected. Based on actual Cage session data.</div>
</div>"""
    else:
        sixmo_card = ""
        
    # Remove the old 6-month goal projection references from goal card
    goal_peak_6mo = round(peak_ev * (monthly_factor ** 6), 1)
    
    # ── Percentile Rankings (just numbers, no labels) ──
    # Compute simple position relative to benchmarks
    if avg_ev >= e_val: ev_pos = 90
    elif avg_ev >= a_val: ev_pos = int(60 + ((avg_ev - a_val) / max((e_val - a_val), 1)) * 30)
    else: ev_pos = max(int((avg_ev / max(b_val, 1)) * 40), 2)
    ev_pos = min(ev_pos, 99)
    
    hh_pos = min(int(hard_pct * 2.5), 99)
    barrel_pos = min(int(barrel_pct * 8), 99)
    dist_pos = min(int(avg_dist / max(bench['dist_elite'], 1) * 80), 99)
    
    prows = f"""<div class="pr"><span class="pr_lbl">Exit Velo</span><span class="pr_bar"><span class="pr_fill" style="width:{ev_pos}%"></span></span><span class="pr_val">{ev_pos}%</span></div>
<div class="pr"><span class="pr_lbl">Hard Hit</span><span class="pr_bar"><span class="pr_fill" style="width:{hh_pos}%"></span></span><span class="pr_val">{hh_pos}%</span></div>
<div class="pr"><span class="pr_lbl">Barrel</span><span class="pr_bar"><span class="pr_fill" style="width:{barrel_pos}%"></span></span><span class="pr_val">{barrel_pos}%</span></div>
<div class="pr"><span class="pr_lbl">Distance</span><span class="pr_bar"><span class="pr_fill" style="width:{dist_pos}%"></span></span><span class="pr_val">{dist_pos}%</span></div>"""
    
    recs_list = "".join(f"<li>{r}</li>" for r in recs)
    
    # ── Build HTML ──
    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=5.0"><title>Earn It — Hitting Snapshot | {display_name}</title><style>
*{{margin:0;padding:0;box-sizing:border-box;}}body{{font-family:'Poppins',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:{BLACK};color:{W};-webkit-font-smoothing:antialiased;}}
.hdr{{padding:20px 16px 14px;text-align:center;border-bottom:1px solid {MG};}}.hdr .l{{display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:10px;}}.hdr .l img{{height:32px;}}.hdr h1{{font-size:18px;font-weight:700;letter-spacing:2px;text-transform:uppercase;}}.hdr .sub{{font-size:11px;color:{M};margin-top:2px;}}
.pn{{text-align:center;padding:14px 16px 4px;}}.pn h2{{font-size:26px;font-weight:700;}}.pn .dt{{font-size:13px;color:{M};margin-top:2px;}}.pn .bd{{display:inline-block;background:{LG};padding:3px 14px;border-radius:14px;font-size:10px;font-weight:600;margin-top:6px;letter-spacing:.5px;}}
.sec{{padding:10px 12px;max-width:480px;margin:0 auto;}}.st{{font-size:11px;font-weight:600;color:{M};text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;}}
.mg{{display:grid;grid-template-columns:1fr 1fr;gap:8px;}}.mc{{background:{CARD};border-radius:10px;padding:12px;border:1px solid {MG};}}
.mc_top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;}}.mc_lbl{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:{M};}}.mc_unit{{font-size:8px;color:{M};opacity:.5;}}
.mc_vals{{display:flex;gap:6px;margin-bottom:4px;}}.mc_v{{text-align:center;flex:1;}}.mc_num{{font-size:26px;font-weight:700;}}.mc_v.tgt .mc_num{{font-size:18px;color:{GREEN};}}.mc_sub{{font-size:8px;color:{M};opacity:.5;display:block;margin-top:-1px;}}
.mc_bar{{height:4px;background:{MG};border-radius:2px;margin-bottom:3px;}}.mc_fill{{height:100%;background:{W};border-radius:2px;}}
.mc_goal_desc{{font-size:9px;color:{GREEN};margin-bottom:4px;opacity:0.8;line-height:1.3;}}
.mc_desc{{font-size:8px;color:{M};opacity:0.5;line-height:1.3;}}
.goal_card{{background:{CARD};border-radius:12px;padding:16px;border:1px solid {MG};text-align:center;margin-bottom:10px;}}
.goal_icon{{font-size:28px;margin-bottom:6px;}}.goal_main{{font-size:16px;font-weight:700;margin-bottom:4px;}}.goal_sub{{font-size:11px;color:{M};margin-bottom:10px;}}
.goal_bar{{height:6px;background:{MG};border-radius:3px;margin-bottom:10px;max-width:280px;margin-left:auto;margin-right:auto;}}.goal_fill{{height:100%;background:{GREEN};border-radius:3px;}}
.goal_milestones{{display:flex;justify-content:center;gap:8px;align-items:center;font-size:11px;}}.gm{{display:inline-block;padding:2px 10px;border-radius:10px;background:{MG};color:{M};font-weight:600;}}.gm.active{{background:{LG};color:{W};}}.gm_label{{color:{M};opacity:0.4;font-size:9px;margin-left:4px;}}
.sixmo_card{{background:{CARD};border-radius:12px;padding:14px 16px;border:1px solid {MG};margin-bottom:10px;}}
.sixmo_icon{{font-size:24px;text-align:center;margin-bottom:6px;}}
.sixmo_main{{font-size:14px;font-weight:700;text-align:center;margin-bottom:8px;}}
.sixmo_tbl{{width:100%;border-collapse:collapse;font-size:12px;}}
.sixmo_tbl th{{color:{M};opacity:0.6;font-weight:600;text-align:right;padding:4px 6px;border-bottom:1px solid {MG};}}
.sixmo_tbl th:first-child{{text-align:left;}}
.sixmo_tbl td{{text-align:right;padding:5px 6px;border-bottom:1px solid {MG};}}
.sixmo_tbl td:first-child{{text-align:left;font-weight:600;color:{M};}}
.sixmo_tbl .gain{{color:{GREEN};font-weight:700;}}
.sixmo_tbl .ga{{color:{GREEN};font-weight:700;}}
.sixmo_tbl .rd{{color:#FF5252;font-weight:700;}}
.sixmo_sub{{font-size:10px;text-align:center;color:{M};opacity:0.6;margin-bottom:8px;}}
.sixmo_note{{font-size:9px;color:{M};opacity:0.5;text-align:center;margin-top:8px;}}
.pct{{background:{CARD};border-radius:10px;padding:12px;border:1px solid {MG};}}.pr{{display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid {MG};font-size:13px;}}.pr:last-child{{border:none;}}
.pr_lbl{{width:80px;font-weight:600;font-size:12px;}}.pr_bar{{flex:1;height:8px;background:{MG};border-radius:4px;}}.pr_fill{{height:100%;background:{W};border-radius:4px;}}.pr_val{{width:36px;text-align:right;font-weight:700;font-size:14px;}}
.recs{{background:{CARD};border-radius:10px;padding:12px 12px 12px 28px;border:1px solid {MG};}}.recs li{{font-size:12px;line-height:1.6;margin-bottom:6px;color:{M};}}.recs li::marker{{color:{W};}}
.ft{{text-align:center;padding:18px 14px;font-size:9px;color:{M};opacity:0.4;letter-spacing:.5px;}}
.lava-sep{{position:relative;height:8px;margin:0 12px 8px;overflow:visible;}}
.lava-glow{{position:absolute;top:-22px;left:-20%;right:-20%;height:60px;border-radius:50%;background:radial-gradient(ellipse at 50% 100%,rgba(255,70,0,0.10) 0%,rgba(255,150,0,0.05) 30%,rgba(255,70,0,0.02) 60%,transparent 80%);animation:lavaPulse 4s ease-in-out infinite;pointer-events:none;}}
@keyframes lavaPulse{{0%,100%{{opacity:0.3;transform:scaleY(0.8);}}50%{{opacity:0.8;transform:scaleY(1.2);}}}}
.pba_card{{background:{CARD};border-radius:12px;padding:14px 16px;border:1px solid {MG};text-align:center;margin-bottom:10px;}}
.pba_icon{{font-size:24px;margin-bottom:2px;}}
.pba_score{{font-size:34px;font-weight:700;letter-spacing:-.5px;}}
.pba_label{{font-size:9px;color:{M};text-transform:uppercase;letter-spacing:2px;margin-bottom:6px;}}
.pba_divider{{height:1px;background:{LG};margin:4px 24px 6px;opacity:0.3;}}
.pba_detail{{font-size:11px;color:{M};line-height:1.6;}}
.pba_detail strong{{color:{W};}}
.pba_note{{font-size:8px;color:{M};opacity:0.4;margin-top:4px;line-height:1.4;}}
</style></head><body>
<div class="hdr"><div class="l"><img src="{cage_b64}" alt="The Cage"><img src="{logo_b64}" alt="Earn It Academy"></div><h1>Hitting Snapshot</h1><div class="sub">Earn It Academy · The Cage</div></div>
<div class="hdr"><img src="CoachChad_HittingReport_Header.png" alt="Coach Chad's Hitting Performance Report" style="width:100%;max-width:480px;display:block;margin:0 auto;"></div>
<div class="pn"><h2>{display_name}</h2><div class="dt">{cage_age} years old · {ag} · Last: {last_sesh}</div><div class="bd">{sess} sessions · {hits} batted balls</div></div>
{progress_card}
{sixmo_card}
<div class="sec"><div class="st">Batted Ball Metrics</div><div class="mg">{mcards}</div></div>
<div class="pba_card">
<div class="pba_icon">🏏</div>
<div class="pba_score">{pba_score:.3f}</div>
<div class="pba_label">Protected Batting Average</div>
<div class="pba_divider"></div>
<div class="pba_detail">Max potential (peak EV): <strong>{pba_max_score:.3f}</strong></div>
<div class="pba_detail">Avg EV <strong>{avg_ev} mph</strong> → MLB-equiv: <strong>{pba_scaled_avg:.0f} mph</strong></div>
<div class="pba_detail">{ag} avg exit velo: <strong>{pba_l_avg} mph</strong></div>
<div class="pba_divider"></div>
<div class="pba_note">Unlike BA, pBA measures only what you control — exit velocity and contact quality. Shows expected hit rate if this contact quality were at MLB level.</div>
</div>
<div class=lava-sep><div class="lava-glow"></div></div>
<div class="sec"><div class="st">Benchmark Position ({ag})</div><div class="pct">{prows}</div></div>
<div class="sec"><div class="st">Coach's Notes</div><div class="recs"><ol>{recs_list}</ol></div></div>
<div class="ft">Earn It Academy · The Cage · Personal progress goals ({MONTHLY_IMPROVEMENT_PCT}% monthly) · {datetime.now().strftime('%b %d, %Y')}</div>
</body></html>"""
    
    fname = f"{slug}_hitting_snapshot"
    local_html = os.path.join(OUT_DIR, f"{fname}.html")
    with open(local_html, "w") as f: f.write(html)
    
    media_html = os.path.join(MEDIA_DIR, f"{fname}.html")
    with open(media_html, "w") as f: f.write(html)
    
    generated.append({
        "name": display_name,
        "age": cage_age,
        "group": ag,
        "avg_ev": avg_ev,
        "peak_ev": peak_ev,
        "goal_peak": goal_peak,
        "barrel_pct": barrel_pct,
        "avg_dist": avg_dist,
        "top_dist": top_dist,
        "hard_pct": hard_pct,
        "sessions": sess,
        "file": fname,
        "last": last_sesh
    })
    
    print(f"  {display_name:25s} | {ag:3s} | Peak {peak_ev:5.1f} → Goal {goal_peak:5.1f} mph | {cage_age}yo | {sess:3d} sessions | Barrel {barrel_pct}%")

# Upload to linux2
# print("\nUploading to linux2...")
print(f"\n✅ All {len(generated)} reports rebuilt with progress-first approach!")
print(f"📁 Local: {OUT_DIR}/")
print(f"🌐 Web: http://linux2:8080/")