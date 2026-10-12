// src/state/store.ts
import create from 'zustand';
import { devtools } from 'zustand/middleware';
import { UnifiedState } from './unifiedState';
import { Action, reducer } from './actions';

/**
 * Zustand store that holds the **UnifiedState** and provides a **dispatch**
 * function to apply actions via the pure reducer. All components must obtain
 * state or dispatch through this hook – direct mutation is prohibited.
 */
export const useStore = create<UnifiedState & { dispatch: (action: Action) => void }>()(
  devtools((set, get) => ({
    // Initial empty state
    chatHistory: [],
    attachmentData: {},
    workspaceVariables: {},
    // Dispatch applies the reducer and updates the store in one step
    dispatch: (action: Action) => {
      const nextState = reducer(get(), action);
      set(nextState);
    },
  })),
);

// Convenience selector for components that only need the dispatch function
export const useDispatch = () => useStore((state) => state.dispatch);
