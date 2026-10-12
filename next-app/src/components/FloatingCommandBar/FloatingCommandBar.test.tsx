// src/components/FloatingCommandBar/FloatingCommandBar.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { FloatingCommandBar } from './FloatingCommandBar';
import { describe, test, expect, vi } from 'vitest';
const mockInterpret = vi.fn().mockResolvedValue(undefined);

vi.mock('../../hooks/usePromptInterpreter', () => ({ __esModule: true, usePromptInterpreter: () => ({ prompt: [], addMessage: vi.fn(), interpret: mockInterpret }) }));

describe('FloatingCommandBar', () => {
  test('renders input and send button', () => {
    render(<FloatingCommandBar />);
    const input = screen.getByPlaceholderText('Enter command…');
    const button = screen.getByRole('button', { name: /send/i });
    expect(input).toBeInTheDocument();
    expect(button).toBeInTheDocument();
  });

  test('calls interpret on submit', async () => {

    render(<FloatingCommandBar />);
    const input = screen.getByPlaceholderText('Enter command…');
    const button = screen.getByRole('button', { name: /send/i });
    fireEvent.change(input, { target: { value: 'test prompt' } });
    fireEvent.click(button);
    // Wait for promise resolution
    await new Promise((r) => setTimeout(r, 0));
    expect(mockInterpret).toHaveBeenCalledWith('test prompt');
  });
});
