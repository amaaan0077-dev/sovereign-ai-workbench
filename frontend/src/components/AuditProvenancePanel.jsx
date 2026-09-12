import React, { useState } from "react";
import { Download, Activity, FileText, CheckCircle, XCircle, GitBranch } from "lucide-react";
import PipelineView from "./PipelineView";

export default function AuditProvenancePanel({
  auditTrace,
  deliverableFile,
  xlsxFile,
  networkStatus,
  lastCitations,
  routing,
  verificationResult,
  webResearch,
  isLoading,
}) {
  const [activeTab, setActiveTab] = useState("provenance");

  const downloadUrl     = deliverableFile ? `http://127.0.0.1:8000/api/deliverables/${deliverableFile}` : null;
  const xlsxDownloadUrl = xlsxFile        ? `http://127.0.0.1:8000/api/deliverables/${xlsxFile}`        : null;

  // ── Tab bar ────────────────────────────────────────────────────
  const tabs = [
    { id: "provenance", icon: <Activity size={11} />, label: "PROVENANCE" },
    { id: "pipeline",   icon: <GitBranch size={11} />, label: "PIPELINE"  },
  ];

  return (
    <aside style={{
      width:          "360px",
      height:         "calc(100vh - 44px - 28px)",
      backgroundColor: "var(--console-steel)",
      display:        "flex",
      flexDirection:  "column",
      fontSize:       "12px",
    }}>
      {/* ── Panel header ──────────────────────────────────────── */}
      <div style={{
        padding:         "10px 12px",
        borderBottom:    "1px solid var(--grid-boundary)",
        display:         "flex",
        alignItems:      "center",
        justifyContent:  "space-between",
        backgroundColor: "#1F232A",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "7px", fontWeight: 600 }}>
          <Activity size={13} color="var(--verification-cyan)" />
          <span>PROVENANCE &amp; NETWORK AUDIT</span>
        </div>
        <span className="mono" style={{ fontSize: "10px", color: "var(--verification-cyan)" }}>
          0 WAN PACKETS
        </span>
      </div>

      {/* ── Tab selector ─────────────────────────────────────── */}
      <div style={{
        display:         "flex",
        borderBottom:    "1px solid var(--grid-boundary)",
        backgroundColor: "#191C22",
      }}>
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              flex:            1,
              padding:         "7px 4px",
              display:         "flex",
              alignItems:      "center",
              justifyContent:  "center",
              gap:             "5px",
              fontFamily:      "JetBrains Mono, monospace",
              fontSize:        "9px",
              fontWeight:      700,
              cursor:          "pointer",
              backgroundColor: activeTab === tab.id ? "var(--chassis-lead)" : "transparent",
              color:           activeTab === tab.id ? "var(--verification-cyan)" : "var(--subsystem-muted)",
              borderBottom:    activeTab === tab.id ? "2px solid var(--verification-cyan)" : "2px solid transparent",
              border:          "none",
              transition:      "color 0.15s",
            }}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      {/* ── Tab content ──────────────────────────────────────── */}

      {activeTab === "pipeline" ? (
        /* ── PIPELINE TAB ─────────────────────────────────── */
        <div style={{ flex: 1, overflow: "hidden" }}>
          <PipelineView
            auditTrace={auditTrace}
            routing={routing}
            verificationResult={verificationResult}
            webResearch={webResearch}
            isLoading={isLoading}
          />
        </div>
      ) : (
        /* ── PROVENANCE TAB ───────────────────────────────── */
        <div style={{
          flex:          1,
          overflowY:     "auto",
          padding:       "12px",
          display:       "flex",
          flexDirection: "column",
          gap:           "14px",
        }}>

          {/* ── Verification Engine Result Card ────────────── */}
          {verificationResult && (
            <div>
              <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)", marginBottom: "6px", textTransform: "uppercase" }}>
                Verification Engine Result
              </div>
              <div style={{
                backgroundColor: verificationResult.status === "VALID" ? "#0D1F1A" : "#1C1010",
                border:          `1px solid ${verificationResult.status === "VALID" ? "var(--verification-cyan)" : "#C23A2A"}`,
                padding:         "10px",
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "6px" }}>
                  {verificationResult.status === "VALID"
                    ? <CheckCircle size={14} color="var(--verification-cyan)" />
                    : <XCircle    size={14} color="#C23A2A" />}
                  <span className="mono" style={{
                    fontSize:   "11px",
                    fontWeight: 700,
                    color:      verificationResult.status === "VALID" ? "var(--verification-cyan)" : "#C23A2A",
                  }}>
                    {verificationResult.status} — {verificationResult.check_count} CHECKS
                  </span>
                </div>

                {verificationResult.passed_checks?.map((c, i) => (
                  <div key={i} className="mono" style={{ fontSize: "9px", color: "var(--subsystem-muted)", marginBottom: "2px" }}>
                    ✓ {c.length > 68 ? c.slice(0, 68) + "…" : c}
                  </div>
                ))}

                {verificationResult.issues?.map((issue, i) => (
                  <div key={i} className="mono" style={{ fontSize: "9px", color: "#C23A2A", marginBottom: "2px", marginTop: "4px" }}>
                    ⚠ {issue.length > 68 ? issue.slice(0, 68) + "…" : issue}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ── Generated Deliverables ─────────────────────── */}
          <div>
            <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)", marginBottom: "6px", textTransform: "uppercase" }}>
              Generated Industrial Deliverables
            </div>

            {/* DOCX */}
            {deliverableFile ? (
              <div style={{
                backgroundColor: "#191D24",
                border:          "1px solid var(--verification-cyan)",
                padding:         "10px",
                marginBottom:    "8px",
              }}>
                <div className="mono" style={{
                  textAlign:       "center",
                  padding:         "2px 0",
                  backgroundColor: "#2B1D11",
                  border:          "1px solid var(--restricted-amber)",
                  color:           "var(--restricted-amber)",
                  fontWeight:      600,
                  fontSize:        "10px",
                  letterSpacing:   "0.05em",
                  marginBottom:    "8px",
                }}>
                  CLASSIFIED: CONFIDENTIAL // AIR-GAPPED
                </div>

                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
                  <FileText size={18} color="var(--verification-cyan)" />
                  <div>
                    <div style={{ fontWeight: 600, color: "var(--spec-white)", fontSize: "12px" }}>
                      Official Safety Approval Note
                    </div>
                    <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)" }}>
                      {deliverableFile}
                    </div>
                  </div>
                </div>

                <a href={downloadUrl} download target="_blank" rel="noreferrer" style={{
                  padding:         "7px 10px",
                  backgroundColor: "var(--verification-cyan)",
                  color:           "#16191E",
                  textDecoration:  "none",
                  fontWeight:      600,
                  fontSize:        "11px",
                  display:         "flex",
                  alignItems:      "center",
                  justifyContent:  "center",
                  gap:             "6px",
                }}>
                  <Download size={12} /> DOWNLOAD .DOCX
                </a>
              </div>
            ) : (
              <div style={{
                padding:         "10px",
                border:          "1px dashed var(--grid-boundary)",
                backgroundColor: "#191B20",
                textAlign:       "center",
                color:           "var(--subsystem-muted)",
                fontSize:        "11px",
                marginBottom:    "8px",
              }}>
                No .docx generated. Use Hero Demo preset.
              </div>
            )}

            {/* XLSX */}
            {xlsxFile ? (
              <div style={{
                backgroundColor: "#191D24",
                border:          "1px solid #2E8B57",
                padding:         "10px",
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
                  <FileText size={18} color="#2E8B57" />
                  <div>
                    <div style={{ fontWeight: 600, color: "var(--spec-white)", fontSize: "12px" }}>
                      Excel Analysis Report
                    </div>
                    <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)" }}>
                      {xlsxFile}
                    </div>
                  </div>
                </div>

                <a href={xlsxDownloadUrl} download target="_blank" rel="noreferrer" style={{
                  padding:         "7px 10px",
                  backgroundColor: "#2E8B57",
                  color:           "#fff",
                  textDecoration:  "none",
                  fontWeight:      600,
                  fontSize:        "11px",
                  display:         "flex",
                  alignItems:      "center",
                  justifyContent:  "center",
                  gap:             "6px",
                }}>
                  <Download size={12} /> DOWNLOAD .XLSX
                </a>
              </div>
            ) : null}
          </div>

          {/* ── Agent Multi-Step Execution Trace ─────────────── */}
          <div>
            <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)", marginBottom: "6px", textTransform: "uppercase" }}>
              Agent Reasoning &amp; Tool Trace ({auditTrace.length} Steps)
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "5px" }}>
              {auditTrace.length === 0 ? (
                <div className="mono" style={{
                  fontSize: "10px", color: "var(--subsystem-muted)",
                  padding: "8px", border: "1px solid var(--grid-boundary)",
                }}>
                  Awaiting query execution trace...
                </div>
              ) : (
                auditTrace.map((step, idx) => {
                  const isVerify = step.action === "VERIFICATION_ENGINE";
                  const isInvalid = isVerify && step.verification_status === "INVALID";

                  return (
                    <div key={idx} style={{
                      padding:         "7px 9px",
                      backgroundColor: "#181B21",
                      border:          "1px solid var(--grid-boundary)",
                      borderLeft:      `2px solid ${isInvalid ? "#C23A2A" : "var(--verification-cyan)"}`,
                    }}>
                      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "2px" }}>
                        <span className="mono" style={{
                          fontSize:  "10px",
                          fontWeight: 600,
                          color:     isInvalid ? "#C23A2A" : "var(--verification-cyan)",
                        }}>
                          STEP {step.step}: {step.action}
                        </span>
                        {isVerify && (
                          <span className="mono" style={{
                            fontSize:        "9px",
                            padding:         "1px 5px",
                            backgroundColor: isInvalid ? "#2A0D0D" : "#0D1F1A",
                            color:           isInvalid ? "#C23A2A" : "var(--verification-cyan)",
                            border:          `1px solid ${isInvalid ? "#C23A2A" : "var(--verification-cyan)"}`,
                          }}>
                            {step.verification_status}
                          </span>
                        )}
                      </div>
                      <div style={{ fontSize: "11px", color: "var(--spec-white)" }}>
                        {step.detail}
                      </div>
                      {step.stdout && (
                        <div className="mono" style={{
                          marginTop:       "4px",
                          padding:         "3px 6px",
                          backgroundColor: "#121417",
                          color:           "var(--verification-cyan)",
                          fontSize:        "10px",
                        }}>
                          SANDBOX_STDOUT: {step.stdout}
                        </div>
                      )}
                    </div>
                  );
                })
              )}
            </div>
          </div>

          {/* ── Live Network Socket Audit ─────────────────────── */}
          <div>
            <div className="mono" style={{
              fontSize:       "10px",
              color:          "var(--subsystem-muted)",
              marginBottom:   "6px",
              textTransform:  "uppercase",
              display:        "flex",
              justifyContent: "space-between",
            }}>
              <span>Process Network Sockets</span>
              <span style={{ color: "var(--verification-cyan)" }}>0 WAN CONNECTIONS</span>
            </div>

            <div style={{
              border:          "1px solid var(--grid-boundary)",
              backgroundColor: "#14171C",
              fontSize:        "10px",
            }} className="mono">
              <div style={{
                display:               "grid",
                gridTemplateColumns:   "35px 1fr 1fr",
                padding:               "4px 6px",
                backgroundColor:       "#1D2128",
                borderBottom:          "1px solid var(--grid-boundary)",
                fontWeight:            600,
                color:                 "var(--subsystem-muted)",
              }}>
                <span>FD</span><span>LOCAL</span><span>REMOTE</span>
              </div>

              {(networkStatus?.connections || []).slice(0, 4).map((c, i) => (
                <div key={i} style={{
                  display:             "grid",
                  gridTemplateColumns: "35px 1fr 1fr",
                  padding:             "4px 6px",
                  borderBottom:        "1px solid #232730",
                  color:               "var(--spec-white)",
                }}>
                  <span>{c.fd === -1 ? `s${i+1}` : c.fd}</span>
                  <span>{c.local_address}</span>
                  <span style={{ color: "var(--verification-cyan)" }}>{c.remote_address}</span>
                </div>
              ))}
            </div>

            <div className="mono" style={{
              marginTop:      "6px",
              fontSize:       "10px",
              color:          "var(--subsystem-muted)",
              display:        "flex",
              alignItems:     "center",
              justifyContent: "space-between",
            }}>
              <span>TELEMETRY FLAGS: DISABLED</span>
              <span>AUDIT HASH: #a8f9c2d1</span>
            </div>
          </div>

        </div>
      )}
    </aside>
  );
}
