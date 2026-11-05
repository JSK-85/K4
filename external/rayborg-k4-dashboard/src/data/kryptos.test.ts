import { describe, expect, it } from 'vitest';
import {
  K1_CIPHER,
  K2_CIPHER,
  K2_CORRECTED_CIPHER,
  K3_CIPHER,
  K4_CIPHER,
  K4_CRIBS,
  K4_KNOWN_PLAIN,
  KRYPTOS_ALPHABET,
} from './kryptos';
import { normalizeLetters } from '../lib/ciphers';

describe('canonical Kryptos data', () => {
  it('uses a complete 26-character keyed alphabet', () => {
    expect(KRYPTOS_ALPHABET).toHaveLength(26);
    expect(new Set(KRYPTOS_ALPHABET).size).toBe(26);
  });

  it('preserves canonical section letter counts', () => {
    expect(normalizeLetters(K1_CIPHER)).toHaveLength(63);
    expect(normalizeLetters(K2_CIPHER)).toHaveLength(369);
    expect(normalizeLetters(K2_CORRECTED_CIPHER)).toHaveLength(370);
    expect(normalizeLetters(K3_CIPHER)).toHaveLength(336);
    expect(K4_CIPHER).toHaveLength(97);
  });

  it('freezes the complete 97-letter K4 transcription', () => {
    expect(K4_CIPHER).toBe(
      'OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR',
    );
  });

  it('assigns all four question marks before K4', () => {
    expect((K2_CIPHER.match(/\?/g) ?? [])).toHaveLength(3);
    expect((K3_CIPHER.match(/\?/g) ?? [])).toHaveLength(1);
    expect(K4_CIPHER).not.toContain('?');
  });

  it('locks every public crib to the declared ciphertext positions', () => {
    for (const crib of K4_CRIBS) {
      expect(K4_CIPHER.slice(crib.start - 1, crib.end)).toBe(crib.cipher);
      expect(crib.end - crib.start + 1).toBe(crib.plain.length);
    }
  });

  it('contains exactly 24 confirmed plaintext positions', () => {
    expect(K4_KNOWN_PLAIN.filter(Boolean)).toHaveLength(24);
    expect(K4_KNOWN_PLAIN.slice(21, 34).join('')).toBe('EASTNORTHEAST');
    expect(K4_KNOWN_PLAIN.slice(63, 74).join('')).toBe('BERLINCLOCK');
  });
});
