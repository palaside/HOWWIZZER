// vitest.setup.ts
// Global test setup for Vitest (happy-dom)
// Provides jest-dom matchers and ensures a minimal DOM environment.

import '@testing-library/jest-dom'; // optional matchers like toBeInTheDocument

// In case any test accesses document/window before happy-dom initializes,
// we provide a very small stub. Happy-dom already defines global.document,
// but explicit stubbing avoids ReferenceError in edge cases.
if (typeof document === 'undefined') {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (global as any).document = {} as Document;
}
if (typeof window === 'undefined') {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (global as any).window = {} as Window;
}
