#!/usr/bin/env python3
"""Generate 2 charts (Velo + HH%) w/ trend lines for every player card, insert below Coach's Notes."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64, csv, io, os, sys

DATA = '/tmp/earn-it-hitting-reports/monthly_data.csv'
BASE = '/tmp/earn-it-hitting-reports'

# uid -> (slug, display name)
ROSTER = {
    20752: ('marshall_longworth', 'Marshall Longworth'),
    22908: ('rowan_giles', 'Rowan Giles'),
    38010: ('ben_bryne', 'Ben Byrne'),
    41033: ('bennett_baker', 'Bennett Baker'),
    41048: ('aj_owen', 'AJ Owen'),
    41051: ('mason_bullock', 'Mason Bullock'),
    41057: ('peyton_hiatt', 'Peyton Hiatt'),
    41067: ('joseph_hileman', 'Joseph Hileman'),
    41072: ('easton_brooks', 'Easton Brooks'),
    41075: ('ezra_whitted', 'Ezra Whitted'),
    41076: ('greyson_davidson', 'Greyson Davidson'),
    41083: ('aymes_deel', 'Aymes Deel'),
    41098: ('easton_elam', 'Easton Elam'),
    41101: ('mcquade_niece', 'McQuade Niece'),
    41102: ('irby_stewart', 'Irby Stewart'),
    41104: ('zeke_whitted', 'Zeke Whitted'),
    41105: ('asher_scott', 'Asher Scott'),
    41110: ('frankie_sullins', 'Frankie Sullins'),
    41116: ('jameson_smith', 'Jameson Smith'),
    41118: ('will_meade', 'Will Meade'),
    41123: ('paxton_wilson', 'Paxton Wilson'),
    41139: ('jake_wallencat', 'Jake Wallencat'),
    41144: ('harmon_grieb', 'Harmon Grieb'),
    41146: ('deklan_thompson', 'Deklan Thompson'),
    41147: ('axl_deel', 'Axl Deel'),
    41162: ('jackson_landis', 'Jackson Landis'),
    41167: ('bentley_thacker', 'Bentley Thacker'),
    41179: ('wesley_perry', 'Wesley Perry'),
    41180: ('tripp_stanley', 'Tripp Stanley'),
    41183: ('jude_burrow', 'Jude Burrow'),
    41185: ('gunner_ison', 'Gunner Ison'),
    41188: ('eli_pate', 'Eli Pate'),
    41190: ('eliza_stewart', 'Eliza Stewart'),
    41197: ('arley_knapp', 'Arley Knapp'),
    41198: ('sutton_campbell', 'Sutton Campbell'),
}

BG = '#000008'; PLOT_BG = '#0d0d10'; TXT = '#aaaaaa'
RED = '#ff3355'; BLU = '#3388ff'; GRN = '#00e868'

# load data
by_uid = {}
with open(DATA) as f:
    r = csv.DictReader(f)
    for row in r:
        uid = int(row['uid'])
        by_uid.setdefault(uid, []).append({
            'ym': row['ym'],
            'max': float(row['max_ev']),
            'avg': float(row['avg_ev']),
            'hh': float(row['hh_pct']),
        })

def trend_vals(yvals):
    n = len(yvals)
    xs = list(range(n))
    mx = sum(xs)/n; my = sum(yvals)/n
    num = sum((xs[i]-mx)*(yvals[i]-my) for i in range(n))
    den = sum((xs[i]-mx)**2 for i in range(n))
    slope = num/den if den else 0.0
    inter = my - slope*mx
    return [inter + slope*xs[0], inter + slope*xs[-1]]

def style_axis(ax, months):
    ax.set_facecolor(PLOT_BG)
    ax.grid(True, alpha=0.08, linestyle='-', color='#1a1a20')
    ax.set_axisbelow(True)
    ax.tick_params(axis='both', labelcolor=TXT, colors=TXT, labelsize=8)
    ax.set_xticks(range(len(months)))
    ax.set_xticklabels(months, rotation=45, ha='right', fontsize=7)

def finalize(fig, ax, legend):
    lg = legend[0]
    lg.get_frame().set_facecolor('#0a0a0c')
    lg.get_frame().set_edgecolor('#222')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, facecolor=BG)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

def make_charts(name, months, maxev, avgev, hhpct):
    # Chart 1: Max EV + Avg EV
    fig, ax1 = plt.subplots(figsize=(10, 3.8))
    fig.patch.set_facecolor(BG)
    style_axis(ax1, months)
    ax1.plot(range(len(months)), maxev, color=RED, marker='o', linewidth=2, markersize=5,
             markerfacecolor=RED, markeredgecolor='white', markeredgewidth=0.8, label='Max EV', zorder=5)
    ax1.fill_between(range(len(months)), maxev, alpha=0.05, color=RED, zorder=1)
    ax1.plot(range(len(months)), avgev, color=BLU, marker='s', linewidth=2, markersize=5,
             markerfacecolor=BLU, markeredgecolor='white', markeredgewidth=0.8, label='Avg EV', zorder=5)
    for col, vals in ((RED, maxev), (BLU, avgev)):
        tv = trend_vals(vals)
        ax1.plot([0, len(months)-1], tv, color=col, linestyle='--', linewidth=1.2, alpha=0.55, zorder=4)
    ax1.set_ylabel('mph', color=TXT, fontsize=9)
    ax1.set_ylim(bottom=min(avgev)-3, top=max(maxev)+3)
    leg = ax1.legend(loc='upper left', fontsize=7.5, labelcolor=TXT)
    c1 = finalize(fig, ax1, [leg])
    # Chart 2: Hard Hit %
    fig, ax2 = plt.subplots(figsize=(10, 3.0))
    fig.patch.set_facecolor(BG)
    style_axis(ax2, months)
    ax2.plot(range(len(months)), hhpct, color=GRN, marker='^', linewidth=2, markersize=5.5,
             markerfacecolor=GRN, markeredgecolor='white', markeredgewidth=0.8, label='Hard Hit %', zorder=5)
    ax2.fill_between(range(len(months)), hhpct, alpha=0.06, color=GRN, zorder=1)
    tv2 = trend_vals(hhpct)
    ax2.plot([0, len(months)-1], tv2, color=GRN, linestyle='--', linewidth=1.2, alpha=0.55, zorder=4)
    ax2.set_ylabel('Hard Hit %', color=TXT, fontsize=9)
    ax2.set_ylim(bottom=0, top=max(hhpct)+18)
    leg2 = ax2.legend(loc='upper left', fontsize=7.5, labelcolor=TXT)
    c2 = finalize(fig, ax2, [leg2])
    return c1, c2

ok = 0; skipped = []
for uid, (slug, disp) in sorted(ROSTER.items()):
    path = os.path.join(BASE, f'{slug}_hitting_snapshot.html')
    if not os.path.exists(path):
        skipped.append((slug, 'no html'))
        continue
    rows = by_uid.get(uid, [])
    if len(rows) < 2:
        skipped.append((slug, f'insufficient data ({len(rows)} months)'))
        continue
    rows.sort(key=lambda r: r['ym'])
    rows = rows[-24:]  # last 24 months
    months = [r['ym'] for r in rows]
    maxev = [r['max'] for r in rows]
    avgev = [r['avg'] for r in rows]
    hhpct = [r['hh'] for r in rows]
    c1, c2 = make_charts(disp, months, maxev, avgev, hhpct)
    sections = f'''<div class="sec"><div class="st">Monthly Progress</div><div class="recs" style="padding:10px;">
<img src="data:image/png;base64,{c1}" style="width:100%;border-radius:6px;display:block;">
<div style="font-size:9px;color:#888888;opacity:0.5;text-align:center;margin-top:8px;">Monthly averages · Max EV &amp; Avg EV (mph) · dashed = trend · Last {len(months)} months</div>
</div></div>
<div class="sec"><div class="st">Hard Hit %</div><div class="recs" style="padding:10px;">
<img src="data:image/png;base64,{c2}" style="width:100%;border-radius:6px;display:block;">
<div style="font-size:9px;color:#888888;opacity:0.5;text-align:center;margin-top:8px;">Monthly Hard Hit % · per-session 92% of rolling max (30 sessions back) · dashed = trend · Last {len(months)} months</div>
</div></div>
'''
    html = open(path).read()
    # strip any previously embedded chart sections (idempotent re-run)
    if '<div class="sec"><div class="st">Monthly Progress</div>' in html:
        start = html.find('<div class="sec"><div class="st">Monthly Progress</div>')
        end = html.find('<div class="ft">')
        if start != -1 and end != -1 and start < end:
            html = html[:start] + html[end:]
    idx = html.find('<div class="ft">')
    if idx < 0:
        skipped.append((slug, 'no footer'))
        continue
    new_html = html[:idx] + sections + html[idx:]
    # backup original once
    bak = path + '.prechart'
    if not os.path.exists(bak):
        os.replace(path, bak)
    open(path, 'w').write(new_html)
    ok += 1
    print(f'{slug}: OK ({len(months)} months, {len(new_html)} chars)')

print(f'\nDone: {ok} cards updated, skipped: {skipped}')
