from typing import Dict
from models import Scenario

SCENARIOS: Dict[str, Scenario] = {
    "billing_transfer": Scenario(
        id="billing_transfer",
        name="FinTech / Credit Wallet Transfer",
        category="Financial Services & Billing",
        description="IBM Bob generated an account wallet transfer endpoint. The code compiles and passes basic happy-path tests, but hides critical silent assumptions around negative inputs, tenant isolation, and idempotency.",
        target_file="services/billing_service.py",
        vulnerable_code='''def transfer_funds(sender_id: str, receiver_id: str, amount: float, idempotency_key: str = None) -> dict:
    if sender_id not in WALLETS_DB or receiver_id not in WALLETS_DB:
        raise KeyError("Account wallet does not exist")

    sender = WALLETS_DB[sender_id]
    receiver = WALLETS_DB[receiver_id]

    # AI check: only checked for insufficient funds
    if sender["balance"] < amount:
        raise ValueError("Insufficient balance")

    # State mutation without bounds check or atomic lock
    sender["balance"] -= amount
    receiver["balance"] += amount

    tx_id = f"tx_{uuid.uuid4().hex[:8]}"
    return {"status": "success", "tx_id": tx_id, "sender_balance": sender["balance"]}''',
        hardened_code='''def transfer_funds(sender_id: str, receiver_id: str, amount: float, idempotency_key: str = None) -> dict:
    # 1. Invariant: Amount Boundary Verification
    if amount <= 0:
        raise ValueError("Transfer amount must be strictly positive (> 0)")

    if sender_id not in WALLETS_DB or receiver_id not in WALLETS_DB:
        raise KeyError("Account wallet does not exist")

    sender = WALLETS_DB[sender_id]
    receiver = WALLETS_DB[receiver_id]

    # 2. Invariant: Cross-Tenant Isolation Enforcement
    if sender.get("tenant_id") != receiver.get("tenant_id"):
        raise PermissionError("Cross-tenant transfers are forbidden without organizational authorization")

    # 3. Invariant: Idempotency Protection Replay Filter
    if idempotency_key:
        for prev in TRANSACTION_LOG:
            if prev.get("idempotency_key") == idempotency_key:
                return {"status": "idempotent_duplicate", "tx_id": prev["tx_id"], "sender_balance": sender["balance"]}

    if sender["balance"] < amount:
        raise ValueError("Insufficient balance")

    sender["balance"] -= amount
    receiver["balance"] += amount

    tx_id = f"tx_{uuid.uuid4().hex[:8]}"
    TRANSACTION_LOG.append({"tx_id": tx_id, "idempotency_key": idempotency_key, "amount": amount})
    return {"status": "success", "tx_id": tx_id, "sender_balance": sender["balance"]}'''
    ),
    "inventory_reservation": Scenario(
        id="inventory_reservation",
        name="E-Commerce / Flash Sale Inventory",
        category="Supply Chain & E-Commerce",
        description="IBM Bob refactored warehouse checkout stock decrement. It silently assumed cart item quantities are strictly within [1, max_warehouse_stock], leading to stock underflow and negative cart exploits.",
        target_file="services/inventory_service.py",
        vulnerable_code='''def reserve_stock(sku: str, quantity: int, cart_id: str) -> dict:
    item = INVENTORY_DB.get(sku)
    if not item:
        raise KeyError(f"SKU {sku} not found")

    if item["available_stock"] < quantity:
        raise ValueError("Not enough stock available")

    # AI mutation without bounds or negative cart check
    item["available_stock"] -= quantity
    return {"status": "reserved", "sku": sku, "remaining_stock": item["available_stock"]}''',
        hardened_code='''def reserve_stock(sku: str, quantity: int, cart_id: str) -> dict:
    # 1. Invariant: Strictly positive item quantity
    if quantity <= 0:
        raise ValueError("Reserved quantity must be at least 1")
    if quantity > 50:
        raise ValueError("Bulk order exceeds single-transaction safety limit (50 max)")

    item = INVENTORY_DB.get(sku)
    if not item:
        raise KeyError(f"SKU {sku} not found")

    if item["available_stock"] < quantity:
        raise ValueError("Not enough stock available")

    item["available_stock"] -= quantity
    return {"status": "reserved", "sku": sku, "remaining_stock": item["available_stock"]}'''
    ),
    "saas_tenant_export": Scenario(
        id="saas_tenant_export",
        name="Multi-Tenant SaaS / Audit Log Exporter",
        category="Cloud Security & Compliance",
        description="IBM Bob implemented an async audit export handler. It assumed user query parameters are implicitly scoped to the requesting workspace, creating a high-severity cross-tenant data leak vulnerability.",
        target_file="services/audit_service.py",
        vulnerable_code='''def export_audit_logs(workspace_id: str, query_filter: dict) -> list:
    # AI assumed query_filter cannot override workspace_id
    records = AUDIT_DB.find_many(query_filter)
    return [r for r in records if r["status"] == "active"]''',
        hardened_code='''def export_audit_logs(workspace_id: str, query_filter: dict) -> list:
    # 1. Invariant: Enforce immutable workspace_id partition key
    sanitized_filter = {k: v for k, v in query_filter.items() if k != "workspace_id"}
    sanitized_filter["workspace_id"] = workspace_id
    records = AUDIT_DB.find_many(sanitized_filter)
    return [r for r in records if r["status"] == "active"]'''
    )
}
