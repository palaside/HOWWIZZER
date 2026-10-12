// src/components/FloatingCommandBar.tsx
import React, { useState } from 'react';
import { usePromptInterpreter } from '../../hooks/usePromptInterpreter';

/**
 * Floating command bar that captures user prompts and forwards them to the
 * Silent Injector via the {@code usePromptInterpreter} hook.
 *
 * Design notes:
 * - Positioned fixed at the bottom‑right of the viewport with a subtle glassmorphism
 *   background to match the premium UI guidelines.
 * - Uses the built‑in `interpret` function which handles immediate UI rendering
 *   and async AI streaming.
 */
export const FloatingCommandBar: React.FC = () => {
  const { interpret } = usePromptInterpreter();
  const [input, setInput] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    setIsSubmitting(true);
    try {
      await interpret(input);
    } catch (err) {
      console.error('Prompt interpretation failed:', err);
    } finally {
      setIsSubmitting(false);
      setInput('');
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '1.5rem',
        right: '1.5rem',
        background: 'rgba(255, 255, 255, 0.15)',
        backdropFilter: 'blur(12px)',
        borderRadius: '12px',
        padding: '1rem',
        boxShadow: '0 4px 30px rgba(0,0,0,0.1)',
        width: '320px',
      }}
    >
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '0.5rem' }}>
        <input
          type="text"
          placeholder="Enter command…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isSubmitting}
          style={{
            flex: 1,
            border: 'none',
            background: 'transparent',
            color: '#fff',
            fontSize: '0.95rem',
            outline: 'none',
          }}
        />
        <button
          type="submit"
          disabled={isSubmitting}
          style={{
            padding: '0.4rem 0.8rem',
            borderRadius: '6px',
            border: 'none',
            background: isSubmitting ? '#555' : '#0066ff',
            color: '#fff',
            cursor: isSubmitting ? 'default' : 'pointer',
          }}
        >
          {isSubmitting ? '…' : 'Send'}
        </button>
      </form>
    </div>
  );
};
