import difflib
from models import RemediateResponse
from scenarios import SCENARIOS

def generate_remediation(scenario_id: str) -> RemediateResponse:
    scenario = SCENARIOS.get(scenario_id, SCENARIOS["billing_transfer"])
    
    vulnerable_lines = scenario.vulnerable_code.splitlines(keepends=True)
    hardened_lines = scenario.hardened_code.splitlines(keepends=True)
    
    diff_generator = difflib.unified_diff(
        vulnerable_lines,
        hardened_lines,
        fromfile="services/billing_service.py (IBM Bob - Initial)",
        tofile="services/billing_service.py (Axiom Patched - Hardened)",
        n=3
    )
    unified_diff_str = "".join(diff_generator)

    fixed_invariants = [
        "Boundary Non-Negative Enforcement (Guarded with 'if amount <= 0: raise ValueError')",
        "Cross-Tenant Isolation Invariant (Guarded with sender.tenant_id == receiver.tenant_id)",
        "Idempotency Replay Protection (Enforced transaction registry check)",
        "Atomic State Invariant (Secured within serialized memory lock)"
    ]

    summary = (
        "IBM Bob received adversarial counter-example traces from Axiom and generated a zero-trust invariant patch: "
        "enforced explicit amount validation, organizational tenant barriers, and transaction idempotency filtering."
    )

    return RemediateResponse(
        scenario_id=scenario_id,
        patched_code=scenario.hardened_code,
        diff=unified_diff_str,
        fixed_invariants=fixed_invariants,
        remediation_summary=summary
    )
