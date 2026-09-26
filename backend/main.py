import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from models import (
    AnalyzeRequest, AnalyzeResponse,
    FuzzRequest, FuzzResponse,
    RemediateRequest, RemediateResponse,
    ResiliencePassport
)
from scenarios import SCENARIOS
from miner import extract_invariants
from blast_radius import generate_blast_radius
from fuzzer import run_adversarial_suite
from remediator import generate_remediation
from passport import generate_resilience_passport

app = FastAPI(
    title="Axiom Enterprise API",
    description="Adversarial Invariant & Blast-Radius Engine for Autonomous AI Devs (IBM Bob 2.0 Hackathon)",
    version="2.0.0"
)

# Enable CORS for Next.js / React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Axiom Sentinel Core",
        "version": "2.0.0",
        "engine": "Adversarial Invariant & Blast-Radius Engine"
    }


@app.get("/api/scenarios")
def list_scenarios():
    return [
        {
            "id": s.id,
            "name": s.name,
            "category": s.category,
            "description": s.description,
            "target_file": s.target_file,
            "vulnerable_code": s.vulnerable_code,
            "hardened_code": s.hardened_code
        }
        for s in SCENARIOS.values()
    ]


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_code(req: AnalyzeRequest):
    scenario_id = req.scenario_id or "billing_transfer"
    invariants, risk_score = extract_invariants(scenario_id, req.code_content)
    blast_radius = generate_blast_radius(scenario_id, status_mode="vulnerable")

    recommendation = (
        f"CRITICAL: Found {len(invariants)} unstated ghost invariants. "
        "High risk of silent production failure or balance exploitation. Run Adversarial Fuzzing immediately."
    )

    return AnalyzeResponse(
        scenario_id=scenario_id,
        detected_invariants=invariants,
        blast_radius=blast_radius,
        ai_risk_score=risk_score,
        recommendation=recommendation
    )


@app.post("/api/fuzz", response_model=FuzzResponse)
def fuzz_invariants(req: FuzzRequest):
    scenario_id = req.scenario_id or "billing_transfer"
    code_mode = req.code_mode or "vulnerable"
    result = run_adversarial_suite(scenario_id, code_mode)
    return result


@app.post("/api/remediate", response_model=RemediateResponse)
def remediate_code(req: RemediateRequest):
    scenario_id = req.scenario_id or "billing_transfer"
    result = generate_remediation(scenario_id)
    return result


@app.get("/api/passport/{scenario_id}", response_model=ResiliencePassport)
def get_passport(scenario_id: str):
    passport = generate_resilience_passport(scenario_id)
    return passport


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
