import React, { useState, useEffect } from "react";
import TopRail from "./components/TopRail";
import GroundingPanel from "./components/GroundingPanel";
import WorkspacePanel from "./components/WorkspacePanel";
import AuditProvenancePanel from "./components/AuditProvenancePanel";
import SystemFooter from "./components/SystemFooter";
import { fetchNetworkStatus, fetchDocuments, fetchModels, sendChatQuery } from "./services/api";

export default function App() {
  const [activePersona, setActivePersona] = useState({
    id: "officer_priya",
    name: "Priya Nair",
    role: "Lead Reliability Inspector",
    clearance: "CONFIDENTIAL",
    level: 2,
    color: "#C2782A"
  });

  const [documents, setDocuments] = useState([]);
  const [models, setModels] = useState({});
  const [networkStatus, setNetworkStatus] = useState(null);
  const [conversation, setConversation] = useState([]);
  const [auditTrace, setAuditTrace] = useState([]);
  const [deliverableFile, setDeliverableFile] = useState(null);
  const [lastCitations, setLastCitations] = useState([]);
  const [latencyMs, setLatencyMs] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Initial Load & Polling
  useEffect(() => {
    async function initData() {
      const [docs, mods, net] = await Promise.all([
        fetchDocuments(),
        fetchModels(),
        fetchNetworkStatus()
      ]);
      setDocuments(docs);
      setModels(mods);
      setNetworkStatus(net);
    }
    initData();

    const interval = setInterval(async () => {
      const net = await fetchNetworkStatus();
      setNetworkStatus(net);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmitQuery = async (queryText) => {
    setIsLoading(true);
    const userTimestamp = new Date().toLocaleTimeString();

    // Add User Entry
    setConversation(prev => [
      ...prev,
      {
        type: "user",
        text: queryText,
        userName: activePersona.name,
        clearance: activePersona.clearance,
        timestamp: userTimestamp
      }
    ]);

    try {
      const result = await sendChatQuery(queryText, activePersona.id, activePersona.level);
      
      setLatencyMs(result.execution_time_ms);
      setAuditTrace(result.audit_trace || []);
      setDeliverableFile(result.deliverable_file);
      setLastCitations(result.citations || []);

      // Add Agent Entry
      setConversation(prev => [
        ...prev,
        {
          type: "agent",
          response: result.response,
          lane: result.routing?.lane,
          model: result.routing?.selected_model?.display_name,
          citations: result.citations || [],
          executionTimeMs: result.execution_time_ms,
          timestamp: new Date().toLocaleTimeString()
        }
      ]);

      // Update Network Status from response
      if (result.network_security) {
        setNetworkStatus(result.network_security);
      }
    } catch (error) {
      setConversation(prev => [
        ...prev,
        {
          type: "agent",
          response: `[ERROR] On-premise agent execution halted: ${error.message}`,
          lane: "SYSTEM_ERROR",
          model: "Local Guardrail",
          citations: [],
          executionTimeMs: 0,
          timestamp: new Date().toLocaleTimeString()
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", overflow: "hidden" }}>
      {/* 1. Persistent Top Telemetry Bar */}
      <TopRail
        networkStatus={networkStatus}
        activePersona={activePersona}
        onSelectPersona={setActivePersona}
      />

      {/* 2. Main Tri-Column Instrumentation Deck */}
      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        {/* Left Column: Knowledge Grounding & Model Registry */}
        <GroundingPanel
          documents={documents}
          activePersona={activePersona}
          models={models}
        />

        {/* Center Column: Interactive Workspace & Agent Feed */}
        <WorkspacePanel
          activePersona={activePersona}
          conversation={conversation}
          isLoading={isLoading}
          onSubmitQuery={handleSubmitQuery}
        />

        {/* Right Column: Hero Deliverable & Network Audit */}
        <AuditProvenancePanel
          auditTrace={auditTrace}
          deliverableFile={deliverableFile}
          networkStatus={networkStatus}
          lastCitations={lastCitations}
        />
      </div>

      {/* 3. Bottom Status Rail */}
      <SystemFooter
        latencyMs={latencyMs}
        networkStatus={networkStatus}
      />
    </div>
  );
}
