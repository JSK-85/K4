import { STANDARD_ALPHABET } from '../data/kryptos';

export type PolyalphabeticVariant = 'vigenere' | 'beaufort' | 'variant-beaufort';
export type CipherOperation = 'encrypt' | 'decrypt';

export function keyedAlphabet(keyword: string, base = STANDARD_ALPHABET): string {
  const cleaned = normalizeLetters(keyword, base);
  return [...new Set((cleaned + base).split(''))].join('');
}

export function normalizeLetters(text: string, alphabet = STANDARD_ALPHABET): string {
  const allowed = new Set(alphabet.toUpperCase());
  return text
    .toUpperCase()
    .split('')
    .filter((char) => allowed.has(char))
    .join('');
}

function modulo(value: number, modulus: number): number {
  return ((value % modulus) + modulus) % modulus;
}

function requirePositiveInteger(value: number, label: string, minimum = 1): void {
  if (!Number.isFinite(value) || !Number.isInteger(value) || value < minimum) {
    throw new Error(`${label} must be an integer of at least ${minimum}.`);
  }
}

export function polyalphabeticTransform(
  text: string,
  key: string,
  alphabet = STANDARD_ALPHABET,
  variant: PolyalphabeticVariant = 'vigenere',
  operation: CipherOperation = 'decrypt',
): string {
  const upperAlphabet = [...new Set(alphabet.toUpperCase())].join('');
  const cleanKey = normalizeLetters(key, upperAlphabet);
  if (upperAlphabet.length < 2 || !cleanKey) return text.toUpperCase();

  let keyIndex = 0;
  return text
    .toUpperCase()
    .split('')
    .map((char) => {
      const value = upperAlphabet.indexOf(char);
      if (value === -1) return char;

      const keyValue = upperAlphabet.indexOf(cleanKey[keyIndex % cleanKey.length]);
      keyIndex += 1;
      let transformed: number;

      if (variant === 'beaufort') {
        transformed = keyValue - value;
      } else if (variant === 'variant-beaufort') {
        transformed =
          operation === 'encrypt' ? value - keyValue : value + keyValue;
      } else {
        transformed =
          operation === 'encrypt' ? value + keyValue : value - keyValue;
      }

      return upperAlphabet[modulo(transformed, upperAlphabet.length)];
    })
    .join('');
}

export function caesarTransform(
  text: string,
  shift: number,
  operation: CipherOperation = 'decrypt',
  alphabet = STANDARD_ALPHABET,
): string {
  const appliedShift = operation === 'decrypt' ? -shift : shift;
  return text
    .toUpperCase()
    .split('')
    .map((char) => {
      const index = alphabet.indexOf(char);
      return index === -1
        ? char
        : alphabet[modulo(index + appliedShift, alphabet.length)];
    })
    .join('');
}

export function atbashTransform(
  text: string,
  alphabet = STANDARD_ALPHABET,
): string {
  const reversed = alphabet.split('').reverse().join('');
  return text
    .toUpperCase()
    .split('')
    .map((char) => {
      const index = alphabet.indexOf(char);
      return index === -1 ? char : reversed[index];
    })
    .join('');
}

export function reverseTransform(text: string): string {
  return text.split('').reverse().join('');
}

export function railFenceEncrypt(text: string, rails: number): string {
  requirePositiveInteger(rails, 'Rails', 2);
  if (rails >= text.length) return text;
  const rows = Array.from({ length: rails }, () => [] as string[]);
  let row = 0;
  let direction = 1;
  for (const char of text) {
    rows[row].push(char);
    if (row === 0) direction = 1;
    if (row === rails - 1) direction = -1;
    row += direction;
  }
  return rows.flat().join('');
}

export function railFenceDecrypt(text: string, rails: number): string {
  requirePositiveInteger(rails, 'Rails', 2);
  if (rails >= text.length) return text;
  const pattern: number[] = [];
  let row = 0;
  let direction = 1;
  for (let index = 0; index < text.length; index += 1) {
    pattern.push(row);
    if (row === 0) direction = 1;
    if (row === rails - 1) direction = -1;
    row += direction;
  }

  const counts = Array<number>(rails).fill(0);
  pattern.forEach((rail) => (counts[rail] += 1));
  const rows: string[][] = [];
  let offset = 0;
  counts.forEach((count) => {
    rows.push(text.slice(offset, offset + count).split(''));
    offset += count;
  });
  const cursors = Array<number>(rails).fill(0);
  return pattern.map((rail) => rows[rail][cursors[rail]++]).join('');
}

export function rotationalRouteEncrypt(
  text: string,
  rows: number,
  columns: number,
): string {
  requirePositiveInteger(rows, 'Rows');
  requirePositiveInteger(columns, 'Columns');
  if (rows * columns !== text.length) {
    throw new Error(`Grid ${rows}x${columns} does not fit ${text.length} characters.`);
  }
  let output = '';
  for (let column = 0; column < columns; column += 1) {
    for (let row = rows - 1; row >= 0; row -= 1) {
      output += text[row * columns + column];
    }
  }
  return output;
}

export function rotationalRouteDecrypt(
  text: string,
  rows: number,
  columns: number,
): string {
  requirePositiveInteger(rows, 'Rows');
  requirePositiveInteger(columns, 'Columns');
  if (rows * columns !== text.length) {
    throw new Error(`Grid ${rows}x${columns} does not fit ${text.length} characters.`);
  }
  const grid = Array<string>(text.length);
  let inputIndex = 0;
  for (let column = 0; column < columns; column += 1) {
    for (let row = rows - 1; row >= 0; row -= 1) {
      grid[row * columns + column] = text[inputIndex++];
    }
  }
  return grid.join('');
}

export function k3Encrypt(plainText: string): string {
  const normalized = normalizeLetters(plainText);
  const firstStage = rotationalRouteEncrypt(normalized, 8, 42);
  return rotationalRouteEncrypt(firstStage, 24, 14);
}

export function k3Decrypt(cipherText: string): string {
  const normalized = normalizeLetters(cipherText);
  const secondStage = rotationalRouteDecrypt(normalized, 24, 14);
  return rotationalRouteDecrypt(secondStage, 8, 42);
}

export function columnarEncrypt(text: string, keyword: string): string {
  const key = normalizeLetters(keyword);
  if (!key) return text;
  const order = key
    .split('')
    .map((char, index) => ({ char, index }))
    .sort((a, b) => a.char.localeCompare(b.char) || a.index - b.index);
  return order
    .map(({ index }) => {
      let column = '';
      for (let cursor = index; cursor < text.length; cursor += key.length) {
        column += text[cursor];
      }
      return column;
    })
    .join('');
}

export function columnarDecrypt(text: string, keyword: string): string {
  const key = normalizeLetters(keyword);
  if (!key) return text;
  const width = key.length;
  const baseHeight = Math.floor(text.length / width);
  const longColumns = text.length % width;
  const order = key
    .split('')
    .map((char, index) => ({ char, index }))
    .sort((a, b) => a.char.localeCompare(b.char) || a.index - b.index);
  const columns = Array<string>(width).fill('');
  let offset = 0;
  for (const { index } of order) {
    const height = baseHeight + (index < longColumns ? 1 : 0);
    columns[index] = text.slice(offset, offset + height);
    offset += height;
  }
  let output = '';
  for (let row = 0; row <= baseHeight; row += 1) {
    for (let column = 0; column < width; column += 1) {
      output += columns[column][row] ?? '';
    }
  }
  return output;
}
