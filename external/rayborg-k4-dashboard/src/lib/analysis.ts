import { STANDARD_ALPHABET } from '../data/kryptos';
import { normalizeLetters } from './ciphers';

export interface LetterFrequency {
  letter: string;
  count: number;
  percentage: number;
}

export interface RepeatedNgram {
  value: string;
  positions: number[];
  distances: number[];
}

export function letterFrequencies(text: string): LetterFrequency[] {
  const normalized = normalizeLetters(text);
  const counts = Object.fromEntries(
    STANDARD_ALPHABET.split('').map((letter) => [letter, 0]),
  ) as Record<string, number>;
  for (const char of normalized) counts[char] += 1;
  return STANDARD_ALPHABET.split('')
    .map((letter) => ({
      letter,
      count: counts[letter],
      percentage: normalized.length
        ? (counts[letter] / normalized.length) * 100
        : 0,
    }))
    .sort((a, b) => b.count - a.count || a.letter.localeCompare(b.letter));
}

export function indexOfCoincidence(text: string): number {
  const normalized = normalizeLetters(text);
  if (normalized.length < 2) return 0;
  const frequencies = letterFrequencies(normalized);
  const numerator = frequencies.reduce(
    (sum, item) => sum + item.count * (item.count - 1),
    0,
  );
  return numerator / (normalized.length * (normalized.length - 1));
}

export function shannonEntropy(text: string): number {
  const normalized = normalizeLetters(text);
  if (!normalized.length) return 0;
  return letterFrequencies(normalized).reduce((entropy, item) => {
    if (!item.count) return entropy;
    const probability = item.count / normalized.length;
    return entropy - probability * Math.log2(probability);
  }, 0);
}

export function repeatedNgrams(
  text: string,
  minLength = 2,
  maxLength = 4,
): RepeatedNgram[] {
  const normalized = normalizeLetters(text);
  const groups = new Map<string, number[]>();
  for (let size = minLength; size <= maxLength; size += 1) {
    for (let index = 0; index <= normalized.length - size; index += 1) {
      const value = normalized.slice(index, index + size);
      const positions = groups.get(value) ?? [];
      positions.push(index + 1);
      groups.set(value, positions);
    }
  }
  return [...groups.entries()]
    .filter(([, positions]) => positions.length > 1)
    .map(([value, positions]) => ({
      value,
      positions,
      distances: positions.slice(1).map((position, index) => position - positions[index]),
    }))
    .sort(
      (a, b) =>
        b.value.length - a.value.length ||
        b.positions.length - a.positions.length ||
        a.value.localeCompare(b.value),
    );
}

export function averagePeriodicIc(text: string, period: number): number {
  const normalized = normalizeLetters(text);
  if (!normalized || !Number.isInteger(period) || period < 1) return Number.NaN;
  const columns = Array.from({ length: period }, () => '');
  normalized.split('').forEach((char, index) => {
    columns[index % period] += char;
  });
  const estimable = columns.filter((column) => column.length >= 2);
  if (!estimable.length) return Number.NaN;
  return (
    estimable.reduce((sum, column) => sum + indexOfCoincidence(column), 0) /
    estimable.length
  );
}

export function periodicIcSeries(text: string, maxPeriod = 16) {
  return Array.from({ length: maxPeriod }, (_, index) => ({
    period: index + 1,
    ic: averagePeriodicIc(text, index + 1),
  }));
}

export function deriveKeystream(
  cipherText: string,
  plainText: string,
  alphabet = STANDARD_ALPHABET,
): string {
  const cipher = normalizeLetters(cipherText, alphabet);
  const plain = normalizeLetters(plainText, alphabet);
  const length = Math.min(cipher.length, plain.length);
  let output = '';
  for (let index = 0; index < length; index += 1) {
    const difference =
      (alphabet.indexOf(cipher[index]) - alphabet.indexOf(plain[index]) + alphabet.length) %
      alphabet.length;
    output += alphabet[difference];
  }
  return output;
}

export function coincidenceCount(a: string, b: string): number {
  const left = normalizeLetters(a);
  const right = normalizeLetters(b);
  const length = Math.min(left.length, right.length);
  let matches = 0;
  for (let index = 0; index < length; index += 1) {
    if (left[index] === right[index]) matches += 1;
  }
  return matches;
}

export function textFingerprint(text: string) {
  const normalized = normalizeLetters(text);
  return {
    letters: normalized.length,
    unique: new Set(normalized).size,
    ic: indexOfCoincidence(normalized),
    entropy: shannonEntropy(normalized),
    repeats: repeatedNgrams(normalized).length,
  };
}
