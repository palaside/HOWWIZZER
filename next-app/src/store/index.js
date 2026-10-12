import create from 'zustand';
import { devtools } from 'zustand/middleware';

export const useWorkspaceStore = create(devtools((set) => ({
  // Core state
  chatHistory: [], // [{id, role, content, timestamp}]
  attachments: [], // [{id, name, url, size}]
  uiVariables: {}, // arbitrary UI state

  // Actions
  addMessage: (msg) => set((s) => ({ chatHistory: [...s.chatHistory, msg] })),
  addAttachment: (file) => set((s) => ({ attachments: [...s.attachments, file] })),
  setUIVariable: (key, value) => set((s) => ({ uiVariables: { ...s.uiVariables, [key]: value } })),
})))
;
