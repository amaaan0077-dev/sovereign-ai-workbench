"""
Pre-seeded Industrial Knowledge Base containing authentic PSU & Refinery documents
tagged with Clearance Tiers (INTERNAL, CONFIDENTIAL, SECRET).
"""
from app.core.security import ClearanceTier
from app.rag.vector_store import DocumentChunk, vector_store

SAMPLE_DOCS = [
    # --- TIER 1: INTERNAL ---
    DocumentChunk(
        chunk_id="sop_pump_01",
        doc_id="SOP-PUMP-OVERHAUL-2024",
        title="Centrifugal Pump P-102 Overhaul & Vibration Maintenance Manual",
        clearance_tier=ClearanceTier.INTERNAL,
        department="Refinery Maintenance & Mechanical Engineering",
        page=4,
        content="Centrifugal Pump P-102 operates in Crude Distillation Unit-1. Vibration baseline standard ISO 10816-3: "
                "Normal allowable RMS velocity is <= 4.5 mm/s. Alert limit is 7.1 mm/s. "
                "Immediate shutdown threshold is 11.2 mm/s. Bearing lubrication requires Mobil SHC 630 synthetic oil "
                "replaced every 2,500 operating hours."
    ),
    DocumentChunk(
        chunk_id="sop_pump_02",
        doc_id="SOP-PUMP-OVERHAUL-2024",
        title="Centrifugal Pump P-102 Overhaul & Vibration Maintenance Manual",
        clearance_tier=ClearanceTier.INTERNAL,
        department="Refinery Maintenance & Mechanical Engineering",
        page=11,
        content="Coupling alignment procedure for P-102: Dial gauge radial runout tolerance must not exceed 0.05 mm. "
                "Axial end-play float must be retained within 0.12 mm to prevent impeller thrust bearing fatigue. "
                "Torque motor mounting bolts to 185 Nm."
    ),

    # --- TIER 2: CONFIDENTIAL ---
    DocumentChunk(
        chunk_id="insp_crack_01",
        doc_id="INSPECTION-CRACK-ANALYSIS-UNIT-4",
        title="NDT Ultrasonic Inspection Report - Crude Column CD-01",
        clearance_tier=ClearanceTier.CONFIDENTIAL,
        department="Asset Integrity & Quality Inspection",
        page=2,
        content="Non-Destructive Testing (NDT) report for Crude Distillation Column CD-01 weld seam W-14. "
                "Phased Array Ultrasonic Testing (PAUT) identified an intermittent circumferential crack "
                "measuring 28 mm in length with a depth penetration of 4.2 mm in the heat-affected zone (HAZ). "
                "Material: ASTM A516 Grade 70 carbon steel."
    ),
    DocumentChunk(
        chunk_id="insp_crack_02",
        doc_id="INSPECTION-CRACK-ANALYSIS-UNIT-4",
        title="NDT Ultrasonic Inspection Report - Crude Column CD-01",
        clearance_tier=ClearanceTier.CONFIDENTIAL,
        department="Asset Integrity & Quality Inspection",
        page=5,
        content="Engineering recommendation for CD-01 crack W-14: Column operating pressure must be immediately "
                "derated from design pressure of 18.5 bar down to maximum safe allowable working pressure (MAWP) of 14.8 bar. "
                "Safety factor derating formula: P_safe = P_design * (1 - (crack_depth / wall_thickness * 1.5)). "
                "Emergency weld pad overlay scheduled during next turnaround (Window 3B)."
    ),

    # --- TIER 3: SECRET ---
    DocumentChunk(
        chunk_id="sec_crude_01",
        doc_id="STRATEGIC-CRUDE-RESERVE-ALLOCATION-2026",
        title="Ministry Strategic Petroleum Reserve (ISPRL) Emergency Buffer Directives",
        clearance_tier=ClearanceTier.SECRET,
        department="Strategic Refinery Reserves & Ministry Liaison",
        page=1,
        content="CONFIDENTIAL STRATEGIC DIRECTIVE: National Strategic Petroleum Reserve allocation quotas for Q3/Q4 2026. "
                "Underground rock cavern holding reserves: Visakhapatnam (1.33 MMT), Mangalore (1.50 MMT), and Padur (2.50 MMT). "
                "Mandatory minimum inventory reserve threshold is set at 9.5 days of net domestic crude consumption. "
                "Release authorization strictly governed by Ministry Empowered Committee Order SEC-POL-88."
    ),
    DocumentChunk(
        chunk_id="sec_crude_02",
        doc_id="STRATEGIC-CRUDE-RESERVE-ALLOCATION-2026",
        title="Ministry Strategic Petroleum Reserve (ISPRL) Emergency Buffer Directives",
        clearance_tier=ClearanceTier.SECRET,
        department="Strategic Refinery Reserves & Ministry Liaison",
        page=7,
        content="Pricing hedging mechanisms and emergency swap contracts with GCC suppliers under bilateral sovereign trade. "
                "Emergency swap exchange ratio pegged at Brent benchmark index minus 2.4% discount with guaranteed 48-hour "
                "berthing priority at crude offloading terminals."
    )
]

def seed_sample_documents():
    for doc in SAMPLE_DOCS:
        vector_store.add_chunk(doc)
    print(f"Seeded {len(SAMPLE_DOCS)} industrial documents into Sovereign Vector Store.")
