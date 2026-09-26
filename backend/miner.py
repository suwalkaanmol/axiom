import re
from typing import List, Tuple
from models import Invariant

SCENARIO_INVARIANTS = {
    "billing_transfer": [
        Invariant(
            id="inv_billing_01",
            title="Boundary Non-Negative Enforcement",
            category="boundary",
            severity="CRITICAL",
            description="The transfer function validates sender balance sufficiency, but omits bounds checking for negative transfer amounts.",
            implicit_assumption="LLM assumed amount > 0 is guaranteed by the API client or schema validator.",
            exploit_scenario="Passing amount = -500.0 results in sender balance INCREASING by 500 (credit multiplication exploit).",
            line_number=11,
            status="detected"
        ),
        Invariant(
            id="inv_billing_02",
            title="Cross-Tenant Isolation Invariant",
            category="tenant_isolation",
            severity="CRITICAL",
            description="Transfers are executed between any two arbitrary wallet IDs without validating tenant or organizational affiliation.",
            implicit_assumption="LLM assumed caller permissions prevent inter-organizational wallet interaction.",
            exploit_scenario="A rogue tenant account can execute transfers targeting wallets in unrelated enterprise workspaces.",
            line_number=7,
            status="detected"
        ),
        Invariant(
            id="inv_billing_03",
            title="Idempotency Replay Protection",
            category="idempotency",
            severity="HIGH",
            description="The method accepts an optional idempotency_key parameter but does not check prior transaction logs before applying state mutations.",
            implicit_assumption="LLM assumed network gateways deduplicate retry requests upstream.",
            exploit_scenario="Network timeout causes client retry; the wallet balance is debited twice for a single transaction.",
            line_number=2,
            status="detected"
        ),
        Invariant(
            id="inv_billing_04",
            title="Atomic State Transition & Concurrency Lock",
            category="concurrency",
            severity="HIGH",
            description="Non-atomic read-modify-write pattern allows race conditions under concurrent burst requests.",
            implicit_assumption="LLM assumed single-threaded execution or database-level serializable isolation.",
            exploit_scenario="Two concurrent $80 transfers on a $100 balance both pass balance checks and result in negative account balance.",
            line_number=15,
            status="detected"
        ),
    ],
    "inventory_reservation": [
        Invariant(
            id="inv_inv_01",
            title="Cart Quantity Range Invariant",
            category="boundary",
            severity="CRITICAL",
            description="Quantity decrement does not assert minimum purchase boundaries (> 0).",
            implicit_assumption="LLM assumed quantity is strictly >= 1.",
            exploit_scenario="Passing quantity = -10 artificially increases warehouse available stock.",
            line_number=6,
            status="detected"
        ),
        Invariant(
            id="inv_inv_02",
            title="Bulk Order Quota Boundary",
            category="boundary",
            severity="MEDIUM",
            description="No maximum order ceiling per transaction.",
            implicit_assumption="LLM assumed inventory stock buffer is sufficient for unbounded requests.",
            exploit_scenario="Bot orders 500,000 units in a single hit, starving inventory without payment capture.",
            line_number=2,
            status="detected"
        )
    ],
    "saas_tenant_export": [
        Invariant(
            id="inv_saas_01",
            title="Immutable Workspace Scope Invariant",
            category="tenant_isolation",
            severity="CRITICAL",
            description="Query filter dictionary can override the root workspace_id partition key.",
            implicit_assumption="LLM assumed input dictionaries are sanitized before reaching repository layer.",
            exploit_scenario="Attacker passes {'workspace_id': 'victim_corp'} to dump unauthorized tenant records.",
            line_number=3,
            status="detected"
        )
    ]
}


def extract_invariants(scenario_id: str, custom_code: str = None) -> Tuple[List[Invariant], int]:
    """
    Analyzes code or scenario to extract unstated ghost invariants and compute AI risk score.
    """
    if scenario_id in SCENARIO_INVARIANTS and not custom_code:
        invariants = SCENARIO_INVARIANTS[scenario_id]
        risk_score = 88 if scenario_id == "billing_transfer" else (76 if scenario_id == "inventory_reservation" else 92)
        return invariants, risk_score

    # Generic heuristics engine for custom pasted code
    invariants = []
    code = custom_code or ""

    if "< 0" not in code and "<= 0" not in code and ("amount" in code.lower() or "price" in code.lower() or "quantity" in code.lower()):
        invariants.append(Invariant(
            id="inv_custom_01",
            title="Implicit Non-Negative Input Boundary",
            category="boundary",
            severity="CRITICAL",
            description="Mathematical state mutation without lower bound check.",
            implicit_assumption="LLM assumed input values are sanitized and strictly positive.",
            exploit_scenario="Negative numeric inputs can reverse credit/debit arithmetic.",
            line_number=10,
            status="detected"
        ))

    if "tenant" not in code.lower() and "org" not in code.lower() and ("user" in code.lower() or "account" in code.lower()):
        invariants.append(Invariant(
            id="inv_custom_02",
            title="Missing Multi-Tenant Isolation Fence",
            category="tenant_isolation",
            severity="HIGH",
            description="Entity identifiers accessed across trust boundaries without tenant validation.",
            implicit_assumption="LLM assumed single-tenant runtime context.",
            exploit_scenario="Cross-workspace reference leak.",
            line_number=5,
            status="detected"
        ))

    if "idempotency" not in code.lower() and ("tx" in code.lower() or "transfer" in code.lower() or "order" in code.lower()):
        invariants.append(Invariant(
            id="inv_custom_03",
            title="Unprotected State Mutation (No Idempotency)",
            category="idempotency",
            severity="HIGH",
            description="Side-effect inducing operation without replay tokens.",
            implicit_assumption="LLM assumed idempotent transport layer.",
            exploit_scenario="Network retries produce duplicated mutations.",
            line_number=1,
            status="detected"
        ))

    risk_score = min(95, 30 + len(invariants) * 20)
    return invariants, risk_score
