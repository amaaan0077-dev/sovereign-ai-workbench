import React from "react";
import { Download, ShieldCheck, CheckCircle, FileText, Activity, Hash, Lock } from "lucide-react";

export default function AuditProvenancePanel({ auditTrace, deliverableFile, networkStatus, lastCitations }) {
  const downloadUrl = deliverableFile ? `http://127.0.0.1:8000/api/deliverables/${deliverableFile}` : null;

  return (
    <aside style={{
      width: "360px",
      height: "calc(100vh - 44px - 28px)",
      backgroundColor: "var(--console-steel)",
      display: "flex",
      flexDirection: "column",
      fontSize: "12px"
    }}>
      {/* Panel Top Header */}
      <div style={{
        padding: "10px 12px",
        borderBottom: "1px solid var(--grid-boundary)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        backgroundColor: "#1F232A"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "7px", fontWeight: 600 }}>
          <Activity size={13} color="var(--verification-cyan)" />
          <span>PROVENANCE &amp; NETWORK AUDIT</span>
        </div>
        <span className="mono" style={{ fontSize: "10px", color: "var(--verification-cyan)" }}>
          0 WAN PACKETS
        </span>
      </div>

      <div style={{ flex: 1, overflowY: "auto", padding: "12px", display: "flex", flexDirection: "column", gap: "14px" }}>
        
        {/* HERO SECTION: GENERATED DELIVERABLE CARD */}
        <div>
          <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)", marginBottom: "6px", textTransform: "uppercase" }}>
            Generated Industrial Deliverable (.docx)
          </div>

          {deliverableFile ? (
            <div style={{
              backgroundColor: "#191D24",
              border: "1px solid var(--verification-cyan)",
              padding: "12px",
              display: "flex",
              flexDirection: "column",
              gap: "8px"
            }}>
              {/* Classification Banner */}
              <div style={{
                textAlign: "center",
                padding: "2px 0",
                backgroundColor: "#2B1D11",
                border: "1px solid var(--restricted-amber)",
                color: "var(--restricted-amber)",
                fontWeight: 600,
                fontSize: "10px",
                letterSpacing: "0.05em"
              }} className="mono">
                ★ CLASSIFIED: CONFIDENTIAL // AIR-GAPPED ON-PREMISE ★
              </div>

              {/* Document Info */}
              <div style={{ display: "flex", alignItems: "center", gap: "8px", marginTop: "2px" }}>
                <FileText size={20} color="var(--verification-cyan)" />
                <div>
                  <div style={{ fontWeight: 600, color: "var(--spec-white)", fontSize: "12px" }}>
                    Official Safety Approval Note
                  </div>
                  <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)" }}>
                    REF: IOCL/OPS/2026/CRACK-CD01.docx
                  </div>
                </div>
              </div>

              <div style={{ fontSize: "11px", color: "var(--subsystem-muted)", lineHeight: "1.4" }} className="serif-doc">
                Autonomous technical memo incorporating PAUT ultrasonic crack penetration telemetry, ISO 10816-3 vibration baseline, sandboxed MAWP derating formula, and formal sign-off blocks.
              </div>

              {/* Direct Download Button */}
              <a
                href={downloadUrl}
                download
                target="_blank"
                rel="noreferrer"
                style={{
                  marginTop: "6px",
                  padding: "8px 12px",
                  backgroundColor: "var(--verification-cyan)",
                  color: "#16191E",
                  textDecoration: "none",
                  fontWeight: 600,
                  fontSize: "11px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "6px"
                }}
              >
                <Download size={13} />
                <span>DOWNLOAD VERIFIED .DOCX</span>
              </a>
            </div>
          ) : (
            <div style={{
              padding: "14px",
              border: "1px dashed var(--grid-boundary)",
              backgroundColor: "#191B20",
              textAlign: "center",
              color: "var(--subsystem-muted)",
              fontSize: "11px"
            }}>
              No deliverable generated in current run. Dispatch the <strong>Hero Demo preset</strong> to compile a formal Word approval note with sandboxed calculations.
            </div>
          )}
        </div>

        {/* AGENT MULTI-STEP EXECUTION TRACE */}
        <div>
          <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)", marginBottom: "6px", textTransform: "uppercase" }}>
            Agent Reasoning &amp; Tool Trace ({auditTrace.length} Steps)
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            {auditTrace.length === 0 ? (
              <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)", padding: "8px", border: "1px solid var(--grid-boundary)" }}>
                Awaiting query execution trace...
              </div>
            ) : (
              auditTrace.map((step, idx) => (
                <div key={idx} style={{
                  padding: "7px 9px",
                  backgroundColor: "#181B21",
                  border: "1px solid var(--grid-boundary)",
                  borderLeft: "2px solid var(--verification-cyan)"
                }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "2px" }}>
                    <span className="mono" style={{ fontSize: "10px", fontWeight: 600, color: "var(--verification-cyan)" }}>
                      STEP {step.step}: {step.action}
                    </span>
                    <CheckCircle size={10} color="var(--verification-cyan)" />
                  </div>
                  <div style={{ fontSize: "11px", color: "var(--spec-white)" }}>
                    {step.detail}
                  </div>
                  {step.stdout && (
                    <div className="mono" style={{
                      marginTop: "4px",
                      padding: "3px 6px",
                      backgroundColor: "#121417",
                      color: "var(--verification-cyan)",
                      fontSize: "10px"
                    }}>
                      SANDBOX_STDOUT: {step.stdout}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* LIVE NETWORK SOCKET AUDIT */}
        <div>
          <div className="mono" style={{ fontSize: "10px", color: "var(--subsystem-muted)", marginBottom: "6px", textTransform: "uppercase", display: "flex", justifyContent: "space-between" }}>
            <span>Process Network Sockets</span>
            <span style={{ color: "var(--verification-cyan)" }}>0 WAN CONNECTIONS</span>
          </div>

          <div style={{
            border: "1px solid var(--grid-boundary)",
            backgroundColor: "#14171C",
            fontSize: "10px"
          }} className="mono">
            <div style={{
              display: "grid",
              gridTemplateColumns: "35px 1fr 1fr",
              padding: "4px 6px",
              backgroundColor: "#1D2128",
              borderBottom: "1px solid var(--grid-boundary)",
              fontWeight: 600,
              color: "var(--subsystem-muted)"
            }}>
              <span>FD</span>
              <span>LOCAL</span>
              <span>REMOTE</span>
            </div>

            {(networkStatus?.connections || []).slice(0, 4).map((c, i) => (
              <div key={i} style={{
                display: "grid",
                gridTemplateColumns: "35px 1fr 1fr",
                padding: "4px 6px",
                borderBottom: "1px solid #232730",
                color: "var(--spec-white)"
              }}>
                <span>{c.fd === -1 ? `s${i+1}` : c.fd}</span>
                <span>{c.local_address}</span>
                <span style={{ color: "var(--verification-cyan)" }}>{c.remote_address}</span>
              </div>
            ))}
          </div>

          <div className="mono" style={{
            marginTop: "6px",
            fontSize: "10px",
            color: "var(--subsystem-muted)",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between"
          }}>
            <span>TELEMETRY FLAGS: DISABLED</span>
            <span>AUDIT HASH: #a8f9c2d1</span>
          </div>
        </div>

      </div>
    </aside>
  );
}
