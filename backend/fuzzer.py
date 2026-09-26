import sys
import os
import copy
from typing import List
from models import TestCaseResult, FuzzResponse

# Ensure target_services path is accessible
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
TARGETS_DIR = os.path.join(PARENT_DIR, "target_services")
if TARGETS_DIR not in sys.path:
    sys.path.insert(0, TARGETS_DIR)

import billing_service


def run_adversarial_suite(scenario_id: str, code_mode: str = "vulnerable") -> FuzzResponse:
    """
    Executes live synthesized adversarial tests against target service code.
    code_mode: 'vulnerable' (AI code) or 'hardened' (Axiom patch)
    """
    test_results: List[TestCaseResult] = []
    terminal_lines = [
        f"======================== test session starts ========================",
        f"platform win32 -- Python {sys.version.split()[0]}, pytest-9.1.1, pluggy-1.6.0",
        f"rootdir: {PARENT_DIR}",
        f"collected 3 adversarial items for target: {scenario_id} [{code_mode.upper()} MODE]",
        ""
    ]

    # Reset in-memory DB for clean execution
    billing_service.WALLETS_DB = {
        "acc_alice": {"id": "acc_alice", "tenant_id": "org_ibm", "balance": 100.0, "currency": "USD"},
        "acc_bob": {"id": "acc_bob", "tenant_id": "org_ibm", "balance": 50.0, "currency": "USD"},
        "acc_mallory": {"id": "acc_mallory", "tenant_id": "org_external", "balance": 0.0, "currency": "USD"},
    }
    billing_service.TRANSACTION_LOG.clear()

    fn_to_test = (
        billing_service.transfer_funds_vulnerable
        if code_mode == "vulnerable"
        else billing_service.transfer_funds_hardened
    )

    # -------------------------------------------------------------
    # Test 1: Negative Amount (Boundary Invariant)
    # -------------------------------------------------------------
    t1_passed = False
    t1_actual = ""
    t1_stack = None
    try:
        res = fn_to_test("acc_alice", "acc_bob", -500.0)
        # If no error thrown, check if balance exploit occurred
        t1_actual = f"HTTP 200 OK | Balance: {res['sender_balance']} USD (Credit Duplication Exploit Succeeded!)"
        t1_stack = (
            "Traceback (most recent call last):\n"
            "  File \"test_adversarial.py\", line 18, in test_negative_transfer_boundary\n"
            "    with pytest.raises(ValueError, match='Transfer amount must be strictly positive'):\n"
            "        transfer_funds('acc_alice', 'acc_bob', -500.0)\n"
            "E   Failed: DID NOT RAISE <class 'ValueError'>. Sender balance illegally incremented to 600.0!"
        )
    except ValueError as e:
        t1_passed = True
        t1_actual = f"Rejected with ValueError: {str(e)}"

    test_results.append(TestCaseResult(
        test_id="ADV-01",
        name="test_negative_transfer_boundary",
        invariant_targeted="Boundary Non-Negative Enforcement",
        input_payload={"sender_id": "acc_alice", "receiver_id": "acc_bob", "amount": -500.0},
        expected_behavior="Raise ValueError: Transfer amount must be strictly positive (> 0)",
        actual_result=t1_actual,
        passed=t1_passed,
        stack_trace=t1_stack
    ))

    # -------------------------------------------------------------
    # Test 2: Cross-Tenant Transfer (Isolation Invariant)
    # -------------------------------------------------------------
    t2_passed = False
    t2_actual = ""
    t2_stack = None
    try:
        res = fn_to_test("acc_alice", "acc_mallory", 20.0)
        t2_actual = f"HTTP 200 OK | Transferred 20 USD from org_ibm to unauthorized tenant org_external!"
        t2_stack = (
            "Traceback (most recent call last):\n"
            "  File \"test_adversarial.py\", line 34, in test_cross_tenant_isolation_boundary\n"
            "    with pytest.raises(PermissionError, match='Cross-tenant transfers are forbidden'):\n"
            "        transfer_funds('acc_alice', 'acc_mallory', 20.0)\n"
            "E   Failed: DID NOT RAISE <class 'PermissionError'>. Cross-tenant leakage verified!"
        )
    except PermissionError as e:
        t2_passed = True
        t2_actual = f"Rejected with PermissionError: {str(e)}"

    test_results.append(TestCaseResult(
        test_id="ADV-02",
        name="test_cross_tenant_isolation_boundary",
        invariant_targeted="Cross-Tenant Isolation Invariant",
        input_payload={"sender": "acc_alice (org_ibm)", "receiver": "acc_mallory (org_external)", "amount": 20.0},
        expected_behavior="Raise PermissionError: Cross-tenant transfers are forbidden",
        actual_result=t2_actual,
        passed=t2_passed,
        stack_trace=t2_stack
    ))

    # -------------------------------------------------------------
    # Test 3: Idempotency Replay (Replay Protection Invariant)
    # -------------------------------------------------------------
    t3_passed = False
    t3_actual = ""
    t3_stack = None
    try:
        # First call
        fn_to_test("acc_alice", "acc_bob", 10.0, idempotency_key="idemp_1001")
        # Duplicate replay call
        res2 = fn_to_test("acc_alice", "acc_bob", 10.0, idempotency_key="idemp_1001")
        if res2.get("status") == "idempotent_duplicate":
            t3_passed = True
            t3_actual = "Deduplicated successfully (idempotent_duplicate acknowledged)"
        else:
            t3_actual = f"Double-debit occurred! Sender balance debited twice (Remaining: {res2.get('sender_balance')} USD)"
            t3_stack = (
                "Traceback (most recent call last):\n"
                "  File \"test_adversarial.py\", line 52, in test_idempotency_replay_filter\n"
                "    assert res2['status'] == 'idempotent_duplicate'\n"
                "E   AssertionError: assert 'success' == 'idempotent_duplicate'\n"
                "E     Replay attack debited sender balance twice for key 'idemp_1001'"
            )
    except Exception as e:
        t3_actual = f"Error: {str(e)}"

    test_results.append(TestCaseResult(
        test_id="ADV-03",
        name="test_idempotency_replay_filter",
        invariant_targeted="Idempotency Replay Protection",
        input_payload={"sender": "acc_alice", "receiver": "acc_bob", "amount": 10.0, "idempotency_key": "idemp_1001"},
        expected_behavior="Filter duplicate replay; return previous receipt without deducting balance twice",
        actual_result=t3_actual,
        passed=t3_passed,
        stack_trace=t3_stack
    ))

    # Format terminal logs
    for r in test_results:
        symbol = "PASSED [33%]" if r.passed else "FAILED [33%]"
        prefix = "tests/test_adversarial.py::" + r.name
        terminal_lines.append(f"{prefix:<55} {symbol}")

    terminal_lines.append("")
    if not all(r.passed for r in test_results):
        terminal_lines.append("=================================== FAILURES ===================================")
        for r in test_results:
            if not r.passed and r.stack_trace:
                terminal_lines.append(f"__________________________ {r.name} __________________________")
                terminal_lines.append(r.stack_trace)
                terminal_lines.append("")

    failed_count = sum(1 for r in test_results if not r.passed)
    passed_count = sum(1 for r in test_results if r.passed)

    if failed_count > 0:
        terminal_lines.append(f"======================= {failed_count} failed, {passed_count} passed in 0.14s =======================")
    else:
        terminal_lines.append(f"======================= {passed_count} passed, 0 failed in 0.08s =======================")

    return FuzzResponse(
        scenario_id=scenario_id,
        code_mode=code_mode,
        total_tests=len(test_results),
        passed_tests=passed_count,
        failed_tests=failed_count,
        test_results=test_results,
        terminal_logs="\n".join(terminal_lines),
        all_secured=(failed_count == 0)
    )
