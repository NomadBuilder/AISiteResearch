# Keeping Render and Mac Awake During Enrichment

## Problem
- **Render free tier**: Spins down after 15 minutes of inactivity
- **MacBook**: Goes to sleep, stopping enrichment process

## Solutions

### Option 1: Run Enrichment with Mac Sleep Prevention (Recommended)

Run this command to start enrichment - your Mac won't sleep while it runs:

```bash
cd /Users/aazir/ncii-infra-mapping && ./scripts/run_enrichment_with_caffeinate.sh
```

This will:
- ✅ Prevent Mac from sleeping during enrichment
- ✅ Process only missing domains (faster)
- ✅ Log everything to `enrichment.log`
- ✅ Let Mac sleep normally when done

### Option 2: Keep Render Awake (Separate Terminal)

In a **separate terminal**, run this to ping Render every 5 minutes:

```bash
cd /Users/aazir/ncii-infra-mapping && ./scripts/keepalive_render.sh
```

Or manually ping it:
```bash
curl https://ncii-infra-mapping.onrender.com/
```

### Option 3: Use External Keepalive Service (Free)

Set up a free service to ping Render automatically:

1. **UptimeRobot** (https://uptimerobot.com/)
   - Create free account
   - Add monitor: `https://ncii-infra-mapping.onrender.com/`
   - Set interval: 5 minutes
   - Free tier: 50 monitors

2. **cron-job.org** (https://cron-job.org/)
   - Create free account
   - Add cron job: `curl https://ncii-infra-mapping.onrender.com/`
   - Set schedule: Every 5 minutes

### Option 4: Run Both Together

**Terminal 1** - Enrichment (prevents Mac sleep):
```bash
cd /Users/aazir/ncii-infra-mapping && ./scripts/run_enrichment_with_caffeinate.sh
```

**Terminal 2** - Keep Render awake:
```bash
cd /Users/aazir/ncii-infra-mapping && ./scripts/keepalive_render.sh
```

## Monitor Progress

Check database status:
```bash
cd /Users/aazir/ncii-infra-mapping && ./check_render.sh
```

Watch enrichment log:
```bash
cd /Users/aazir/ncii-infra-mapping && tail -f enrichment.log
```

## Notes

- Render free tier wakes up automatically when pinged (takes ~30 seconds)
- Mac `caffeinate` only works while the script runs
- For long-term, consider UptimeRobot or upgrading Render to always-on ($7/month)

