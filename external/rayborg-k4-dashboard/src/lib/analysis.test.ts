import { describe, expect, it } from 'vitest';
import { K4_CIPHER, STANDARD_ALPHABET } from '../data/kryptos';
import {
  deriveKeystream,
  averagePeriodicIc,
  indexOfCoincidence,
  letterFrequencies,
  repeatedNgrams,
  shannonEntropy,
  textFingerprint,
} from './analysis';

describe('statistical diagnostics', () => {
  it('calculates limiting IC examples', () => {
    expect(indexOfCoincidence('AAAA')).toBe(1);
    expect(indexOfCoincidence('ABCD')).toBe(0);
  });

  it('calculates entropy in bits per symbol', () => {
    expect(shannonEntropy('AAAA')).toBe(0);
    expect(shannonEntropy('ABAB')).toBe(1);
  });

  it('returns a complete sorted frequency table', () => {
    const frequencies = letterFrequencies('AAABBC');
    expect(frequencies).toHaveLength(26);
    expect(frequencies[0]).toMatchObject({ letter: 'A', count: 3, percentage: 50 });
  });

  it('reports one-based repeated n-gram positions and distances', () => {
    const repeat = repeatedNgrams('ABCZZABC', 3, 3).find(
      (item) => item.value === 'ABC',
    );
    expect(repeat).toEqual({ value: 'ABC', positions: [1, 6], distances: [5] });
  });

  it('derives standard Vigenere keystream values', () => {
    expect(deriveKeystream('LXFOPVEFRNHR', 'ATTACKATDAWN', STANDARD_ALPHABET)).toBe(
      'LEMONLEMONLE',
    );
  });

  it('fingerprints all 97 K4 letters', () => {
    const fingerprint = textFingerprint(K4_CIPHER);
    expect(fingerprint.letters).toBe(97);
    expect(fingerprint.unique).toBeGreaterThan(20);
    expect(fingerprint.ic).toBeGreaterThan(0);
  });

  it('marks periodic IC unavailable when no residue class has two letters', () => {
    expect(Number.isNaN(averagePeriodicIc('AAAA', 4))).toBe(true);
    expect(averagePeriodicIc('AAAA', 2)).toBe(1);
  });
});
