#!/bin/bash
# Auto-publish updated player cards to GitHub Pages
# Runs via cron: copies fresh files, commits, pushes

REPO=/home/chadlongworth/earn-it-hitting-reports
SRC=/home/chadlongworth/cage-schedule

cd "$REPO" || exit 1

# Copy updated HTML files from cage-schedule
rsync -a "$SRC/"*_hitting_snapshot.html "$REPO/" 2>/dev/null
rsync -a "$SRC/roster_charts.py" "$REPO/" 2>/dev/null
rsync -a "$SRC/monthly_data.csv" "$REPO/data/" 2>/dev/null
[ ! -f "$REPO/data/monthly_data.csv" ] && mkdir -p "$REPO/data" && cp "$SRC/monthly_data.csv" "$REPO/data/"
[ ! -f "$REPO/scripts/roster_charts.py" ] && mkdir -p "$REPO/scripts" && cp "$SRC/roster_charts.py" "$REPO/scripts/"

# Check if anything changed
if git diff --quiet && git diff --cached --quiet; then
    exit 0  # no changes
fi

# Commit and push
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
git add -A
git commit -m "Auto-publish update $TIMESTAMP"
git push origin main 2>&1 || echo "Push failed (will retry next cycle)"
