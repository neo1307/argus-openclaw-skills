---
name: B2B Lead Generation Scraper
description: Extracts verified B2B leads (name, email, company, LinkedIn, job title) from target sources and exports them as CRM-ready CSV files.
version: 1.0.0
tags: [python, scraping, lead-generation, b2b, linkedin, csv, crm, automation]
author: neo1307
requires: [python3, selenium, webdriver-manager, pandas, requests]
env:
  - LI_SESSION: LinkedIn session cookie (li_at value from browser)
runtime: chromium or chrome must be installed for Selenium headless mode
---

# B2B Lead Generation Scraper

## Overview
Automated lead extraction tool that collects verified B2B contact data from
target sources and delivers clean, CRM-ready CSV files. Delivers 500-2,000+
leads per run depending on target criteria.

## What It Does
- Extracts: Full name, job title, company name, LinkedIn URL, email (when available)
- Filters by: industry, job title keywords, company size, location
- Deduplicates records automatically
- Outputs clean CSV ready for HubSpot, Salesforce, Pipedrive import
- Validates and removes junk/incomplete rows before delivery

## Setup
1. Define target criteria in OpenClaw chat or `config/target.json`:
   - `industry`: e.g. "SaaS", "Real Estate", "Healthcare"
   - `job_titles`: e.g. ["CEO", "Head of Marketing", "VP Sales"]
   - `location`: e.g. "United States", "London"
   - `company_size`: e.g. "10-50", "50-200"
2. Set OpenClaw secrets:
   - `LI_SESSION` — LinkedIn session cookie (li_at)
3. Specify output path or let default to `data/leads/`

## Usage
> "Find 500 B2B leads: SaaS CEOs in the United States"
> "Scrape marketing directors at companies with 50-200 employees in London"
> "Generate a lead list of HR managers in healthcare companies"
> "Export leads to CSV formatted for HubSpot import"

## Output
- `leads_YYYY-MM-DD_[criteria].csv` with columns:
  - first_name, last_name, full_name, job_title, company, linkedin_url, email, location
- Summary: total found, duplicates removed, validation pass rate

## Rules
- Never scrape more than 200 profiles per hour to avoid detection
- Always deduplicate by LinkedIn URL before saving
- Mark rows with missing email as `email_status: not_found` — do not fabricate
- Save raw data before cleaning in `data/raw/`
- Output CSV must be UTF-8 encoded for CRM compatibility

## Pricing (MeshCore)
- Free tier: up to 50 leads per run
- Pro tier: up to 2,000 leads per run ($0.05/call)
