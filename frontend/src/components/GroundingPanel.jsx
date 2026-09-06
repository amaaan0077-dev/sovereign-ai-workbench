import React from "react";
import { Database, Lock, Unlock, HardDrive, Shield } from "lucide-react";

export default function GroundingPanel({ documents, activePersona, models }) {
  const clearanceLevel = activePersona.level;

  return (
    <aside style={{
      width: "320px",
      height: "calc(100vh - 44px - 28px)",
      backgroundColor: "var(--console-steel)",
      borderRight: "1px solid var(--grid-boundary)",
      display: "flex",
      flexDirection: "column",
      fontSize: "12px"
    }}>
      {/* Panel Header */}
      <div style={{
        padding: "10px 12px",
        borderBottom: "1px solid var(--grid-boundary)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        backgroundColor: "#1F232A"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "7px", fontWeight: 600 }}>
          <Database size={13} color="var(--verification-cyan)" />
          <span>SOVEREIGN VECTOR REPOSITORY</span>
        </div>
        <span className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)" }}>QDRANT LOCAL</span>
      </div>

      {/* Clearance Filter Notice */}
      <div style={{
        padding: "8px 12px",
        backgroundColor: "#171A20",
        borderBottom: "1px solid var(--grid-boundary)",
        fontSize: "11px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between"
      }}>
        <span style={{ color: "var(--subsystem-muted)" }}>GATE ENFORCEMENT:</span>
        <span className="mono" style={{
          color: activePersona.color,
          fontWeight: 600,
          border: `1px solid ${activePersona.color}`,
          padding: "1px 6px"
        }}>
          {activePersona.clearance} (LVL {activePersona.level})
        </span>
      </div>

      {/* Document Chunks List */}
      <div style={{ flex: 1, overflowY: "auto", padding: "10px" }}>
        <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)", marginBottom: "8px", textTransform: "uppercase" }}>
          Indexed Technical Manuals & Blueprints ({documents.length})
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          {documents.map((doc, idx) => {
            const isAccessible = doc.clearance_level <= clearanceLevel;
            const badgeColor = doc.clearance_level === 3 ? "var(--restricted-red)" : doc.clearance_level === 2 ? "var(--restricted-amber)" : "var(--verification-cyan)";

            return (
              <div key={idx} style={{
                backgroundColor: isAccessible ? "#1C2027" : "#191B20",
                border: `1px solid ${isAccessible ? "var(--grid-boundary)" : "#2A2E38"}`,
                padding: "8px 10px",
                opacity: isAccessible ? 1 : 0.65
              }}>
                <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: "4px" }}>
                  <span className="mono" style={{ fontSize: "11px", fontWeight: 600, color: isAccessible ? "var(--spec-white)" : "var(--subsystem-muted)" }}>
                    {doc.doc_id}
                  </span>
                  <span className="mono" style={{
                    fontSize: "9px",
                    fontWeight: 600,
                    padding: "1px 5px",
                    color: badgeColor,
                    border: `1px solid ${badgeColor}`
                  }}>
                    {doc.clearance_tier}
                  </span>
                </div>

                <div style={{ fontSize: "11px", color: "var(--subsystem-muted)", marginBottom: "6px", lineHeight: "1.3" }}>
                  {doc.title}
                </div>

                <div style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  fontSize: "10px",
                  borderTop: "1px dashed var(--grid-boundary)",
                  paddingTop: "5px"
                }}>
                  <span className="mono" style={{ color: "var(--subsystem-muted)" }}>{doc.department}</span>
                  <span className="mono" style={{ color: isAccessible ? "var(--verification-cyan)" : "var(--restricted-red)", display: "flex", alignItems: "center", gap: "3px" }}>
                    {isAccessible ? <Unlock size={10} /> : <Lock size={10} />}
                    {isAccessible ? "ACCESSIBLE" : "GATE BLOCKED"}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Model Registry Footer Deck */}
      <div style={{
        borderTop: "1px solid var(--grid-boundary)",
        padding: "10px 12px",
        backgroundColor: "#16191E"
      }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "8px" }}>
          <span style={{ fontSize: "11px", fontWeight: 600, color: "var(--spec-white)" }}>LOCAL MODEL REGISTRY</span>
          <span className="mono" style={{ fontSize: "10px", color: "var(--verification-cyan)" }}>ON-PREM vLLM</span>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "5px", fontSize: "11px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", color: "var(--subsystem-muted)" }}>
            <span>Qwen2.5-Coder (Python Calc):</span>
            <span className="mono" style={{ color: "var(--spec-white)" }}>5.5 GB [RESIDENT]</span>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", color: "var(--subsystem-muted)" }}>
            <span>Qwen2.5-VL (OCR & P&ID):</span>
            <span className="mono" style={{ color: "var(--verification-cyan)" }}>6.0 GB [HOT-SWAP]</span>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", color: "var(--subsystem-muted)" }}>
            <span>Qwen2.5-14B (Drafting):</span>
            <span className="mono" style={{ color: "var(--spec-white)" }}>9.5 GB [RESIDENT]</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
