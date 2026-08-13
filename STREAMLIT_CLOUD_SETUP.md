# Streamlit Community Cloud Deployment Guide

This guide walks you through deploying your FPL Fantasy Squads app to Streamlit Community Cloud.

## Prerequisites

1. **GitHub Account** - Required to deploy
2. **Streamlit Account** - Sign up at https://streamlit.io (free tier available)
3. **Your app code on GitHub** - Push your repo first

## Step 1: Push Your Code to GitHub

```bash
cd /home/nich/Desktop/FPLProject
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

**Important:** Make sure `.env` is in `.gitignore` so local secrets are never committed.

## Step 2: Create a Streamlit Account

1. Go to https://streamlit.io
2. Click "Sign up" 
3. Use your GitHub account to sign in (easiest option)

## Step 3: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **"New app"**
3. Fill in:
   - **Repository**: Select your GitHub repo (e.g., `your-username/FPLProject`)
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **"Deploy"**

Streamlit will automatically install dependencies from `requirements.txt` and start your app!

## Step 4: Configure Secrets

In your app's Streamlit Cloud dashboard, click **Settings → Secrets** and add:

```
API_FOOTBALL_KEY = "your-api-football-key"
DEFAULT_LEAGUE_ID = "39"
DEFAULT_SEASON = "2026"
SEASON_START_DATE = "2026-08-21"
WORK_SHEET_ID = "your-google-sheet-id"
WORK_SHEET_SQUADS = "Current Squads"
```

Click **Save** when finished. Streamlit Cloud makes these values available to the app as environment variables.

## Troubleshooting

### App crashes on startup
Check the logs in Streamlit Cloud dashboard (View logs):
- Missing dependencies? Update `requirements.txt`
- Missing secrets? Add them in Settings → Secrets


### Google Sheets connection fails
- Verify `SHEET_ID` and `SHEET_NAME` are correct
- Ensure the sheet is publicly readable

## Redeploying After Changes

Simply push to GitHub:
```bash
git add .
git commit -m "Update app"
git push origin main
```

Streamlit Cloud automatically redeploys within seconds!

## Costs

✅ **Free tier includes:**
- 1 public app
- Up to 1 GB of data storage
- Community support

For production apps with higher traffic, consider paid tiers.

## Testing Locally First

Before deploying, test locally:
```bash
source FPL_APP/bin/activate
streamlit run app.py
```

Visit http://localhost:8501 to verify everything works.
