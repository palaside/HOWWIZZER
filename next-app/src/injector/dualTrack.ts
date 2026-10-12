// src/injector/dualTrack.ts
import { Message } from '../../state/unifiedState';

/**
 * Result of the dual‑track processing.
 * - `immediate` is the message that appears instantly (≤ 60 ms).
 * - `stream` is an async iterable that yields subsequent fragments
 *   (simulating the SSE‑backed AI response).
 */
export interface DualTrackResult {
  immediate: Message;
  stream?: AsyncIterable<string>;
}

/**
 * Simulate the fast‑track rendering and the slower AI stream.
 * In production this would call the Silent Injector which talks to the
 * FastAPI backend via SSE. Here we provide a lightweight mock that
 * respects the timing contract for TDD.
 */
export async function dualTrack(
  input: string,
  files?: File[]
): Promise<DualTrackResult> {
  // Immediate message (should be emitted within ~50 ms)
  const immediate: Message = {
    id: crypto.randomUUID?.() ?? `${Date.now()}`,
    role: 'user',
    content: input,
    ts: Date.now(),
  };

  // Mocked async generator for the streamed AI answer
  async function* streamGenerator() {
    const chunks = ['Processing...', 'Analyzing data...', 'Result ready!'];
    for (const chunk of chunks) {
      // Small delay to simulate work (< 30 ms each)
      await new Promise((r) => setTimeout(r, 30));
      yield chunk;
    }
  }

  return { immediate, stream: streamGenerator() };
}
