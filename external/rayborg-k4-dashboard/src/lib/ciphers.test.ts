import { describe, expect, it } from 'vitest';
import {
  K1_CIPHER,
  K1_PLAIN,
  K2_CIPHER,
  K2_CORRECTED_CIPHER,
  K2_PHYSICAL_PLAIN,
  K2_PLAIN,
  K3_CIPHER,
  K3_PLAIN,
  KRYPTOS_ALPHABET,
} from '../data/kryptos';
import {
  atbashTransform,
  caesarTransform,
  columnarDecrypt,
  columnarEncrypt,
  k3Decrypt,
  k3Encrypt,
  normalizeLetters,
  polyalphabeticTransform,
  railFenceDecrypt,
  railFenceEncrypt,
  reverseTransform,
  rotationalRouteDecrypt,
  rotationalRouteEncrypt,
} from './ciphers';

describe('polyalphabetic transforms', () => {
  it('decrypts K1 exactly with the keyed alphabet', () => {
    const actual = polyalphabeticTransform(
      K1_CIPHER,
      'PALIMPSEST',
      KRYPTOS_ALPHABET,
    );
    expect(normalizeLetters(actual)).toBe(K1_PLAIN);
  });

  it('reproduces the physical K2 IDBYROWS artifact', () => {
    const actual = polyalphabeticTransform(
      K2_CIPHER,
      'ABSCISSA',
      KRYPTOS_ALPHABET,
    );
    expect(normalizeLetters(actual)).toBe(K2_PHYSICAL_PLAIN);
  });

  it('recovers intended K2 after the virtual S insertion', () => {
    const actual = polyalphabeticTransform(
      K2_CORRECTED_CIPHER,
      'ABSCISSA',
      KRYPTOS_ALPHABET,
    );
    expect(normalizeLetters(actual)).toBe(K2_PLAIN);
    expect(normalizeLetters(actual).endsWith('WESTXLAYERTWO')).toBe(true);
  });

  it.each(['vigenere', 'beaufort', 'variant-beaufort'] as const)(
    'round trips the %s variant',
    (variant) => {
      const encrypted = polyalphabeticTransform(
        'DEFENDTHEEASTWALL',
        'CLOCK',
        KRYPTOS_ALPHABET,
        variant,
        'encrypt',
      );
      expect(
        polyalphabeticTransform(
          encrypted,
          'CLOCK',
          KRYPTOS_ALPHABET,
          variant,
          'decrypt',
        ),
      ).toBe('DEFENDTHEEASTWALL');
    },
  );
});

describe('K3 rotational route', () => {
  it('decrypts every K3 letter', () => {
    expect(k3Decrypt(K3_CIPHER)).toBe(K3_PLAIN);
  });

  it('re-enciphers to the canonical K3 transcription', () => {
    expect(k3Encrypt(K3_PLAIN)).toBe(normalizeLetters(K3_CIPHER));
  });
});

describe('general classical primitives', () => {
  it('round trips Caesar', () => {
    const encrypted = caesarTransform('ATTACK AT DAWN', 11, 'encrypt');
    expect(caesarTransform(encrypted, 11, 'decrypt')).toBe('ATTACK AT DAWN');
  });

  it('uses Atbash as an involution', () => {
    expect(atbashTransform(atbashTransform('KRYPTOS'))).toBe('KRYPTOS');
  });

  it('uses reversal as an involution', () => {
    expect(reverseTransform(reverseTransform('K4? OBKR'))).toBe('K4? OBKR');
  });

  it('round trips rail fence', () => {
    const plain = 'WEAREDISCOVEREDFLEEATONCE';
    expect(railFenceDecrypt(railFenceEncrypt(plain, 4), 4)).toBe(plain);
  });

  it('round trips uneven columnar transposition with duplicate key letters', () => {
    const plain = 'THISISANUNEVENLENGTHMESSAGE';
    expect(columnarDecrypt(columnarEncrypt(plain, 'BERLIN'), 'BERLIN')).toBe(plain);
  });

  it('round trips a rotational route', () => {
    const plain = 'ABCDEFGHIJKLMNOPQRSTUVWX';
    const encrypted = rotationalRouteEncrypt(plain, 4, 6);
    expect(rotationalRouteDecrypt(encrypted, 4, 6)).toBe(plain);
  });

  it('rejects an incompatible route grid', () => {
    expect(() => rotationalRouteEncrypt('ABCDE', 2, 3)).toThrow(/does not fit/);
  });

  it('rejects fractional and non-finite route dimensions', () => {
    expect(() => rotationalRouteEncrypt('ABCDEF', 1.5, 4)).toThrow(/integer/);
    expect(() => rotationalRouteDecrypt('ABCDEF', Number.NaN, 6)).toThrow(/integer/);
  });

  it('rejects invalid rail counts', () => {
    expect(() => railFenceEncrypt('ABCDEF', 1.5)).toThrow(/integer/);
    expect(() => railFenceDecrypt('ABCDEF', Number.NaN)).toThrow(/integer/);
  });
});
