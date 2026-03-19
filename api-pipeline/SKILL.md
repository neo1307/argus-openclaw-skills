---
name: Multi-API Data Pipeline to Google Sheets
description: Connects multiple REST APIs, fetches and transforms data, and pushes it to a live Google Sheets dashboard that auto-updates on a schedule.
version: 1.0.0
tags: [python, api, automation, google-sheets, pipeline, dashboard, data, fastapi]
author: neo1307
requires: [python3, requests, pandas, gspread, google-auth-oauthlib]
env:
  - GOOGLE_SERVICE_ACCOUNT_JSON: Google Service Account key as JSON string
  - TARGET_SHEET_ID: Google Sheets document ID (from the URL)
  - API_KEY_1..N: One secret per connected API (naming convention: SERVICE_API_KEY)
---

# Multi-API Data Pipeline to Google Sheets

## Overview
Automated data pipeline that pulls from multiple REST APIs, transforms and
merges the data, and pushes it to a Google Sheets dashboard that updates
automatically on your chosen schedule (every 15 minutes, hourly, daily).
Replaces hours of manual copy-paste work.

## What It Does
- Connects to up to 10 REST APIs simultaneously
- Handles authentication: API keys, Bearer tokens, OAuth2
- Transforms and merges data across sources
- Pushes clean, formatted data to Google Sheets in real time
- Sends Slack/email alert if any API call fails
- Logs all pipeline runs with success/failure status

## Setup
1. Define API sources in OpenClaw chat or `config/apis.json`:
   - endpoint URL, auth type, auth credentials, fields to extract
2. Set OpenClaw secrets:
   - `GOOGLE_SERVICE_ACCOUNT_JSON` — Google Service Account key (JSON string)
   - `TARGET_SHEET_ID` — Google Sheets document ID
   - One secret per API key: e.g. `SHOPIFY_API_KEY`, `HUBSPOT_TOKEN`
3. Define target sheet tab names and column mappings
4. Set update schedule: `every 15 minutes` / `hourly` / `daily at 06:00`

## Usage
> "Connect Shopify and HubSpot APIs and sync sales data to my Google Sheet every hour"
> "Pull weather data and stock prices into a live dashboard"
> "Set up a pipeline from our internal API to Google Sheets, update every 15 minutes"
> "Add Stripe revenue data to the existing pipeline"

## Output
- Live Google Sheets dashboard with latest data
- Pipeline run log: `logs/pipeline_YYYY-MM-DD.txt`
- Slack/email alert on failure with error details

## Rules
- Never store raw API credentials in output files or logs
- Always validate API response schema before writing to Sheets (fail loudly if schema changed)
- If Google Sheets write fails, buffer data locally and retry up to 3 times
- Respect API rate limits — add delays per API documentation
- Each pipeline run must write a summary row to a `_run_log` tab in the Sheet

## Pricing (MeshCore)
- Free tier: 2 API sources, updates every 60 minutes
- Pro tier: up to 10 APIs, updates every 15 minutes ($0.05/call)
