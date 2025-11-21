# Monitoring Render Database Enrichment

## Quick Status Check

Run this command to see current database status:

```bash
cd /Users/aazir/ncii-infra-mapping && ./check_render.sh
```

Or use the Python script directly:

```bash
cd /Users/aazir/ncii-infra-mapping && export POSTGRES_HOST='dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com' && export POSTGRES_PORT='5432' && export POSTGRES_USER='ncii_user' && export POSTGRES_PASSWORD='Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91' && export POSTGRES_DB='ncii' && python3 scripts/check_render_db.py
```

## Watch Enrichment Progress

To watch the enrichment log in real-time:

```bash
cd /Users/aazir/ncii-infra-mapping && tail -f enrichment.log
```

Press `Ctrl+C` to stop watching.

## Check Enrichment Process Status

To see if the enrichment process is running:

```bash
ps aux | grep enrich_domains | grep -v grep
```

## Restart Enrichment (if needed)

If the process stopped, restart it with:

```bash
cd /Users/aazir/ncii-infra-mapping && export POSTGRES_HOST='dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com' && export POSTGRES_PORT='5432' && export POSTGRES_USER='ncii_user' && export POSTGRES_PASSWORD='Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91' && export POSTGRES_DB='ncii' && nohup python3 scripts/enrich_domains.py --csv data/input/domains.csv > enrichment.log 2>&1 &
```

## View Last 50 Lines of Log

```bash
cd /Users/aazir/ncii-infra-mapping && tail -50 enrichment.log
```


