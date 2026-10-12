// src/store/useWorkspaceStore.ts
import { create } from 'zustand';

export interface ChatMessage {
  id: string;
  role: 'user' | 'agent';
  content: string;
}

export interface WorkspaceState {
  chatHistory: ChatMessage[];
  attachedFile: File | null;
  workspaceVariables: Record<string, string>; // UI vars set by AI in real‑time
  isProcessing: boolean;

  // Actions – only way UI can mutate state
  addMessage: (msg: Omit<ChatMessage, 'id'>) => void;
  setAttachedFile: (file: File | null) => void;
  updateWorkspaceVars: (vars: Record<string, string>) => void;
  setProcessing: (status: boolean) => void;
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  chatHistory: [],
  attachedFile: null,
  workspaceVariables: {},
  isProcessing: false,

  addMessage: (msg) =>
    set((state) => ({
      chatHistory: [...state.chatHistory, { ...msg, id: crypto.randomUUID?.() ?? `${Date.now()}` }],
    })),

  setAttachedFile: (file) => set({ attachedFile: file }),

  updateWorkspaceVars: (vars) =>
    set((state) => ({
      workspaceVariables: { ...state.workspaceVariables, ...vars },
    })),

  setProcessing: (status) => set({ isProcessing: status }),
}));
