# Earn It Academy — Hitting Snapshots

Weekly hitting performance reports for Earn It Academy athletes, auto-generated from HitTrax data every Friday morning.

## Players
- Bennett Baker (8U)
- Greyson Davidson (8U)
- Aymes Deel (12U)
- McQuade Niece (8U)
- Irby Stewart (8U)
- Jake Wallencat (8U)
- Tripp Stanley (10U)
- Eli Pate (8U)

## Auto-Update
A cron job on the gateway server queries HitTrax SQL Server every Friday at 7:00 AM ET, rebuilds all reports, and pushes updates to this repo.

## Tech
- Data: HitTrax SQL Server (SQLEXPRESS)
- Builder: `batch_snapshots_v3.py`
- Hosting: GitHub Pages