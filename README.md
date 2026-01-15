# Daily YouTube Screenshot

This repo captures a daily screenshot from the latest upload on a specific YouTube channel and stores it in `output/`.

## What it does

- Fetches the latest video from the channel RSS feed.
- Downloads the video thumbnail image.
- Saves the frame to:
  - `output/latest.jpg`
  - `output/YYYY-MM-DD.jpg`

## Run locally

```bash
python scripts/daily_youtube_screenshot.py
```

## Customize the schedule

The GitHub Actions schedule lives in `.github/workflows/daily-youtube-screenshot.yml` under `on.schedule`. Update the cron expression to change the daily run time. For example, `0 8 * * *` runs at 08:00 UTC.

## GitHub Actions

The workflow is set up to run daily and via manual `workflow_dispatch`. It runs the capture script and commits any new screenshot files back to the repo.
