// src/state/actions.ts
import { Message, FileMeta, UnifiedState } from './unifiedState';

export type Action =
  | { type: 'ADD_MESSAGE'; payload: Message }
  | { type: 'ADD_ATTACHMENT'; payload: FileMeta }
  | { type: 'SET_VAR'; payload: { key: string; value: any } };

export function reducer(state: UnifiedState, action: Action): UnifiedState {
  switch (action.type) {
    case 'ADD_MESSAGE':
      return { ...state, chatHistory: [...state.chatHistory, action.payload] };
    case 'ADD_ATTACHMENT':
      return {
        ...state,
        attachmentData: { ...state.attachmentData, [action.payload.id]: action.payload },
      };
    case 'SET_VAR':
      return {
        ...state,
        workspaceVariables: { ...state.workspaceVariables, [action.payload.key]: action.payload.value },
      };
    default:
      return state;
  }
}
