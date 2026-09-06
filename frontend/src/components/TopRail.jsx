import React from "react";
import { ShieldCheck, Cpu, HardDrive, Radio, UserCheck } from "lucide-react";

export default function TopRail({ networkStatus, activePersona, onSelectPersona }) {
  const personas = [
    { id: "eng_rahul", name: "Rahul Verma", role: "Process Eng.", clearance: "INTERNAL", level: 1, color: "#2F818E" },
    { id: "officer_priya", name: "Priya Nair", role: "Reliability Lead", clearance: "CONFIDENTIAL", level: 2, color: "#C2782A" },
    { id: "cgm_sharma", name: "Dr. V.K. Sharma", role: "Chief Gen. Mgr", clearance: "SECRET", level: 3, color: "#A83838" }
  ];

  return (
    <header style={{
      height: "44px",
      backgroundColor: "var(--console-steel)",
      borderBottom: "1px solid var(--grid-boundary)",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0 14px",
      fontSize: "12px"
    }}>
      {/* System Nameplate */}
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        <div style={{
          backgroundColor: "#16191E",
          border: "1px solid var(--grid-boundary)",
          padding: "3px 7px",
          display: "flex",
          alignItems: "center",
          gap: "6px",
          color: "var(--spec-white)",
          fontWeight: 600,
          letterSpacing: "0.04em"
        }}>
          <span style={{ color: "var(--verification-cyan)" }}>[AGY-ONPREM]</span>
          <span>SOVEREIGN WORKBENCH // IOCL UNIT-01</span>
        </div>
        
        <div className="mono" style={{ color: "var(--subsystem-muted)", fontSize: "11px", display: "flex", alignItems: "center", gap: "6px" }}>
          <Cpu size={12} color="var(--subsystem-muted)" />
          <span>NVIDIA RTX 4090 (24GB) // VRAM: 14.2 GB</span>
        </div>
      </div>

      {/* Live Air-Gap & Sockets Telemetry */}
      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <div className="mono" style={{
          display: "flex",
          alignItems: "center",
          gap: "7px",
          backgroundColor: "#16191E",
          border: "1px solid var(--verification-cyan)",
          padding: "3px 9px",
          color: "var(--verification-cyan)",
          fontSize: "11px",
          fontWeight: 600
        }}>
          <span style={{
            width: "7px",
            height: "7px",
            borderRadius: "50%",
            backgroundColor: "var(--verification-cyan)",
            boxShadow: "0 0 6px var(--verification-cyan)",
            display: "inline-block"
          }} />
          <span>AIR-GAP INTEGRITY: PROVABLY ZERO-EGRESS (0 WAN PACKETS)</span>
        </div>

        <div className="mono" style={{ color: "var(--subsystem-muted)", fontSize: "11px" }}>
          <span>PORT: 8000</span> | <span>LOCAL SOCKETS: {networkStatus?.active_sockets_monitored || 4}</span>
        </div>
      </div>

      {/* Persona / Clearance Selector */}
      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <span style={{ color: "var(--subsystem-muted)", fontSize: "11px" }}>OPERATOR:</span>
        <div style={{ display: "flex", border: "1px solid var(--grid-boundary)" }}>
          {personas.map(p => {
            const isSelected = activePersona.id === p.id;
            return (
              <button
                key={p.id}
                onClick={() => onSelectPersona(p)}
                style={{
                  padding: "4px 9px",
                  fontSize: "11px",
                  fontWeight: isSelected ? 600 : 400,
                  backgroundColor: isSelected ? "#1C1F24" : "transparent",
                  color: isSelected ? "var(--spec-white)" : "var(--subsystem-muted)",
                  borderRight: "1px solid var(--grid-boundary)",
                  display: "flex",
                  alignItems: "center",
                  gap: "5px"
                }}
              >
                <span style={{
                  width: "6px",
                  height: "6px",
                  backgroundColor: p.color,
                  display: "inline-block"
                }} />
                <span>{p.name.split(" ")[0]}</span>
                <span className="mono" style={{ fontSize: "10px", color: p.color }}>[{p.clearance.slice(0, 4)}]</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}
