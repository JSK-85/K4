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
import type { ShadowRun } from '../types';
import { k3Decrypt, k3Encrypt, normalizeLetters, polyalphabeticTransform } from './ciphers';

export function punctuationLayout(text: string): string {
  let letterOffset = 0;
  const punctuation: string[] = [];
  for (const char of text.toUpperCase()) {
    if (/[A-Z]/.test(char)) letterOffset += 1;
    else if (!/\s/.test(char)) punctuation.push(`${letterOffset}:${char}`);
  }
  return punctuation.join('|');
}

function run(
  definition: Omit<ShadowRun, 'passed'>,
  punctuationSource?: string,
): ShadowRun {
  return {
    ...definition,
    passed:
      normalizeLetters(definition.actual) === normalizeLetters(definition.expected) &&
      (!punctuationSource ||
        punctuationLayout(definition.actual) === punctuationLayout(punctuationSource)),
  };
}

export function createShadowRuns(): ShadowRun[] {
  const k1Actual = polyalphabeticTransform(
    K1_CIPHER,
    'PALIMPSEST',
    KRYPTOS_ALPHABET,
  );
  const k2PhysicalActual = polyalphabeticTransform(
    K2_CIPHER,
    'ABSCISSA',
    KRYPTOS_ALPHABET,
  );
  const k2CorrectedActual = polyalphabeticTransform(
    K2_CORRECTED_CIPHER,
    'ABSCISSA',
    KRYPTOS_ALPHABET,
  );
  const k3Actual = k3Decrypt(K3_CIPHER);
  const k3RoundTrip = k3Encrypt(K3_PLAIN);

  return [
    run({
      id: 'k1-decrypt',
      section: 'K1',
      title: 'Recover K1 plaintext',
      method: 'Keyed-alphabet Vigenere / Quagmire III variant',
      parameters: { key: 'PALIMPSEST', alphabet: KRYPTOS_ALPHABET },
      expected: K1_PLAIN,
      actual: k1Actual,
      detail: 'Exercises mixed-alphabet subtraction and nonletter preservation.',
    }),
    run({
      id: 'k2-physical',
      section: 'K2',
      title: 'Reproduce the physical-screen artifact',
      method: 'Keyed-alphabet Vigenere / Quagmire III variant',
      parameters: {
        key: 'ABSCISSA',
        alphabet: KRYPTOS_ALPHABET,
        ciphertext: '369 physical letters',
      },
      expected: K2_PHYSICAL_PLAIN,
      actual: k2PhysicalActual,
      detail: 'The uncorrected screen predictably ends IDBYROWS.',
    }, K2_CIPHER),
    run({
      id: 'k2-corrected',
      section: 'K2',
      title: 'Restore the intended K2 ending',
      method: 'Virtual-S correction plus keyed-alphabet Vigenere',
      parameters: {
        key: 'ABSCISSA',
        insertion: 'ciphertext S, ninth position from end',
      },
      expected: K2_PLAIN,
      actual: k2CorrectedActual,
      detail: 'Restored key alignment yields WESTXLAYERTWO exactly.',
    }, K2_CORRECTED_CIPHER),
    run({
      id: 'k3-decrypt',
      section: 'K3',
      title: 'Invert the K3 route',
      method: 'Two-stage rotational route transposition',
      parameters: { stage1: 'inverse 24x14', stage2: 'inverse 8x42' },
      expected: K3_PLAIN,
      actual: k3Actual,
      detail: 'Recovers all 336 plaintext letters including DESPARATLY and terminal Q.',
    }),
    run({
      id: 'k3-encrypt',
      section: 'K3',
      title: 'Re-encipher K3 exactly',
      method: 'Two-stage rotational route transposition',
      parameters: { stage1: '8x42', stage2: '24x14' },
      expected: normalizeLetters(K3_CIPHER),
      actual: k3RoundTrip,
      detail: 'A stronger round-trip check than plaintext substring matching.',
    }),
  ];
}
