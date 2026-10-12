import { describe, beforeEach, it, expect } from 'vitest';
import { useAuthStore } from './useAuthStore';
describe('Auth Store (Context Holder)', () => {
  beforeEach(() => {
    useAuthStore.getState().clearAuth();
  });

  it('setAuth updates state correctly', () => {
    const user = { id: 'u1', email: 'user@example.com', role: 'admin' } as const;
    const token = 'secret-token';
    useAuthStore.getState().setAuth(user, token);
    const state = useAuthStore.getState();
    expect(state.user).toEqual(user);
    expect(state.token).toBe(token);
    expect(state.isAuthenticated).toBe(true);
  });

  it('clearAuth resets state', () => {
    const user = { id: 'u1', email: 'user@example.com', role: 'admin' } as const;
    const token = 'secret-token';
    useAuthStore.getState().setAuth(user, token);
    useAuthStore.getState().clearAuth();
    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.token).toBeNull();
    expect(state.isAuthenticated).toBe(false);
  });
});
