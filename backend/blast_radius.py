from models import BlastRadiusGraph, BlastRadiusNode, BlastRadiusEdge

def generate_blast_radius(scenario_id: str, status_mode: str = "vulnerable") -> BlastRadiusGraph:
    """
    Generates service topology and blast radius graph for the AI commit.
    status_mode: 'vulnerable' (red/impacted) or 'hardened' (green/safe)
    """
    if scenario_id == "billing_transfer":
        nodes = [
            BlastRadiusNode(
                id="client_gateway",
                label="API Gateway (Kong/Nginx)",
                type="client",
                status="monitored",
                details="Ingress route /api/v1/wallets/transfer"
            ),
            BlastRadiusNode(
                id="billing_service",
                label="Billing Service (AI Target)",
                type="service",
                status="critical" if status_mode == "vulnerable" else "safe",
                details="services/billing_service.py - Commit by IBM Bob"
            ),
            BlastRadiusNode(
                id="postgres_wallets",
                label="PostgreSQL (Wallets Ledger)",
                type="database",
                status="impacted" if status_mode == "vulnerable" else "safe",
                details="Table: user_balances (Direct mutation vulnerability)"
            ),
            BlastRadiusNode(
                id="stripe_gateway",
                label="Stripe Payments API",
                type="external_api",
                status="impacted" if status_mode == "vulnerable" else "safe",
                details="Downstream settlement webhook reconciliation"
            ),
            BlastRadiusNode(
                id="kafka_events",
                label="Kafka Event Stream",
                type="queue",
                status="monitored",
                details="Topic: billing.transaction.settled (Audit logs)"
            ),
            BlastRadiusNode(
                id="notification_svc",
                label="Notification Service",
                type="service",
                status="monitored",
                details="Customer receipt email / SMS dispatcher"
            )
        ]

        edges = [
            BlastRadiusEdge(
                id="e1",
                source="client_gateway",
                target="billing_service",
                label="POST /transfer",
                risk_level="high" if status_mode == "vulnerable" else "low"
            ),
            BlastRadiusEdge(
                id="e2",
                source="billing_service",
                target="postgres_wallets",
                label="UPDATE balance",
                risk_level="high" if status_mode == "vulnerable" else "low"
            ),
            BlastRadiusEdge(
                id="e3",
                source="billing_service",
                target="stripe_gateway",
                label="Sync Settlement",
                risk_level="medium" if status_mode == "vulnerable" else "low"
            ),
            BlastRadiusEdge(
                id="e4",
                source="billing_service",
                target="kafka_events",
                label="Emit TransactionEvent",
                risk_level="low"
            ),
            BlastRadiusEdge(
                id="e5",
                source="kafka_events",
                target="notification_svc",
                label="Consume Event",
                risk_level="low"
            )
        ]

        risk_score = 88 if status_mode == "vulnerable" else 12
        summary = (
            "CRITICAL: 2 direct dependency layers exposed to unvalidated state mutation. Database ledger and Stripe settlement at risk of desynchronization."
            if status_mode == "vulnerable"
            else "VERIFIED: Invariants enforced. Blast radius contained. All downstream data contracts secured."
        )

        return BlastRadiusGraph(
            nodes=nodes,
            edges=edges,
            risk_score=risk_score,
            impact_summary=summary
        )

    # Fallback default graph for other scenarios
    nodes = [
        BlastRadiusNode(id="api", label="API Gateway", type="client", status="monitored", details="Ingress Traffic"),
        BlastRadiusNode(id="target", label="Target Service", type="service", status="critical" if status_mode == "vulnerable" else "safe", details="AI Commit Target"),
        BlastRadiusNode(id="db", label="Primary Datastore", type="database", status="impacted" if status_mode == "vulnerable" else "safe", details="State Mutation Target"),
        BlastRadiusNode(id="bus", label="Message Broker", type="queue", status="monitored", details="Async Event Bus")
    ]
    edges = [
        BlastRadiusEdge(id="e1", source="api", target="target", label="HTTP", risk_level="high" if status_mode == "vulnerable" else "low"),
        BlastRadiusEdge(id="e2", source="target", target="db", label="Write", risk_level="high" if status_mode == "vulnerable" else "low"),
        BlastRadiusEdge(id="e3", source="target", target="bus", label="Publish", risk_level="low")
    ]
    return BlastRadiusGraph(
        nodes=nodes,
        edges=edges,
        risk_score=75 if status_mode == "vulnerable" else 10,
        impact_summary="Downstream database mutations susceptible to unhandled boundary payloads." if status_mode == "vulnerable" else "Invariants verified. Safe to merge."
    )
