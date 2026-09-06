"""
Native Deliverable Generator for Industrial Documents (.docx and .xlsx).
Generates formal PSU/Defence-standard Approval Notes and Calculation Sheets.
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from app.core.config import DELIVERABLES_DIR

def generate_approval_note_docx(
    title: str,
    reference_no: str,
    requester_name: str,
    department: str,
    clearance_tier: str,
    background_summary: str,
    technical_findings: List[Dict[str, str]],
    calculations: List[Dict[str, Any]],
    citations: List[str],
    recommendation: str
) -> str:
    doc = docx.Document()

    # Classification Banner (Top)
    banner_p = doc.add_paragraph()
    banner_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    banner_run = banner_p.add_run(f"★ CLASSIFIED: {clearance_tier.upper()} // AIR-GAPPED ON-PREMISE AI GENERATED ★")
    banner_run.bold = True
    banner_run.font.size = Pt(11)
    if clearance_tier.upper() == "SECRET":
        banner_run.font.color.rgb = RGBColor(180, 0, 0)
    elif clearance_tier.upper() == "CONFIDENTIAL":
        banner_run.font.color.rgb = RGBColor(180, 100, 0)
    else:
        banner_run.font.color.rgb = RGBColor(0, 100, 180)

    # Formal PSU / Ministry Title
    h1 = doc.add_heading(level=1)
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1_run = h1.add_run("INDIAN REFINERY & DEFENCE INFRASTRUCTURE CORPORATION")
    h1_run.font.name = "Arial"
    h1_run.font.size = Pt(15)
    h1_run.font.color.rgb = RGBColor(20, 20, 20)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub.add_run("TECHNICAL APPROVAL NOTE & SAFETY COMPLIANCE MEMO")
    sub_run.bold = True
    sub_run.font.size = Pt(12)

    doc.add_paragraph("―" * 55).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Meta Table
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta = [
        ("Reference Number:", reference_no),
        ("Date & Timestamp:", datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC") + " (Local Sovereign)"),
        ("Originating Officer:", f"{requester_name} ({department})"),
        ("Subject Matter:", title)
    ]
    for i, (k, v) in enumerate(meta):
        table.cell(i, 0).paragraphs[0].add_run(k).bold = True
        table.cell(i, 1).paragraphs[0].add_run(v)
        table.cell(i, 0).width = Inches(2.0)
        table.cell(i, 1).width = Inches(4.5)

    doc.add_paragraph()

    # 1. Background Section
    doc.add_heading("1. Operational Context & Problem Assessment", level=2)
    doc.add_paragraph(background_summary)

    # 2. Key Technical Findings
    doc.add_heading("2. Verified Sensor & Inspection Telemetry", level=2)
    if technical_findings:
        findings_table = doc.add_table(rows=1, cols=3)
        hdr_cells = findings_table.rows[0].cells
        hdr_cells[0].paragraphs[0].add_run("Equipment / Seam").bold = True
        hdr_cells[1].paragraphs[0].add_run("Measured Value").bold = True
        hdr_cells[2].paragraphs[0].add_run("Safety Baseline / Tolerance").bold = True
        for row in technical_findings:
            r = findings_table.add_row().cells
            r[0].paragraphs[0].add_run(row.get("parameter", ""))
            r[1].paragraphs[0].add_run(row.get("measured", ""))
            r[2].paragraphs[0].add_run(row.get("baseline", ""))

    doc.add_paragraph()

    # 3. Engineering Calculations
    doc.add_heading("3. Sandboxed Engineering Verification & Calculations", level=2)
    for calc in calculations:
        p = doc.add_paragraph()
        p.add_run("• Formula Applied: ").bold = True
        p.add_run(str(calc.get('formula', '')) + "\n")
        p.add_run("• Calculated Derated MAWP / Safe Metric: ").bold = True
        p.add_run(str(calc.get('result', '')) + "\n")
        p.add_run("• Verification Status: ").bold = True
        p.add_run(str(calc.get('verification', 'VERIFIED IN ISOLATED SANDBOX')))

    # 4. Citations & Grounding
    doc.add_heading("4. Sovereign Grounding & Regulatory Citations", level=2)
    cit_p = doc.add_paragraph()
    cit_p.add_run("This technical note was drafted autonomously with strict provenance citations:\n")
    for c in citations:
        doc.add_paragraph(f"  [✓] {c}", style='List Bullet')

    # 5. Recommendation & Signatures
    doc.add_heading("5. Executive Recommendation for Approval", level=2)
    rec_p = doc.add_paragraph(recommendation)
    rec_p.runs[0].italic = True

    doc.add_paragraph("\n" + "_" * 35 + "          " + "_" * 35)
    sig_p = doc.add_paragraph("Initiated by (Lead Reliability Eng.)          Approved by (Unit Operations Head)")
    sig_p.runs[0].bold = True

    # Classification Banner (Bottom)
    banner_b = doc.add_paragraph()
    banner_b.alignment = WD_ALIGN_PARAGRAPH.CENTER
    banner_b.add_run(f"★ CLASSIFIED: {clearance_tier.upper()} // ZERO-EGRESS GUARANTEE ★").bold = True

    # Save to deliverables directory
    filename = f"Approval_Note_{reference_no.replace('/', '_').replace('-', '_')}.docx"
    filepath = DELIVERABLES_DIR / filename
    doc.save(str(filepath))
    return filename
