# Daily YouTube Screenshot

This repo captures a daily screenshot from the latest upload on a specific YouTube channel and stores it in `output/`.

## What it does

- Fetches the latest video from the channel RSS feed.
- Downloads the video with `yt-dlp`.
- Extracts a single frame at `00:00:12` with `ffmpeg`.
- Saves the frame to:
  - `output/latest.jpg`
  - `output/YYYY-MM-DD.jpg`

## Run locally

```bash
pip install -r requirements.txt
python scripts/daily_youtube_screenshot.py
```

> **Note:** You need `ffmpeg` installed and available on your PATH.

## Customize the timestamp

Edit the `TIMESTAMP` constant in `scripts/daily_youtube_screenshot.py` to the `HH:MM:SS` value you want (e.g. `00:00:05`).

## Customize the schedule

The GitHub Actions schedule lives in `.github/workflows/daily-youtube-screenshot.yml` under `on.schedule`. Update the cron expression to change the daily run time. For example, `0 8 * * *` runs at 08:00 UTC.

## GitHub Actions

The workflow is set up to run daily and via manual `workflow_dispatch`. It installs `ffmpeg`, installs Python dependencies, runs the capture script, and commits any new screenshot files back to the repo.
