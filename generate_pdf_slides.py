import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

PDF_PATH = r"C:\Users\Divyanshi\.gemini\antigravity\scratch\axiom\axiom_presentation.pdf"

def build_pdf():
    # 16:9 widescreen style (10 x 5.625 inches or landscape letter: 11 x 8.5)
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=landscape(letter),
        rightMargin=40,
        leftMargin=40,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.HexColor('#0f62fe'),
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#393939'),
        spaceAfter=20
    )

    slide_heading = ParagraphStyle(
        'SlideHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#161616'),
        spaceAfter=12
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#262626'),
        spaceAfter=8
    )

    bold_body_style = ParagraphStyle(
        'BoldBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    card_header = ParagraphStyle(
        'CardHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0f62fe')
    )

    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#8d8d8d')
    )

    story = []

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("AXIOM", title_style))
    story.append(Paragraph("Zero-Trust Invariant & Blast-Radius Firewall for Autonomous AI Dev Partners", ParagraphStyle('Sub', parent=title_style, fontSize=16, leading=20, textColor=colors.HexColor('#161616'))))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Event:</b> IBM Bob 2.0 Hackathon on lablab.ai &nbsp;|&nbsp; <b>Author:</b> Anmol Suwalka", subtitle_style))
    story.append(Paragraph("<b>Repository:</b> github.com/suwalkaanmol/axiom", body_style))
    story.append(Spacer(1, 25))

    banner_data = [
        [
            Paragraph("<b>Target Problem:</b><br/>AI dev tools write code 10x faster, but introduce silent unstated assumptions that bypass human review.", body_style),
            Paragraph("<b>Core Innovation:</b><br/>Adversarial counter-agent that mines ghost invariants, attacks them with fuzzing, and guides IBM Bob self-healing.", body_style),
            Paragraph("<b>Enterprise Value:</b><br/>SOC2/in-toto cryptographic Resilience Passports ensuring safety before deployment.", body_style),
        ]
    ]
    t_banner = Table(banner_data, colWidths=[230, 240, 230])
    t_banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f4f4f4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e0e0e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e0e0e0')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_banner)
    story.append(Spacer(1, 40))
    story.append(Paragraph("Axiom • IBM Bob 2.0 Hackathon • Slide 1/5", footer_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement
    # -------------------------------------------------------------
    story.append(Paragraph("1. The Enterprise Crisis: The AI Assumption Blindspot", slide_heading))
    story.append(Paragraph("When AI dev partners (like IBM Bob) refactor multi-file repositories, code looks clean and passes happy-path tests. However, AI code harbors dangerous unstated assumptions that cause catastrophic production outages.", body_style))
    story.append(Spacer(1, 10))

    prob_data = [
        [
            Paragraph("<b>1. Boundary Neglect</b>", card_header),
            Paragraph("<b>2. Tenant Leakage</b>", card_header),
            Paragraph("<b>3. Concurrency Races</b>", card_header),
            Paragraph("<b>4. Idempotency Gap</b>", card_header)
        ],
        [
            Paragraph("AI assumes numbers/quantities are always positive (>0). Negative amounts cause infinite balance duplication exploits.", body_style),
            Paragraph("AI omits organizational workspace checks, allowing cross-tenant data/fund contamination between clients.", body_style),
            Paragraph("Non-atomic read-modify-write mutations collapse under burst traffic, resulting in double-spending.", body_style),
            Paragraph("Missing replay token deduplication causes network retries to execute financial transactions repeatedly.", body_style)
        ]
    ]
    t_prob = Table(prob_data, colWidths=[175, 175, 175, 175])
    t_prob.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0e0e0')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#fafafa')),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#d0d0d0')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_prob)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>The Human Reviewer Paralysis:</b> Reviewers cannot audit 500-line multi-file AI pull requests for implicit edge-case contracts. They rubber-stamp PRs, allowing fragile code into production.", body_style))
    story.append(Spacer(1, 45))
    story.append(Paragraph("Axiom • IBM Bob 2.0 Hackathon • Slide 2/5", footer_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 3: The Axiom Solution & Architecture
    # -------------------------------------------------------------
    story.append(Paragraph("2. The Solution: Zero-Trust Invariant & Blast-Radius Engine", slide_heading))
    story.append(Paragraph("Axiom acts as an autonomous adversarial auditor that sits directly in the CI/CD pipeline, breaking the circular confirmation bias of AI testing AI.", body_style))
    story.append(Spacer(1, 10))

    sol_data = [
        [
            Paragraph("<b>Pipeline Stage</b>", card_header),
            Paragraph("<b>Axiom Autonomous Action</b>", card_header),
            Paragraph("<b>Technical Impact</b>", card_header)
        ],
        [
            Paragraph("<b>1. Invariant Mining</b>", bold_body_style),
            Paragraph("Inspects AST & semantic diff to extract unstated assumptions (boundary, tenant isolation, concurrency).", body_style),
            Paragraph("Exposes hidden assumptions before code execution.", body_style)
        ],
        [
            Paragraph("<b>2. Adversarial Fuzzing</b>", bold_body_style),
            Paragraph("Synthesizes property-based adversarial pytest suites to deliberately break extracted invariants.", body_style),
            Paragraph("Proves vulnerabilities on camera with reproducible stacktraces.", body_style)
        ],
        [
            Paragraph("<b>3. Blast Radius Map</b>", bold_body_style),
            Paragraph("Interactive system topology mapping downstream PostgreSQL databases, Stripe APIs, and Kafka streams.", body_style),
            Paragraph("Immediate visual risk assessment (Risk Score 88/100).", body_style)
        ],
        [
            Paragraph("<b>4. Self-Healing with Bob</b>", bold_body_style),
            Paragraph("Feeds failure stacktraces back to IBM Bob to synthesize zero-trust hardened patches.", body_style),
            Paragraph("Automated remediation loop (Risk drops to 12/100).", body_style)
        ],
        [
            Paragraph("<b>5. Resilience Passport</b>", bold_body_style),
            Paragraph("Issues in-toto / DSSE cryptographic attestation hash and verified GitHub PR badge.", body_style),
            Paragraph("Audit-ready compliance for enterprise SOC2 standards.", body_style)
        ]
    ]
    t_sol = Table(sol_data, colWidths=[160, 360, 180])
    t_sol.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f62fe')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#ffffff')),
    ]))
    story.append(t_sol)
    story.append(Spacer(1, 20))
    story.append(Paragraph("Axiom • IBM Bob 2.0 Hackathon • Slide 3/5", footer_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 4: Live Demo Walkthrough
    # -------------------------------------------------------------
    story.append(Paragraph("3. Live Demonstration: FinTech Wallet Transfer", slide_heading))
    story.append(Paragraph("Axiom in action against a real-world financial transaction service written by IBM Bob.", body_style))
    story.append(Spacer(1, 10))

    demo_data = [
        [
            Paragraph("<b>Step 1: AI Code Generated</b>", card_header),
            Paragraph("<b>Step 2: Adversarial Attack</b>", card_header),
            Paragraph("<b>Step 3: IBM Bob Remediates</b>", card_header)
        ],
        [
            Paragraph("IBM Bob generates <code>transfer_funds()</code>. Happy path unit tests pass (100% green).<br/><br/><b>Axiom Alert:</b> 4 Ghost Invariants flagged. Downstream PostgreSQL database marked as Critical Blast Radius (Risk: 88).", body_style),
            Paragraph("User clicks <code>EXECUTE ADVERSARIAL FUZZ</code>.<br/><br/><b>Result: 3 FAILED / 0 PASSED</b>.<br/>Terminal catches credit duplication exploit: passing amount = -500 artificially incremented sender wallet balance!", body_style),
            Paragraph("User clicks <code>TRIGGER IBM BOB AUTO-PATCH</code>.<br/><br/>Bob enforces zero-trust bounds and tenant checks.<br/><br/><b>Result: 3 PASSED / 0 FAILED</b>.<br/>Topology turns green, Risk drops to 12/100.", body_style)
        ]
    ]
    t_demo = Table(demo_data, colWidths=[230, 240, 230])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#262626')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#d0d0d0')),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#fcfcfc')),
    ]))
    story.append(t_demo)
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>Key Takeaway:</b> Axiom provides definitive mathematical and empirical proof of code safety rather than superficial text summaries.", body_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Axiom • IBM Bob 2.0 Hackathon • Slide 4/5", footer_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 5: Technology Stack & Why Axiom Wins
    # -------------------------------------------------------------
    story.append(Paragraph("4. Technical Execution & Enterprise Value", slide_heading))
    story.append(Paragraph("Axiom was built from the ground up for the IBM ecosystem to solve the biggest bottleneck to autonomous enterprise adoption.", body_style))
    story.append(Spacer(1, 10))

    final_data = [
        [
            Paragraph("<b>Architecture & Tech Stack</b>", card_header),
            Paragraph("<b>Why Axiom Stands Out to Judges</b>", card_header)
        ],
        [
            Paragraph("• <b>Backend:</b> Python 3.14, FastAPI, AST Analysis, pytest subprocess sandbox<br/>• <b>Frontend:</b> React 18, Tailwind CSS, Vite, dynamic topology node graph<br/>• <b>AI Partner:</b> IBM Bob 2.0 / watsonx for code synthesis and self-healing loop<br/>• <b>Attestation:</b> in-toto / DSSE cryptographic SHA-256 signature generator<br/>• <b>Open Source:</b> Public GitHub repository with 1-click launcher and verified unit tests", body_style),
            Paragraph("• <b>Not a Toy Chatbot:</b> 90% of competitors build chat assistants. Axiom solves the hard enterprise problem: automated code verification.<br/>• <b>High Visual Wow-Factor:</b> Interactive topology graph and live pytest execution terminal give judges a thrilling 2-minute demo.<br/>• <b>IBM Synergy:</b> Elevates IBM Bob from an experimental tool into a trusted, enterprise-ready dev partner.<br/>• <b>Enterprise Compliance:</b> Delivers audit-ready provenance and resilience passports for enterprise CTOs.", body_style)
        ]
    ]
    t_final = Table(final_data, colWidths=[350, 350])
    t_final.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f62fe')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#d0d0d0')),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#ffffff')),
    ]))
    story.append(t_final)
    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>Live Repository:</b> https://github.com/suwalkaanmol/axiom &nbsp;|&nbsp; <b>Developer:</b> Anmol Suwalka", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Axiom • IBM Bob 2.0 Hackathon • Slide 5/5", footer_style))

    doc.build(story)
    print("PDF build successful at:", PDF_PATH)

if __name__ == '__main__':
    build_pdf()
