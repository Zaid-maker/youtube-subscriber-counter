# YouTube Subscriber Counter — Prototype

A simple dark, large-number browser dashboard for a **public** YouTube channel. It queries the YouTube Data API server-side so the API key is not embedded in the webpage. The dashboard refreshes every 60 seconds.

## Important limits

- The official YouTube Data API rounds `subscriberCount` down to three significant figures. This is not a second-by-second exact live counter.
- Do not present the stream as official or affiliated with the channel owner. Avoid using their branding in a misleading way.
- GitHub Actions is used here only for a short preview test, not as a continuous streaming host. GitHub-hosted jobs have a six-hour maximum and service terms/quotas still apply.
- A public repository's source is visible. Never put API keys or stream keys in committed files.

## 1. Get YouTube API credentials

1. Open Google Cloud Console and create/select a project.
2. Enable **YouTube Data API v3**.
3. Create an API key. Restrict it to YouTube Data API v3 where possible.
4. Find the target channel's channel ID (usually starts with `UC`). A channel handle URL is not always itself the channel ID.

## 2. Test locally (optional)

Requires Python 3.10+ and a browser.

```bash
export YOUTUBE_API_KEY='your-api-key'
export YOUTUBE_CHANNEL_ID='UCxxxxxxxxxxxxxxxxxxxxxx'
python3 server.py
```

Open `http://localhost:8000` in your browser. The API key remains in the Python process, not in the page. This is intended for local development; do not expose this server publicly without adding authentication and rate limiting.

## 3. Test on GitHub Actions

1. Create a GitHub repository and upload these files, including `.github/workflows/dashboard-test.yml`.
2. In **Settings → Secrets and variables → Actions**, add:
   - `YOUTUBE_API_KEY`
   - `YOUTUBE_CHANNEL_ID`
3. Open **Actions → Subscriber Counter Dashboard Test → Run workflow**.
4. Open the completed run and download `subscriber-counter-preview` from Artifacts.

The workflow verifies the API call, opens the dashboard in a virtual display, and records a 30-second preview. If the runner's Chromium package name changes, adjust the install/launch command to match the current Ubuntu image.

## 4. Live broadcasting

This repository intentionally does not launch a long-running broadcast from GitHub Actions. Once the preview works, run the same dashboard + capture + FFmpeg pipeline on a host whose terms permit live streaming. Store the YouTube RTMPS URL and stream key as secrets/environment variables, never in the repository. Test privately/unlisted first and confirm the stream preview in YouTube Studio before going public.
