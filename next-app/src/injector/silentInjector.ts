// src/injector/silentInjector.ts
import { dualTrack, DualTrackResult } from './dualTrack';
import { Message } from '../../state/unifiedState';
import { Action } from '../../state/actions';

/**
 * Silent Injector – orchestrates the dual‑track flow.
 * It receives the raw user prompt (and optional files), runs the fast path
 * via `dualTrack`, and streams the AI response back, dispatching each piece
 * as a separate `ADD_MESSAGE` action.
 */
export async function inject(
  prompt: string,
  files: File[],
  dispatch: (action: Action) => void
): Promise<void> {
  // 1️⃣ Fast‑track – immediate user message
  const { immediate, stream } = await dualTrack(prompt, files);
  dispatch({ type: 'ADD_MESSAGE', payload: immediate });

  // 2️⃣ Slow‑track – AI response (mocked via dualTrack stream)
  if (stream) {
    let buffer = '';
    for await (const chunk of stream) {
      buffer += chunk;
      const aiMessage: Message = {
        id: crypto.randomUUID?.() ?? `${Date.now()}`,
        role: 'assistant',
        content: buffer,
        ts: Date.now(),
      };
      dispatch({ type: 'ADD_MESSAGE', payload: aiMessage });
    }
  }
}
