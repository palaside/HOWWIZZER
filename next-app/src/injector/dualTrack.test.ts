// src/injector/dualTrack.test.ts
import { beforeEach, describe, expect, test } from 'vitest';
import { dualTrack } from './dualTrack';

describe('dualTrack timing', () => {
  beforeEach(() => {
    // no setup required
  });

  test('immediate message is produced within 60ms', async () => {
    const start = performance.now();
    const { immediate } = await dualTrack('quick input');
    const elapsed = performance.now() - start;
    expect(immediate).toBeDefined();
    expect(elapsed).toBeLessThan(60);
  });
});
