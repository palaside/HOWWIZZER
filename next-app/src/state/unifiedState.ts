// src/state/unifiedState.ts
export type Message = {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  ts: number; // timestamp ms
};

export type FileMeta = {
  id: string;
  name: string;
  size: number; // bytes
  mime: string;
  previewUrl?: string;
};

export type UnifiedState = {
  chatHistory: Message[];
  attachmentData: Record<string, FileMeta>;
  workspaceVariables: Record<string, any>;
};
