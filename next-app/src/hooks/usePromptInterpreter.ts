// src/hooks/usePromptInterpreter.ts
import { useStore } from '../state/store';
import { Action } from '../state/actions';
import { inject } from '../injector/silentInjector';

/**
 * Hook that provides a function to interpret a user prompt.
 * It dispatches the immediate message via the store and then invokes the silent injector
 * to handle async AI response streaming.
 */
export function usePromptInterpreter() {
  const dispatch = useStore((state) => state.dispatch);

  const interpret = async (prompt: string, files: File[] = []) => {
    // The silent injector handles dispatching both immediate user message and AI response.
    await inject(prompt, files, (action: Action) => dispatch(action));
  };

  return { interpret };
}
