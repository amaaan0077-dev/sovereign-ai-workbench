import React from "react";
import {
  CheckCircle2, XCircle, Clock, MinusCircle,
  GitBranch, Shield, Database, Globe, Terminal,
  Cpu, ShieldCheck, ClipboardList, Package, ArrowRight
} from "lucide-react";

// ── Design tokens (CSS vars defined in index.css) ──────────────
const C = {
  dark:   "#1C1F24",
  steel:  "#262B33",
  grid:   "#3A414D",
  white:  "#E1E4EA",
  muted:  "#8792A2",
  cyan:   "#2F818E",
  amber:  "#C2782A",
  red:    "#C23A2A",
  green:  "#2E8B57",
};

// ── Status badge component ──────────────────────────────────────
function StatusBadge({ status }) {
  const cfg = {
    DONE:     { icon: <CheckCircle2 size={11} />, color: C.cyan,  label: "DONE"     },
    VALID:    { icon: <CheckCircle2 size={11} />, color: C.cyan,  label: "VALID"    },
    INVALID:  { icon: <XCircle      size={11} />, color: C.red,   label: "INVALID"  },
    BYPASSED: { icon: <MinusCircle  size={11} />, color: C.muted, label: "BYPASSED" },
    BLOCKED:  { icon: <XCircle      size={11} />, color: C.amber, label: "BLOCKED"  },
    ACTIVE:   { icon: <Clock        size={11} />, color: C.amber, label: "ACTIVE"   },
    PENDING:  { icon: <Clock        size={11} />, color: C.muted, label: "PENDING"  },
  }[status] || { icon: <MinusCircle size={11} />, color: C.muted, label: status };

  return (
    <span style={{
      display:     "inline-flex",
      alignItems:  "center",
      gap:         "4px",
      padding:     "1px 6px",
      fontSize:    "9px",
      fontWeight:  700,
      fontFamily:  "JetBrains Mono, monospace",
      color:       cfg.color,
      border:      `1px solid ${cfg.color}`,
      backgroundColor: `${cfg.color}18`,
    }}>
      {cfg.icon} {cfg.label}
    </span>
  );
}

