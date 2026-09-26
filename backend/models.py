from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Scenario(BaseModel):
    id: str
    name: str
    category: str
    description: str
    target_file: str
    vulnerable_code: str
    hardened_code: str

class Invariant(BaseModel):
    id: str
    title: str
    category: str  # "boundary", "concurrency", "tenant_isolation", "idempotency", "architectural"
    severity: str  # "CRITICAL", "HIGH", "MEDIUM"
    description: str
    implicit_assumption: str
    exploit_scenario: str
    status: str = "detected"  # "detected", "failing", "verified_fixed"
    line_number: Optional[int] = None

class BlastRadiusNode(BaseModel):
    id: str
    label: str
    type: str  # "service", "database", "external_api", "queue", "client"
    status: str  # "impacted", "critical", "safe", "monitored"
    details: str

class BlastRadiusEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str
    risk_level: str  # "high", "medium", "low"

class BlastRadiusGraph(BaseModel):
    nodes: List[BlastRadiusNode]
    edges: List[BlastRadiusEdge]
    risk_score: int  # 0 to 100
    impact_summary: str

class AnalyzeRequest(BaseModel):
    scenario_id: Optional[str] = None
    code_content: Optional[str] = None
    diff_content: Optional[str] = None

class AnalyzeResponse(BaseModel):
    scenario_id: str
    detected_invariants: List[Invariant]
    blast_radius: BlastRadiusGraph
    ai_risk_score: int
    recommendation: str

class FuzzRequest(BaseModel):
    scenario_id: str
    code_mode: str = "vulnerable"  # "vulnerable" or "hardened"

class TestCaseResult(BaseModel):
    test_id: str
    name: str
    invariant_targeted: str
    input_payload: Dict[str, Any]
    expected_behavior: str
    actual_result: str
    passed: bool
    stack_trace: Optional[str] = None

class FuzzResponse(BaseModel):
    scenario_id: str
    code_mode: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    test_results: List[TestCaseResult]
    terminal_logs: str
    all_secured: bool

class RemediateRequest(BaseModel):
    scenario_id: str

class RemediateResponse(BaseModel):
    scenario_id: str
    patched_code: str
    diff: str
    fixed_invariants: List[str]
    remediation_summary: str

class ResiliencePassport(BaseModel):
    passport_id: str
    issued_at: str
    repo_target: str
    commit_sha: str
    author_agent: str
    auditor: str = "Axiom Sentinel v2.0"
    invariants_audited: int
    adversarial_tests_passed: int
    risk_score_before: int
    risk_score_after: int
    cryptographic_signature: str
    verification_badge_markdown: str
    json_attestation: Dict[str, Any]
