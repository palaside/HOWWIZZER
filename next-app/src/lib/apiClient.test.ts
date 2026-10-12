import { apiClient } from './apiClient';
import { useAuthStore } from '../store/useAuthStore';

import { describe, it, expect, beforeEach } from 'vitest';

describe('apiClient', () => {
  beforeEach(() => {
    // Reset token before each test
    useAuthStore.getState().clearAuth();
  });

  it('injects Authorization header when token is present', () => {
    const token = 'test-token-123';
    const user = { id: '1', email: 'u@example.com', role: 'admin' } as const;
    // Set auth state
    useAuthStore.getState().setAuth(user, token);

    // Grab the request interceptor directly
    const requestInterceptor = apiClient.interceptors.request.handlers[0].fulfilled;
    const config = requestInterceptor({ headers: {} } as any);
    expect(config.headers.Authorization).toBe(`Bearer ${token}`);
  });

  it('does not set Authorization header when token is missing', () => {
    const requestInterceptor = apiClient.interceptors.request.handlers[0].fulfilled;
    const config = requestInterceptor({ headers: {} } as any);
    expect(config.headers.Authorization).toBeUndefined();
  });
});
