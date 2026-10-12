// src/lib/aiGatewayInjector.ts
/**
 * Mocked AI gateway injector used by the frontend hook.
 * In a real implementation this would call the FastAPI Silent Injector
 * via HTTP (e.g., fetch with Server‑Sent Events) and stream responses.
 * For unit tests we keep it synchronous and deterministic.
 */
export const aiGatewayInjector = {
  /**
   * Simulate sending a prompt (and optional file) to the backend.
   * Returns a lightweight response object containing a reply string
   * and optional UI variable changes.
   */
  async sendPrompt(
    text: string,
    file: File | null
  ): Promise<{ reply: string; uiChanges?: Record<string, string> }> {
    // Simple deterministic mock – echo the prompt length and file name if any.
    const reply = `AI processed ${text.length} characters${file ? ` with file ${file.name}` : ''}`;
    // Example UI changes – could be used to update CSS variables, etc.
    const uiChanges = file
      ? { '--bg-color': '#202020', '--accent': '#CEDE62' }
      : { '--bg-color': '#121413' };
    // Simulate minimal async latency
    await new Promise((r) => setTimeout(r, 10));
    return { reply, uiChanges };
  },
};
