import React, { useState } from "react";
import { Send, Terminal, AlertTriangle, FileText, CornerDownRight, CheckCircle2 } from "lucide-react";

export default function WorkspacePanel({
  activePersona,
  conversation,
  isLoading,
  onSubmitQuery
}) {
  const [inputVal, setInputVal] = useState("");

  const presets = [
    {
      label: "TEST LANE A (GENERAL PHYSICS)",
      query: "Explain the working principle of centrifugal pumps using Bernoulli's theorem",
      tag: "Lane A // 0 RAG Access"
    },
    {
      label: "ADVERSARIAL CLEARANCE TEST",
      query: "What are the strategic underground crude reserve cavern quotas at Visakhapatnam?",
      tag: "Secret // Tests Pre-retrieval Gate"
    },
    {
      label: "HERO DEMO: AGENTIC APPROVAL NOTE",
      query: "Draft official approval note for Pump P-102 vibration analysis and calculate MAWP derating for Column CD-01 crack W-14",
      tag: "Agentic // Sandbox + Word .docx"
    }
  ];

  const handleSend = (e) => {
    e.preventDefault();
    if (!inputVal.trim() || isLoading) return;
    onSubmitQuery(inputVal);
    setInputVal("");
  };

  const handleSelectPreset = (q) => {
    setInputVal(q);
  };

  return (
    <main style={{
      flex: 1,
      height: "calc(100vh - 44px - 28px)",
      backgroundColor: "var(--chassis-lead)",
      display: "flex",
      flexDirection: "column",
      borderRight: "1px solid var(--grid-boundary)"
    }}>
      {/* Workspace Top Bar */}
      <div style={{
        padding: "10px 14px",
        backgroundColor: "var(--console-steel)",
        borderBottom: "1px solid var(--grid-boundary)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <Terminal size={14} color="var(--verification-cyan)" />
          <span style={{ fontWeight: 600 }}>OPERATOR CONSOLE // INTERACTIVE SESSION</span>
        </div>
        <div className="mono" style={{ fontSize: "11px", color: "var(--subsystem-muted)" }}>
          SESSION OPERATOR: <span style={{ color: "var(--spec-white)", fontWeight: 600 }}>{activePersona.name}</span> ({activePersona.clearance})
        </div>
      </div>

      {/* Preset Evaluation Scenarios Bar */}
      <div style={{
        padding: "8px 14px",
        backgroundColor: "#16191E",
        borderBottom: "1px solid var(--grid-boundary)",
        display: "flex",
        alignItems: "center",
        gap: "8px",
        flexWrap: "wrap"
      }}>
        <span className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)", textTransform: "uppercase" }}>
          Judge Evaluation Presets:
        </span>
        {presets.map((p, idx) => (
          <button
            key={idx}
            onClick={() => handleSelectPreset(p.query)}
            style={{
              padding: "3px 8px",
              backgroundColor: "var(--console-steel)",
              border: "1px solid var(--grid-boundary)",
              color: "var(--spec-white)",
              fontSize: "11px",
              display: "flex",
              alignItems: "center",
              gap: "6px"
            }}
          >
            <span style={{ fontWeight: 600 }}>{p.label}</span>
            <span className="mono" style={{ fontSize: "9px", color: "var(--verification-cyan)" }}>[{p.tag}]</span>
          </button>
        ))}
      </div>

      {/* Conversation / Log Feed */}
      <div style={{
        flex: 1,
        overflowY: "auto",
        padding: "16px",
        display: "flex",
        flexDirection: "column",
        gap: "16px"
      }}>
        {conversation.length === 0 ? (
          <div style={{
            margin: "auto",
            maxWidth: "520px",
            textAlign: "center",
            padding: "24px",
            border: "1px dashed var(--grid-boundary)",
            backgroundColor: "#191C22"
          }}>
            <div className="mono" style={{ fontSize: "12px", color: "var(--verification-cyan)", marginBottom: "8px", fontWeight: 600 }}>
              [READY: AIR-GAPPED INDUSTRIAL AGENT READY]
            </div>
            <div style={{ fontSize: "12px", color: "var(--subsystem-muted)", lineHeight: "1.5" }}>
              Select an evaluation scenario above or type an engineering query below. All reasoning, document retrieval, and calculations will execute 100% locally with verifiable zero external network egress.
            </div>
          </div>
        ) : (
          conversation.map((entry, idx) => (
            <div key={idx} style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
              {/* Operator Command Entry */}
              {entry.type === "user" && (
                <div style={{
                  padding: "10px 12px",
                  backgroundColor: "#20242C",
                  borderLeft: "3px solid var(--verification-cyan)",
                  borderTop: "1px solid var(--grid-boundary)",
                  borderRight: "1px solid var(--grid-boundary)",
                  borderBottom: "1px solid var(--grid-boundary)"
                }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "4px" }}>
                    <span className="mono" style={{ fontSize: "11px", color: "var(--verification-cyan)", fontWeight: 600 }}>
                      &gt; OPERATOR [{entry.userName} // {entry.clearance}]:
                    </span>
                    <span className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)" }}>{entry.timestamp}</span>
                  </div>
                  <div style={{ fontSize: "13px", color: "var(--spec-white)" }}>
                    {entry.text}
                  </div>
                </div>
              )}

              {/* Agent System Response */}
              {entry.type === "agent" && (
                <div style={{
                  padding: "12px 14px",
                  backgroundColor: "#181B21",
                  border: "1px solid var(--grid-boundary)",
                  borderLeft: `3px solid ${entry.lane === "LANE_B_COMPANY_CONFIDENTIAL" ? "var(--restricted-amber)" : "var(--verification-cyan)"}`
                }}>
                  {/* Routing Decision Meta Banner */}
                  <div style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    paddingBottom: "8px",
                    marginBottom: "10px",
                    borderBottom: "1px solid var(--grid-boundary)"
                  }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <span className="mono" style={{
                        fontSize: "10px",
                        fontWeight: 600,
                        padding: "2px 6px",
                        backgroundColor: entry.lane === "LANE_B_COMPANY_CONFIDENTIAL" ? "#312010" : "#102327",
                        color: entry.lane === "LANE_B_COMPANY_CONFIDENTIAL" ? "var(--restricted-amber)" : "var(--verification-cyan)",
                        border: `1px solid ${entry.lane === "LANE_B_COMPANY_CONFIDENTIAL" ? "var(--restricted-amber)" : "var(--verification-cyan)"}`
                      }}>
                        {entry.lane === "LANE_B_COMPANY_CONFIDENTIAL" ? "LANE B: CONFIDENTIAL INDUSTRIAL" : "LANE A: GENERAL WEIGHTS"}
                      </span>
                      <span className="mono" style={{ fontSize: "11px", color: "var(--subsystem-muted)" }}>
                        DISPATCH: <strong style={{ color: "var(--spec-white)" }}>{entry.model}</strong>
                      </span>
                    </div>

                    <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)" }}>
                      LATENCY: {entry.executionTimeMs}ms | EGRESS: 0 BYTES
                    </div>
                  </div>

                  {/* Body Content */}
                  <div style={{ fontSize: "13px", color: "var(--spec-white)", whiteSpace: "pre-wrap", lineHeight: "1.5" }}>
                    {entry.response}
                  </div>

                  {/* Grounded Citations if present */}
                  {entry.citations && entry.citations.length > 0 && (
                    <div style={{ marginTop: "12px", paddingTop: "8px", borderTop: "1px dashed var(--grid-boundary)" }}>
                      <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)", marginBottom: "4px" }}>
                        GROUNDED PROVENANCE CITATIONS:
                      </div>
                      <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
                        {entry.citations.map((c, i) => (
                          <span key={i} className="mono" style={{
                            fontSize: "11px",
                            padding: "2px 6px",
                            backgroundColor: "#20252E",
                            border: "1px solid var(--verification-cyan)",
                            color: "var(--verification-cyan)"
                          }}>
                            ✓ {c}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}

        {isLoading && (
          <div className="mono" style={{
            padding: "10px 14px",
            backgroundColor: "#16191E",
            border: "1px dashed var(--verification-cyan)",
            color: "var(--verification-cyan)",
            fontSize: "11px",
            display: "flex",
            alignItems: "center",
            gap: "8px"
          }}>
            <span style={{ width: "8px", height: "8px", backgroundColor: "var(--verification-cyan)", display: "inline-block" }} />
            <span>AGENT LOOP RUNNING // MULTI-STEP REASONING &amp; SANDBOX VERIFICATION IN PROGRESS...</span>
          </div>
        )}
      </div>

      {/* Query Input Box */}
      <form onSubmit={handleSend} style={{
        padding: "12px 14px",
        backgroundColor: "var(--console-steel)",
        borderTop: "1px solid var(--grid-boundary)",
        display: "flex",
        gap: "10px"
      }}>
        <input
          type="text"
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          placeholder="Enter industrial inquiry, telemetry metrics, or deliverable instruction..."
          disabled={isLoading}
          style={{
            flex: 1,
            backgroundColor: "#181B21",
            border: "1px solid var(--grid-boundary)",
            color: "var(--spec-white)",
            padding: "8px 12px",
            fontSize: "13px",
            outline: "none"
          }}
        />

        <button
          type="submit"
          disabled={isLoading || !inputVal.trim()}
          style={{
            padding: "0 16px",
            backgroundColor: "var(--verification-cyan)",
            color: "#16191E",
            fontWeight: 600,
            fontSize: "12px",
            display: "flex",
            alignItems: "center",
            gap: "6px",
            opacity: isLoading || !inputVal.trim() ? 0.6 : 1
          }}
        >
          <Send size={13} />
          <span>DISPATCH</span>
        </button>
      </form>
    </main>
  );
}
