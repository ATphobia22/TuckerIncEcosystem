// Experimental WebMCP bridge for Tucker AI.
// WebMCP is a browser-native draft/preview API; keep consequential operations
// behind explicit user confirmation and never expose credentials in tool schemas.

export function registerTuckerWebMCP({ baseUrl = window.location.origin, signal }) {
  const modelContext = document.modelContext ?? navigator.modelContext;
  if (!modelContext) return false;

  modelContext.registerTool({
    name: "tucker_ai_sources",
    description: "Read the currently registered Tucker AI authoritative source catalog.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
    annotations: { readOnlyHint: true },
    execute: async () => {
      const response = await fetch(`${baseUrl}/api/sources`, { headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error(`source catalog request failed: ${response.status}`);
      return response.json();
    },
  }, { signal });

  modelContext.registerTool({
    name: "tucker_ai_capabilities",
    description: "Read detected quantum and hybrid-compute capabilities.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
    annotations: { readOnlyHint: true },
    execute: async () => {
      const response = await fetch(`${baseUrl}/api/tucker-ai/capability-discovery`, { headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error(`capability request failed: ${response.status}`);
      return response.json();
    },
  }, { signal });

  return true;
}
