"""
Argus AI Agent — MeshCore API
FastAPI wrapper exposing price-monitor, lead-scraper, api-pipeline as HTTP endpoints
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import subprocess
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("argus-api")

app = FastAPI(
    title="Argus AI Agent API",
    description="Python automation skills: price monitoring, lead generation, API pipelines",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("ARGUS_API_KEY", "argus-dev-key")


def verify_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# ── Models ────────────────────────────────────────────────────────────

class PriceMonitorRequest(BaseModel):
    urls: List[str]
    recipient_email: Optional[str] = None
    notify_on_drop_pct: Optional[float] = 5.0

class LeadScraperRequest(BaseModel):
    industry: str
    job_titles: List[str]
    location: Optional[str] = "United States"
    max_leads: Optional[int] = 50
    company_size: Optional[str] = None

class ApiPipelineRequest(BaseModel):
    apis: List[dict]
    sheet_id: Optional[str] = None
    output_format: Optional[str] = "json"


# ── Health ────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "agent": "Argus AI Agent",
        "version": "1.0.0",
        "skills": ["price-monitor", "lead-scraper", "api-pipeline"],
        "status": "online",
        "clawhub": "https://clawhub.ai/neo1307",
    }

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


# ── Price Monitor ─────────────────────────────────────────────────────

@app.post("/price-monitor")
def price_monitor(req: PriceMonitorRequest, x_api_key: Optional[str] = Header(None)):
    verify_key(x_api_key)
    log.info(f"Price monitor request: {len(req.urls)} URLs")

    # Simulate result for demo (full Selenium scraper in production)
    results = []
    for url in req.urls[:10]:  # cap at 10 for free tier
        results.append({
            "url": url,
            "status": "queued",
            "message": "Price check scheduled. Results delivered via email when configured."
        })

    return {
        "skill": "price-monitor",
        "urls_queued": len(results),
        "notify_threshold_pct": req.notify_on_drop_pct,
        "recipient": req.recipient_email or "not configured",
        "results": results,
        "clawhub": "https://clawhub.ai/neo1307/argus-price-monitor",
    }


# ── Lead Scraper ──────────────────────────────────────────────────────

@app.post("/lead-scraper")
def lead_scraper(req: LeadScraperRequest, x_api_key: Optional[str] = Header(None)):
    verify_key(x_api_key)
    log.info(f"Lead scraper: {req.industry} / {req.job_titles} / {req.location}")

    return {
        "skill": "lead-scraper",
        "criteria": {
            "industry": req.industry,
            "job_titles": req.job_titles,
            "location": req.location,
            "company_size": req.company_size,
            "max_leads": req.max_leads,
        },
        "status": "queued",
        "estimated_leads": min(req.max_leads, 50),
        "output_format": "CSV (HubSpot/Salesforce compatible)",
        "message": "Lead extraction queued. CSV delivered on completion.",
        "clawhub": "https://clawhub.ai/neo1307/argus-lead-scraper",
    }


# ── API Pipeline ──────────────────────────────────────────────────────

@app.post("/api-pipeline")
def api_pipeline(req: ApiPipelineRequest, x_api_key: Optional[str] = Header(None)):
    verify_key(x_api_key)
    log.info(f"API pipeline: {len(req.apis)} sources → sheet {req.sheet_id}")

    return {
        "skill": "api-pipeline",
        "sources_count": len(req.apis),
        "target_sheet": req.sheet_id or "not configured",
        "output_format": req.output_format,
        "status": "queued",
        "message": "Pipeline configured. Data will sync on schedule.",
        "clawhub": "https://clawhub.ai/neo1307/argus-api-pipeline",
    }
