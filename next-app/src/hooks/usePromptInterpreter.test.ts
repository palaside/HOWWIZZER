// src/hooks/usePromptInterpreter.test.ts
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useWorkspaceStore } from '../store/useWorkspaceStore';
import { usePromptInterpreter } from './usePromptInterpreter';

// Mock the AI gateway injector
vi.mock('../lib/aiGatewayInjector', () => ({
  aiGatewayInjector: {
    sendPrompt: vi.fn(async (text: string, file: File | null) => {
      // Simulate a delayed response
      await new Promise((r) => setTimeout(r, 5));
      return {
        reply: `Mock reply for ${text}`,
        uiChanges: { '--mock-var': '1' },
      };
    }),
  },
}));

import { aiGatewayInjector } from '../lib/aiGatewayInjector';

describe('usePromptInterpreter hook', () => {
  beforeEach(() => {
    // Reset the Zustand store
    useWorkspaceStore.setState({
      chatHistory: [],
      attachedFile: null,
      workspaceVariables: {},
      isProcessing: false,
    });
  });

  test('toggles isProcessing true during flow and false after (including on error)', async () => {
    const { result } = renderHook(() => usePromptInterpreter());
    const { interpret } = result.current;

    // Start command – should set processing true immediately
    const promise = act(() => interpret('test command'));
    // Check that processing flag is true right after invocation
    expect(useWorkspaceStore.getState().isProcessing).toBe(true);

    // Resolve the promise
    await promise;
    // After completion processing should be false
    expect(useWorkspaceStore.getState().isProcessing).toBe(false);
    // Verify that AI reply was added to chatHistory
    const { chatHistory, workspaceVariables } = useWorkspaceStore.getState();
    expect(chatHistory.length).toBe(2); // user + agent
    expect(chatHistory[1].role).toBe('assistant');
    expect(chatHistory[1].content).toContain('Mock reply');
    // UI changes should be merged
    expect(workspaceVariables).toMatchObject({ '--mock-var': '1' });
    // Ensure the mock was called
    expect(aiGatewayInjector.sendPrompt).toHaveBeenCalledOnce();
  });
});
