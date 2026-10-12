// src/store/useWorkspaceStore.test.ts
import { beforeEach, describe, expect, test } from 'vitest';
import { useWorkspaceStore } from './useWorkspaceStore';

describe('useWorkspaceStore - updateWorkspaceVars', () => {
  beforeEach(() => {
    // Reset store to a clean state before each test
    useWorkspaceStore.setState({
      chatHistory: [],
      attachedFile: null,
      workspaceVariables: {},
      isProcessing: false,
    });
  });

  test('merges new CSS vars without overwriting existing keys', () => {
    const { updateWorkspaceVars } = useWorkspaceStore.getState();
    // First update adds one var
    updateWorkspaceVars({ '--primary-color': '#ff0' });
    // Second update adds another var
    updateWorkspaceVars({ '--bg-color': '#111' });

    const { workspaceVariables } = useWorkspaceStore.getState();
    expect(workspaceVariables).toEqual({
      '--primary-color': '#ff0',
      '--bg-color': '#111',
    });
  });
});