// ── Single pipeline stage row ───────────────────────────────────
function StageRow({ index, icon: Icon, label, status, detail, subItems }) {
  const isDone     = status === "DONE" || status === "VALID";
  const isBypassed = status === "BYPASSED";
  const isFailed   = status === "INVALID" || status === "BLOCKED";

  const accentColor = isFailed ? C.red : isDone ? C.cyan : isBypassed ? C.muted : C.amber;

  return (
    <div style={{
      display:        "flex",
      flexDirection:  "column",
      borderLeft:     `2px solid ${accentColor}`,
      backgroundColor: isBypassed ? "#14161A" : isDone ? "#111820" : isFailed ? "#1C1010" : "#131720",
      padding:        "7px 10px",
      gap:            "3px",
      opacity:        isBypassed ? 0.6 : 1,
    }}>
      {/* Header row */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "7px" }}>
          {/* Step number */}
          <span style={{
            fontFamily:  "JetBrains Mono, monospace",
            fontSize:    "9px",
            color:       accentColor,
            fontWeight:  700,
            minWidth:    "18px",
          }}>
            [{String(index).padStart(2, "0")}]
          </span>

          {/* Icon */}
          {Icon && <Icon size={12} color={accentColor} />}

          {/* Label */}
          <span style={{
            fontFamily: "JetBrains Mono, monospace",
            fontSize:   "10px",
            fontWeight: 700,
            color:      C.white,
          }}>
            {label}
          </span>
        </div>

        <StatusBadge status={status} />
      </div>

      {/* Detail text */}
      {detail && (
        <div style={{
          fontSize:   "10px",
          color:      C.muted,
          lineHeight: "1.4",
          paddingLeft: "25px",
        }}>
          {detail}
        </div>
      )}

      {/* Sub-items (e.g. passed checks) */}
      {subItems && subItems.length > 0 && (
        <div style={{
          paddingLeft: "25px",
          display:     "flex",
          flexDirection: "column",
          gap:         "2px",
          marginTop:   "2px",
        }}>
          {subItems.slice(0, 3).map((item, i) => (
            <div key={i} style={{
              fontFamily: "JetBrains Mono, monospace",
              fontSize:   "9px",
              color:      item.startsWith("EVIDENCE_CONS") || item.startsWith("HALLUCINATION") ||
                          item.startsWith("PERMISSION") || item.startsWith("SOURCE")
                          ? C.cyan : C.muted,
            }}>
              ↳ {item.length > 70 ? item.slice(0, 70) + "…" : item}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ── 4-lane task-type selector strip ───────────────────────────────
function LaneStrip({ routing }) {
  const lane     = routing?.lane || "";
  const taskType = routing?.task_type || "";

  const lanes = [
    {
      key:    "general",
      label:  "GENERAL / PUBLIC",
      sub:    "KNOWLEDGE",
      active: lane === "LANE_A_GENERAL" && taskType === "GENERAL_KNOWLEDGE",
      color:  C.cyan,
    },
    {
      key:    "confidential",
      label:  "COMPANY",
      sub:    "CONFIDENTIAL",
      active: lane === "LANE_B_COMPANY_CONFIDENTIAL",
      color:  C.amber,
    },
    {
      key:    "code",
      label:  "CODE /",
      sub:    "ENGINEERING",
      active: taskType === "CODE_SANDBOX",
      color:  C.cyan,
    },
    {
      key:    "document",
      label:  "DOCUMENT /",
      sub:    "ARTIFACT GEN.",
      active: taskType === "DELIVERABLE_DRAFTING",
      color:  C.amber,
    },
  ];

  return (
    <div style={{
      display:         "grid",
      gridTemplateColumns: "repeat(4, 1fr)",
      gap:             "4px",
      marginBottom:    "8px",
    }}>
      {lanes.map(lane => (
        <div key={lane.key} style={{
          padding:         "6px 4px",
          backgroundColor: lane.active ? `${lane.color}20` : C.dark,
          border:          `1px solid ${lane.active ? lane.color : C.grid}`,
          textAlign:       "center",
        }}>
          <div style={{
            fontFamily: "JetBrains Mono, monospace",
            fontSize:   "8px",
            fontWeight: 700,
            color:      lane.active ? lane.color : C.muted,
          }}>
            {lane.label}
          </div>
          <div style={{
            fontFamily: "JetBrains Mono, monospace",
            fontSize:   "7px",
            color:      lane.active ? lane.color : C.muted,
            opacity:    0.8,
          }}>
            {lane.sub}
          </div>
          {lane.active && (
            <div style={{
              width:           "6px",
              height:          "6px",
              backgroundColor: lane.color,
              borderRadius:    "50%",
              margin:          "3px auto 0",
            }} />
          )}
        </div>
      ))}
    </div>
  );
}

// ── Helper: derive stage status from audit_trace ────────────────
function deriveStages(auditTrace, routing, verificationResult, webResearch) {
  if (!auditTrace || auditTrace.length === 0) {
    // No data yet — show all pending
    return Array.from({ length: 9 }, (_, i) => ({
      index: i + 1,
      status: "PENDING",
      detail: null,
      subItems: [],
    }));
  }

  const findStep = (actionName) =>
    auditTrace.find(s => s.action === actionName);

  // [1] Query Routing
  const routingStep = findStep("QUERY_ROUTING");
  const s1 = {
    index:  1,
    icon:   GitBranch,
    label:  "MODEL / TASK ROUTER",
    status: routingStep ? "DONE" : "PENDING",
    detail: routingStep
      ? `${routingStep.detail} | Task: ${routingStep.task_type}`
      : null,
    subItems: routingStep?.routing_reasons || [],
  };

  // [2] RBAC / Clearance
  const ragStep    = findStep("CLEARANCE_FILTERED_RAG");
  const ragBypass  = findStep("RAG_BYPASS");
  const s2 = {
    index:  2,
    icon:   Shield,
    label:  "RBAC / CLEARANCE CHECK",
    status: (ragStep || ragBypass) ? "DONE" : routingStep ? "DONE" : "PENDING",
    detail: ragStep
      ? `Clearance gate active. Retrieved ${ragStep.citations?.length ?? 0} authorized document(s).`
      : ragBypass
      ? "Lane A: No clearance-gated retrieval needed."
      : null,
    subItems: [],
  };

  // [3] RAG Engine
  const s3 = {
    index:  3,
    icon:   Database,
    label:  "RAG ENGINE",
    status: ragStep ? "DONE" : ragBypass ? "BYPASSED" : routingStep ? "BYPASSED" : "PENDING",
    detail: ragStep
      ? `${ragStep.detail}`
      : ragBypass
      ? "Lane A query — private vector store bypassed."
      : null,
    subItems: ragStep?.citations || [],
  };

  // [4] Web Search Agent
  const webDone     = findStep("PUBLIC_WEB_RESEARCH");
  const webBlocked  = findStep("PUBLIC_WEB_RESEARCH_BLOCKED");
  const webBypass   = findStep("WEB_RESEARCH_BYPASS");
  const webUnavail  = findStep("PUBLIC_WEB_RESEARCH_UNAVAILABLE");
  let webStatus = "PENDING";
  let webDetail = null;
  let webSubs   = [];
  if (webDone) {
    webStatus = "DONE";
    webDetail = `${webDone.sources_found} public source(s) retrieved.`;
    webSubs   = (webDone.sources || []).slice(0, 2).map(s => s.title || s.url || "");
  } else if (webBlocked) {
    webStatus = "BLOCKED";
    webDetail = "Privacy filter blocked — confidential data detected in query.";
  } else if (webBypass) {
    webStatus = "BYPASSED";
    webDetail = "No current public information required.";
  } else if (webUnavail) {
    webStatus = "BYPASSED";
    webDetail = webUnavail.detail || "Web research unavailable.";
  }
  const s4 = { index: 4, icon: Globe, label: "WEB SEARCH AGENT", status: webStatus, detail: webDetail, subItems: webSubs };

  // [5] Sandbox
  const sandboxStep   = findStep("SANDBOX_CODE_VERIFICATION");
  const sandboxBypass = findStep("SANDBOX_BYPASS");
  const s5 = {
    index:  5,
    icon:   Terminal,
    label:  "SANDBOX EXECUTION",
    status: sandboxStep ? "DONE" : sandboxBypass ? "BYPASSED" : routingStep ? "BYPASSED" : "PENDING",
    detail: sandboxStep
      ? `Exit code: ${sandboxStep.exit_code} | ${sandboxStep.stdout || ""}`
      : "No code execution or engineering calculation requested.",
    subItems: [],
  };

  // [6] Context Builder (implicit — always runs)
  const llmStep = findStep("LOCAL_LLM_SYNTHESIS");
  const s6 = {
    index:  6,
    icon:   Package,
    label:  "CONTEXT BUILDER",
    status: llmStep ? "DONE" : routingStep ? "ACTIVE" : "PENDING",
    detail: llmStep
      ? `Combined: RAG chunks (${llmStep.private_chunks_used}), web sources (${llmStep.web_sources_used}), user query, tool outputs.`
      : null,
    subItems: [],
  };

  // [7] Local LLM
  const xlsxStep = findStep("XLSX_ANALYSIS_COMPILED");
  const s7 = {
    index:  7,
    icon:   Cpu,
    label:  "LOCAL LLM (OLLAMA)",
    status: llmStep ? "DONE" : "PENDING",
    detail: llmStep
      ? `Model: ${llmStep.model} | Web sources: ${llmStep.web_sources_used} | RAG chunks: ${llmStep.private_chunks_used}${xlsxStep ? " | XLSX compiled" : ""}`
      : null,
    subItems: [],
  };

  // [8] Verification Engine
  const verifyStep = findStep("VERIFICATION_ENGINE");
  let verifyStatus = "PENDING";
  if (verifyStep) {
    verifyStatus = verifyStep.verification_status === "VALID" ? "VALID" : "INVALID";
  }
  const s8 = {
    index:  8,
    icon:   ShieldCheck,
    label:  "VERIFICATION ENGINE",
    status: verifyStatus,
    detail: verifyStep?.detail || null,
    subItems: [
      ...(verifyStep?.passed_checks || []),
      ...(verifyStep?.issues || []).map(i => "⚠ " + i),
    ],
  };

  // [9] Audit + Security
  const auditStep = findStep("AUDIT_SECURITY_LOGGED");
  const s9 = {
    index:  9,
    icon:   ClipboardList,
    label:  "AUDIT + SECURITY LOG",
    status: auditStep ? "DONE" : verifyStep ? "DONE" : "PENDING",
    detail: auditStep
      ? auditStep.detail
      : verifyStep
      ? "Audit record pending write..."
      : null,
    subItems: [],
  };

  return [s1, s2, s3, s4, s5, s6, s7, s8, s9];
}

// ── Main PipelineView component ─────────────────────────────────
export default function PipelineView({
  auditTrace,
  routing,
  verificationResult,
  webResearch,
  isLoading,
}) {
  const stages = deriveStages(auditTrace, routing, verificationResult, webResearch);
  const hasData = auditTrace && auditTrace.length > 0;

  return (
    <div style={{
      display:       "flex",
      flexDirection: "column",
      gap:           "6px",
      padding:       "10px",
      overflowY:     "auto",
      height:        "100%",
    }}>
      {/* Header */}
      <div style={{
        fontFamily:  "JetBrains Mono, monospace",
        fontSize:    "9px",
        color:       C.muted,
        paddingBottom: "6px",
        borderBottom: `1px solid ${C.grid}`,
        display:     "flex",
        justifyContent: "space-between",
        alignItems:  "center",
      }}>
        <span>LIVE PIPELINE TRACE — {hasData ? "EXECUTED" : isLoading ? "RUNNING..." : "AWAITING QUERY"}</span>
        {hasData && (
          <span style={{ color: C.cyan }}>
            {stages.filter(s => s.status === "DONE" || s.status === "VALID").length}/{stages.length} COMPLETE
          </span>
        )}
      </div>

      {/* 4-Lane task router strip */}
      <LaneStrip routing={routing} />

      {/* Connector arrow into pipeline */}
      <div style={{ display: "flex", justifyContent: "center", padding: "2px 0" }}>
        <ArrowRight size={12} color={C.muted} style={{ transform: "rotate(90deg)" }} />
      </div>

      {/* Pipeline stages */}
      <div style={{ display: "flex", flexDirection: "column", gap: "3px" }}>
        {stages.map((stage) => (
          <StageRow
            key={stage.index}
            index={stage.index}
            icon={stage.icon}
            label={stage.label}
            status={stage.status}
            detail={stage.detail}
            subItems={stage.subItems}
          />
        ))}
      </div>

      {/* Output summary */}
      {hasData && (
        <>
          <div style={{ display: "flex", justifyContent: "center", padding: "2px 0" }}>
            <ArrowRight size={12} color={C.muted} style={{ transform: "rotate(90deg)" }} />
          </div>
          <div style={{
            border:          `1px solid ${C.cyan}`,
            backgroundColor: "#0F1820",
            padding:         "8px 10px",
          }}>
            <div style={{
              fontFamily:    "JetBrains Mono, monospace",
              fontSize:      "9px",
              fontWeight:    700,
              color:         C.cyan,
              marginBottom:  "4px",
            }}>
              [OUTPUT] SOVEREIGN RESPONSE PACKAGE
            </div>
            <div style={{
              display:               "grid",
              gridTemplateColumns:   "repeat(3, 1fr)",
              gap:                   "4px",
            }}>
              {[
                { label: "ANSWER",    desc: "Chat response" },
                { label: "EVIDENCE",  desc: "RAG citations" },
                { label: "FILES",     desc: "DOCX / XLSX" },
              ].map(item => (
                <div key={item.label} style={{
                  textAlign:       "center",
                  padding:         "5px",
                  backgroundColor: C.dark,
                  border:          `1px solid ${C.grid}`,
                }}>
                  <div style={{
                    fontFamily: "JetBrains Mono, monospace",
                    fontSize:   "8px",
                    fontWeight: 700,
                    color:      C.white,
                  }}>
                    {item.label}
                  </div>
                  <div style={{
                    fontFamily: "JetBrains Mono, monospace",
                    fontSize:   "7px",
                    color:      C.muted,
                    marginTop:  "2px",
                  }}>
                    {item.desc}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {/* Empty state */}
      {!hasData && !isLoading && (
        <div style={{
          marginTop:       "8px",
          padding:         "12px",
          border:          `1px dashed ${C.grid}`,
          textAlign:       "center",
          color:           C.muted,
          fontFamily:      "JetBrains Mono, monospace",
          fontSize:        "10px",
          backgroundColor: C.dark,
        }}>
          Dispatch a query to trace the live pipeline execution.
        </div>
      )}
    </div>
  );
}
