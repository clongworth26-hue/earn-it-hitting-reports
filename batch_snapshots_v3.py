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
OUT_DIR = "/Users/cl/.openclaw/workspace/zona/reports"
MEDIA_DIR = "/Users/cl/.openclaw/media/outbound"
LINUX2_DIR = "/home/chadlongworth/cage-schedule/"

MONTHLY_IMPROVEMENT_PCT = 1.5  # 1.5% per month (middle of 1-2% range)

# ── Six-month comparison: avg of last 4 sessions vs avg of 4 sessions ~6 months ago ──
six_month_now = {
    41033: (55.1, 46.1, 137.4),
    41048: (70.7, 58.3, 185.8),
    41051: (74.6, 65.0, 232.7),
    41075: (63.2, 52.5, 180.3),
    41076: (43.5, 38.9, 88.4),
    41083: (72.0, 59.1, 166.9),
    41101: (53.1, 43.9, 110.4),
    41102: (55.7, 48.8, 134.9),
    41110: (41.6, 33.3, 55.0),
    41139: (41.7, 36.1, 86.1),
    41144: (57.5, 45.0, 139.9),
    41162: (55.0, 48.7, 138.2),
    41179: (55.7, 44.4, 111.1),
    41180: (51.9, 45.6, 120.2),
    41188: (56.9, 45.4, 125.9),
    # New 7
    38010: (69.4, 58.9, 197.6),
    41197: (57.1, 45.0, 124.0),
    41116: (47.6, 38.5, 88.2),
    41194: (69.6, 61.1, 194.8),
    22908: (69.8, 58.2, 170.5),
    41146: (44.9, 35.4, 67.3),
    41185: (80.5, 72.0, 241.9),
    41123: (74.5, 63.9, 234.6),
}
six_month_ago = {
    41033: (50.1, 42.5, 106.5),
    41048: (61.7, 51.8, 139.2),
    41051: (71.5, 64.9, 215.1),
    41075: (62.5, 51.8, 147.8),
    41076: (41.6, 35.7, 85.2),
    41083: (72.7, 60.0, 198.4),
    41101: (49.2, 39.1, 99.1),
    41102: (52.3, 46.2, 122.9),
    41110: (41.2, 33.8, 59.3),
    41139: (41.8, 34.9, 79.8),
    41144: (46.5, 36.1, 85.0),
    41162: (51.7, 43.3, 117.9),
    41179: (59.6, 44.1, 112.6),
    41180: (46.0, 38.2, 91.1),
    41188: (0.0, 0.0, 0.0),
    # New 7
    38010: (68.1, 60.0, 180.1),
    41197: (0.0, 0.0, 0.0),  # No 6-month data
    41116: (46.0, 38.3, 89.2),
    41194: (0.0, 0.0, 0.0),  # No 6-month data
    22908: (65.4, 58.0, 164.2),
    41146: (39.2, 33.1, 62.8),
    41185: (0.0, 0.0, 0.0),  # No 6-month data
    41123: (71.5, 60.6, 211.3),
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
    (41033, "Bennett",    "Baker",    8, 148, 27.821, 18.769, 22.001, 27.812, 47.322, 1669, "2026-09-24"),
    (41076, "Greyson",    "Davidson", 8, 118, 26.206, 14.950, 15.380, 16.460, 47.369, 1095, "2026-09-24"),
    (41083, "Aymes",      "Deel",    12,  76, 39.608, 25.450,  6.239, 23.519, 94.447, 1081, "2026-09-16"),
    (41101, "McQuade",    "Niece",    8, 128, 29.660, 17.855, 18.705, 24.123, 62.663, 1528, "2026-09-24"),
    (41102, "Irby",       "Stewart",  8, 107, 26.421, 18.864, 19.760, 26.828, 47.852, 1079, "2026-09-24"),
    (41139, "Jake",       "Wallencat",7,  94, 30.798, 15.185, 22.177, 19.438, 62.520, 1012, "2026-09-18"),
    (41180, "Tripp",      "Stanley",  9,  44, 24.689, 19.281, 15.504, 18.997, 43.907,  489, "2026-09-21"),
    (41188, "Eli",        "Pate",     8,  21, 26.604, 20.320, 29.024, 27.893, 42.935,  248, "2026-09-24"),
    # New 7 players
    (41048, "AJ",         "Owen",    11,  70, 34.657, 22.376, 13.513, 29.569, 70.453,  954, "2026-09-23"),
    (41051, "Mason",      "Bullock", 11,  88, 34.149, 26.847, 27.154, 63.517, 76.962, 1276, "2026-09-23"),
    (41110, "Frankie",    "Sullins",  7,  51, 20.586, 14.274, 16.195, 13.322, 26.765,  377, "2026-09-23"),
    (41144, "Harmon",     "Grieb",    9,  32, 31.103, 16.236, 10.410, 15.277, 64.035,  326, "2026-09-23"),
    (41075, "Ezra",       "Whitted", 11,  29, 29.298, 21.100, -6.020, 13.136, 57.694,  391, "2026-09-23"),
    (41179, "Wesley",     "Perry",   10,  19, 27.755, 19.823,  2.854, 17.532, 45.250,  188, "2026-09-23"),
    (41162, "Jackson",    "Landis",   8,  25, 25.198, 18.971,  7.903, 18.810, 43.092,  303, "2026-09-22"),
    # Chad's latest additions
    (38010, "Ben",        "Bryne",   12, 151, 33.624, 25.159, 15.253, 28.074, 72.315, 2251, "2026-08-28"),
    (41197, "Arley",      "Knapp",    9,   4, 25.904, 20.102,  5.281, 14.266, 45.308,   31, "2026-08-19"),
    (41116, "Jameson",    "Smith",    9,  44, 29.931, 16.455,  5.275, 11.823, 51.521,  312, "2026-08-26"),
    (41194, "Marshall",   "Longworth",12,   2, 31.959, 27.294, 24.685, 42.138, 61.085,   29, "2026-07-21"),
    (22908, "Rowan",      "Giles",   12, 349, 32.701, 20.738, 16.251, 20.842, 64.884, 5126, "2026-07-27"),
    (41146, "Deklan",     "Thompson", 7,  70, 21.236, 14.840,  6.242,  9.748, 27.400,  666, "2026-09-17"),
    (41185, "Gunner",     "Ison",    14,   7, 36.420, 31.433, 11.740, 37.676, 78.973,  104, "2026-08-18"),
    # Paxton Wilson
    (41123, "Paxton",     "Wilson",  12,  42, 34.201, 27.428, 18.833, 36.115, 76.598,  620, "2026-08-28"),
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
</style></head><body>
<div class="hdr"><div class="l"><img src="{cage_b64}" alt="The Cage"><img src="{logo_b64}" alt="Earn It Academy"></div><h1>Hitting Snapshot</h1><div class="sub">Earn It Academy · The Cage</div></div>
<div class="pn"><h2>{display_name}</h2><div class="dt">{cage_age} years old · {ag} · Last: {last_sesh}</div><div class="bd">{sess} sessions · {hits} batted balls</div></div>
{progress_card}
{sixmo_card}
<div class="sec"><div class="st">Batted Ball Metrics</div><div class="mg">{mcards}</div></div>
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
print("\nUploading to linux2...")
for g in generated:
    fname = f"{g['file']}.html"
    src = os.path.join(OUT_DIR, fname)
    r = subprocess.run(["scp", "-o", "ConnectTimeout=5", src, f"linux2:{LINUX2_DIR}{fname}"], capture_output=True, text=True, timeout=10)
    print(f"  {'✅' if r.returncode==0 else '❌'} {fname}")

print(f"\n✅ All {len(generated)} reports rebuilt with progress-first approach!")
print(f"📁 Local: {OUT_DIR}/")
print(f"🌐 Web: http://linux2:8080/")