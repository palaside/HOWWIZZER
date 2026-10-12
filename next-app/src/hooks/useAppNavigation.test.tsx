import { renderHook, act } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { useAppNavigation } from './useAppNavigation';
import { describe, it, expect } from 'vitest';

// Helper to render hook within a router context
const renderUseAppNavigation = () => {
  return renderHook(() => useAppNavigation(), {
    wrapper: ({ children }) => (
      <MemoryRouter initialEntries={['/']}>{children}</MemoryRouter>
    ),
  });
};

describe('useAppNavigation (Frontend Hook Router)', () => {
  it('navigates to dashboard', () => {
    const { result } = renderUseAppNavigation();
    act(() => {
      result.current.goToDashboard();
    });
    // After navigation, the location should be /dashboard
    expect(window.location.pathname).toBe('/dashboard');
  });

  it('navigates to login', () => {
    const { result } = renderUseAppNavigation();
    act(() => {
      result.current.goToLogin();
    });
    expect(window.location.pathname).toBe('/login');
  });

  it('goBack navigates back', () => {
    const { result } = renderUseAppNavigation();
    // push a second entry then go back
    act(() => {
      window.history.pushState({}, '', '/first');
      result.current.goToDashboard(); // navigates to /dashboard
    });
    expect(window.location.pathname).toBe('/dashboard');
    act(() => {
      result.current.goBack();
    });
    expect(window.location.pathname).toBe('/first');
  });
});
