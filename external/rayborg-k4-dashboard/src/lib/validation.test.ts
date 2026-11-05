import { describe, expect, it } from 'vitest';
import type { Experiment } from '../types';
import {
  contentFingerprint,
  isExperiment,
  isExperimentArray,
  mergeExperimentRecords,
} from './validation';

function fixture(overrides: Partial<Experiment> = {}): Experiment {
  return {
    id: 'run-1',
    createdAt: '2026-07-27T00:00:00.000Z',
    title: 'Control',
    section: 'K4',
    method: 'Vigenere',
    operation: 'decrypt',
    key: 'KEY',
    alphabet: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    input: 'ABC',
    output: 'XYZ',
    notes: '',
    status: 'tested',
    provenance: {
      appVersion: '0.1.0',
      inputFingerprint: contentFingerprint('ABC'),
      indexConvention: 'one-based local K4 positions 1–97',
      parameters: { key: 'KEY' },
      searchSpace: 'single deterministic transformation',
      corpus: 'not used',
      scoring: 'not used',
      seed: 'not applicable',
      elapsedMs: 0.1,
      hardware: 'test runner',
      candidatesTested: 1,
      holdout: 'not applicable',
      negativeControl: 'not run',
    },
    ...overrides,
  };
}

describe('persisted experiment validation', () => {
  it('accepts a complete bounded experiment', () => {
    expect(isExperiment(fixture())).toBe(true);
    expect(isExperimentArray([fixture()])).toBe(true);
  });

  it('rejects invalid React-child fields and duplicate IDs', () => {
    expect(isExperiment({ ...fixture(), section: { value: 'K4' } })).toBe(false);
    expect(isExperiment({ ...fixture(), provenance: { parameters: {} } })).toBe(false);
    expect(isExperimentArray([fixture(), fixture()])).toBe(false);
  });

  it('merges external records by ID with external state winning', () => {
    const local = fixture({ status: 'active' });
    const external = fixture({ status: 'rejected' });
    expect(mergeExperimentRecords([local], [external])).toEqual([external]);
  });

  it('creates deterministic content fingerprints', () => {
    expect(contentFingerprint('ABC')).toBe(contentFingerprint('ABC'));
    expect(contentFingerprint('ABC')).not.toBe(contentFingerprint('ABD'));
  });
});
