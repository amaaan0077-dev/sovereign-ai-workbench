import React from "react";
import { ShieldCheck, Activity } from "lucide-react";

export default function SystemFooter({ latencyMs, networkStatus }) {
  return (
    <footer style={{
      height: "28px",
      backgroundColor: "var(--console-steel)",
      borderTop: "1px solid var(--grid-boundary)",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0 14px",
      fontSize: "11px",
      color: "var(--subsystem-muted)"
    }} className="mono">
      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <span style={{ color: "var(--verification-cyan)", display: "flex", alignItems: "center", gap: "4px" }}>
          <ShieldCheck size={12} />
          <span>SOVEREIGN MANDATE:</span>
        </span>
        <span>ALL DATA CONFINED TO ON-PREMISE BOUNDARY. TELEMETRY STRICTLY PURGED.</span>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
        <span>ACTIVE PROFILE: BASELINE (SINGLE 24GB GPU)</span>
        <span>LAST DISPATCH: {latencyMs ? `${latencyMs}ms` : "IDLE"}</span>
        <span style={{ color: "var(--verification-cyan)" }}>EGRESS: 0 BYTES [SECURE]</span>
      </div>
    </footer>
  );
}
