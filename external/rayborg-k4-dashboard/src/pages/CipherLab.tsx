import {
  ArrowDownUp,
  Check,
  Clipboard,
  FlaskConical,
  Plus,
  RotateCcw,
  TriangleAlert,
} from 'lucide-react';
import { useState } from 'react';
import {
  K1_CIPHER,
  K2_CIPHER,
  K2_CORRECTED_CIPHER,
  K3_CIPHER,
  K4_CIPHER,
  KRYPTOS_ALPHABET,
  STANDARD_ALPHABET,
} from '../data/kryptos';
import {
  letterFrequencies,
  periodicIcSeries,
  repeatedNgrams,
  textFingerprint,
} from '../lib/analysis';
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
  type CipherOperation,
  type PolyalphabeticVariant,
} from '../lib/ciphers';
import type { Experiment, SectionId } from '../types';
import { contentFingerprint } from '../lib/validation';

type LabMethod =
  | 'keyed-vigenere'
  | 'vigenere'
  | 'beaufort'
  | 'variant-beaufort'
  | 'caesar'
  | 'atbash'
  | 'reverse'
  | 'rail-fence'
  | 'columnar'
  | 'grid-route'
  | 'k3-route';

interface CipherLabProps {
  addExperiment: (experiment: Experiment) => void;
}

const METHOD_LABELS: Record<LabMethod, string> = {
  'keyed-vigenere': 'Kryptos keyed Vigenere',
  vigenere: 'Vigenere',
  beaufort: 'Beaufort',
  'variant-beaufort': 'Variant Beaufort',
  caesar: 'Caesar shift',
  atbash: 'Atbash',
  reverse: 'Reverse',
  'rail-fence': 'Rail fence',
  columnar: 'Columnar transposition',
  'grid-route': 'Rotational grid route',
  'k3-route': 'K3 two-stage route',
};

const PRESETS = {
  K1: K1_CIPHER,
  K2: K2_CIPHER,
  'K2 corrected': K2_CORRECTED_CIPHER,
  K3: K3_CIPHER,
  K4: K4_CIPHER,
};
type PresetId = keyof typeof PRESETS | 'Custom';

const METHODS_USING_KEY: LabMethod[] = [
  'keyed-vigenere',
  'vigenere',
  'beaufort',
  'variant-beaufort',
  'columnar',
];
const METHODS_USING_SELECTED_ALPHABET: LabMethod[] = [
  'vigenere',
  'beaufort',
  'variant-beaufort',
  'caesar',
  'atbash',
];

export function CipherLab({ addExperiment }: CipherLabProps) {
  const [preset, setPreset] = useState<PresetId>('K4');
  const [input, setInput] = useState(K4_CIPHER);
  const [method, setMethod] = useState<LabMethod>('keyed-vigenere');
  const [operation, setOperation] = useState<CipherOperation>('decrypt');
  const [key, setKey] = useState('KRYPTOS');
  const [alphabetMode, setAlphabetMode] = useState<'standard' | 'kryptos' | 'custom'>('kryptos');
  const [customAlphabet, setCustomAlphabet] = useState(KRYPTOS_ALPHABET);
  const [shift, setShift] = useState(3);
  const [rails, setRails] = useState(3);
  const [rows, setRows] = useState(1);
  const [columns, setColumns] = useState(97);
  const [copied, setCopied] = useState(false);
  const [logged, setLogged] = useState(false);
  const [analysisTab, setAnalysisTab] = useState<'frequency' | 'periods' | 'repeats'>('frequency');

  const customLetters = customAlphabet.toUpperCase().replace(/[^A-Z]/g, '');
  const customIsValid =
    customLetters.length === 26 && new Set(customLetters).size === 26;
  const alphabet =
    alphabetMode === 'standard'
      ? STANDARD_ALPHABET
      : alphabetMode === 'kryptos'
        ? KRYPTOS_ALPHABET
        : customLetters;
  const methodUsesKey = METHODS_USING_KEY.includes(method);
  const methodUsesAlphabet = METHODS_USING_SELECTED_ALPHABET.includes(method);
  const effectiveAlphabet =
    method === 'keyed-vigenere'
      ? KRYPTOS_ALPHABET
      : methodUsesAlphabet
        ? alphabet
        : STANDARD_ALPHABET;
  const stripsNonletters = ['rail-fence', 'columnar', 'grid-route', 'k3-route'].includes(method);
  const effectiveInput = stripsNonletters ? normalizeLetters(input, STANDARD_ALPHABET) : input;

  let output = '';
  let error = '';
  const transformStarted = performance.now();
  try {
    if (methodUsesAlphabet && alphabetMode === 'custom' && !customIsValid) {
      throw new Error('Custom alphabet must be a unique 26-letter A–Z permutation.');
    }
    const normalized = normalizeLetters(input, STANDARD_ALPHABET);
    switch (method) {
      case 'keyed-vigenere':
        output = polyalphabeticTransform(
          input,
          key,
          KRYPTOS_ALPHABET,
          'vigenere',
          operation,
        );
        break;
      case 'vigenere':
      case 'beaufort':
      case 'variant-beaufort':
        output = polyalphabeticTransform(
          input,
          key,
          alphabet,
          method as PolyalphabeticVariant,
          operation,
        );
        break;
      case 'caesar':
        output = caesarTransform(input, shift, operation, alphabet);
        break;
      case 'atbash':
        output = atbashTransform(input, alphabet);
        break;
      case 'reverse':
        output = reverseTransform(input);
        break;
      case 'rail-fence':
        output =
          operation === 'encrypt'
            ? railFenceEncrypt(normalized, rails)
            : railFenceDecrypt(normalized, rails);
        break;
      case 'columnar':
        output =
          operation === 'encrypt'
            ? columnarEncrypt(normalized, key)
            : columnarDecrypt(normalized, key);
        break;
      case 'grid-route':
        output =
          operation === 'encrypt'
            ? rotationalRouteEncrypt(normalized, rows, columns)
            : rotationalRouteDecrypt(normalized, rows, columns);
        break;
      case 'k3-route':
        output = operation === 'encrypt' ? k3Encrypt(normalized) : k3Decrypt(normalized);
        break;
    }
  } catch (caught) {
    error = caught instanceof Error ? caught.message : 'Unable to transform this input.';
  }
  const transformElapsedMs = performance.now() - transformStarted;

  const fingerprint = textFingerprint(output);
  const frequencies = letterFrequencies(output);
  const periods = periodicIcSeries(output, 16);
  const repeats = repeatedNgrams(output).slice(0, 18);
  const maxFrequency = Math.max(...frequencies.map((item) => item.count), 1);
  const estimablePeriodIcs = periods
    .map((item) => item.ic)
    .filter(Number.isFinite);
  const maxPeriodIc = Math.max(...estimablePeriodIcs, 0.001);

  const loadPreset = (next: keyof typeof PRESETS) => {
    setPreset(next);
    setInput(PRESETS[next]);
    setLogged(false);
    if (next === 'K1') {
      setMethod('keyed-vigenere');
      setKey('PALIMPSEST');
      setOperation('decrypt');
    } else if (next === 'K2' || next === 'K2 corrected') {
      setMethod('keyed-vigenere');
      setKey('ABSCISSA');
      setOperation('decrypt');
    } else if (next === 'K3') {
      setMethod('k3-route');
      setOperation('decrypt');
    }
  };

  const swapInputOutput = () => {
    if (!output || error) return;
    setInput(output);
    setPreset('Custom');
    setOperation((current) => (current === 'decrypt' ? 'encrypt' : 'decrypt'));
  };

  const copyOutput = async () => {
    await navigator.clipboard.writeText(output);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1400);
  };

  const logRun = () => {
    if (!output || error) return;
    const section: SectionId | 'custom' =
      preset === 'K1' || preset === 'K2' || preset === 'K3' || preset === 'K4'
        ? preset
        : preset === 'K2 corrected'
          ? 'K2'
          : 'custom';
    addExperiment({
      id: crypto.randomUUID(),
      createdAt: new Date().toISOString(),
      title: `${preset} / ${METHOD_LABELS[method]}`,
      section,
      method: METHOD_LABELS[method],
      operation,
      key,
      alphabet: effectiveAlphabet,
      input,
      output,
      notes: `shift=${shift}; rails=${rails}; grid=${rows}x${columns}`,
      status: 'tested',
      provenance: {
        appVersion: '0.1.0',
        inputFingerprint: contentFingerprint(effectiveInput),
        indexConvention:
          section === 'K4' ? 'one-based local K4 positions 1–97' : 'section-local letters',
        parameters: {
          key,
          alphabet: effectiveAlphabet,
          shift: String(shift),
          rails: String(rails),
          rows: String(rows),
          columns: String(columns),
          punctuation: stripsNonletters
            ? 'removed before transposition'
            : method === 'reverse'
              ? 'preserved and reversed with the full input'
              : 'preserved; does not advance polyalphabetic keys',
          effectiveInput: stripsNonletters ? 'normalized A–Z letters' : 'raw input',
        },
        searchSpace: 'single deterministic transformation',
        corpus: 'not used',
        scoring: 'not used',
        seed: 'not applicable',
        elapsedMs: transformElapsedMs,
        hardware: navigator.userAgent,
        candidatesTested: 1,
        holdout: 'not applicable to direct transformation',
        negativeControl: 'not run',
      },
    });
    setLogged(true);
    window.setTimeout(() => setLogged(false), 1600);
  };

  return (
    <div className="page-stack lab-page">
      <header className="page-header">
        <div>
          <span className="eyebrow">LIVE TRANSFORMATION DESK</span>
          <h1>Cipher lab</h1>
          <p>
            Auditable classical primitives with explicit alphabets, key advancement,
            direction and grid parameters.
          </p>
        </div>
        <div className="header-token">
          <FlaskConical size={18} />
          <span>All transforms run in this browser</span>
        </div>
      </header>

      <section className="lab-layout">
        <div className="panel lab-controls">
          <div className="control-section">
            <label className="field-label" htmlFor="preset">Source text</label>
            <div className="preset-row" id="preset">
              {(Object.keys(PRESETS) as Array<keyof typeof PRESETS>).map((item) => (
                <button
                  className={preset === item ? 'chip chip-active' : 'chip'}
                  key={item}
                  onClick={() => loadPreset(item)}
                  aria-pressed={preset === item}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>

          <div className="field-group">
            <label className="field-label" htmlFor="lab-method">Method</label>
            <select
              id="lab-method"
              value={method}
              onChange={(event) => setMethod(event.target.value as LabMethod)}
            >
              {Object.entries(METHOD_LABELS).map(([value, label]) => (
                <option value={value} key={value}>{label}</option>
              ))}
            </select>
          </div>

          <div className="segmented-control" aria-label="Operation">
            <button
              className={operation === 'decrypt' ? 'active' : ''}
              onClick={() => setOperation('decrypt')}
              aria-pressed={operation === 'decrypt'}
            >
              Decrypt
            </button>
            <button
              className={operation === 'encrypt' ? 'active' : ''}
              onClick={() => setOperation('encrypt')}
              aria-pressed={operation === 'encrypt'}
            >
              Encrypt
            </button>
          </div>

          {methodUsesKey && (
            <div className="field-group">
              <label className="field-label" htmlFor="lab-key">Key / keyword</label>
              <input
                id="lab-key"
                value={key}
                onChange={(event) => setKey(event.target.value.toUpperCase())}
                spellCheck={false}
              />
            </div>
          )}

          {methodUsesAlphabet && (
            <div className="field-group">
              <span className="field-label">Alphabet</span>
              <div className="radio-stack">
                <label>
                  <input
                    type="radio"
                    checked={alphabetMode === 'standard'}
                    onChange={() => setAlphabetMode('standard')}
                  />
                  <span>Standard A–Z</span>
                </label>
                <label>
                  <input
                    type="radio"
                    checked={alphabetMode === 'kryptos'}
                    onChange={() => setAlphabetMode('kryptos')}
                  />
                  <span>KRYPTOS keyed</span>
                </label>
                <label>
                  <input
                    type="radio"
                    checked={alphabetMode === 'custom'}
                    onChange={() => setAlphabetMode('custom')}
                  />
                  <span>Custom</span>
                </label>
              </div>
              {alphabetMode === 'custom' && (
                <input
                  className="mono-input"
                  value={customAlphabet}
                  onChange={(event) => setCustomAlphabet(event.target.value.toUpperCase())}
                  spellCheck={false}
                  aria-label="Custom alphabet"
                />
              )}
              <code className="alphabet-preview">{alphabet}</code>
            </div>
          )}

          {method === 'caesar' && (
            <div className="field-group">
              <label className="field-label" htmlFor="lab-shift">Shift: {shift}</label>
              <input
                id="lab-shift"
                type="range"
                min="0"
                max="25"
                value={shift}
                onChange={(event) => setShift(Number(event.target.value))}
              />
            </div>
          )}

          {method === 'rail-fence' && (
            <div className="field-group">
              <label className="field-label" htmlFor="lab-rails">Rails</label>
              <input
                id="lab-rails"
                type="number"
                min="2"
                max="24"
                value={rails}
                onChange={(event) => setRails(Number(event.target.value))}
              />
            </div>
          )}

          {method === 'grid-route' && (
            <div className="field-row">
              <div className="field-group">
                <label className="field-label" htmlFor="lab-rows">Rows</label>
                <input
                  id="lab-rows"
                  type="number"
                  min="1"
                  value={rows}
                  onChange={(event) => setRows(Number(event.target.value))}
                />
              </div>
              <div className="field-group">
                <label className="field-label" htmlFor="lab-columns">Columns</label>
                <input
                  id="lab-columns"
                  type="number"
                  min="1"
                  value={columns}
                  onChange={(event) => setColumns(Number(event.target.value))}
                />
              </div>
            </div>
          )}

          <div className="control-note">
            Non-alphabet symbols are preserved and do not advance polyalphabetic keys.
            Route tools normalize to letters first.
          </div>
        </div>

        <div className="lab-workspace">
          <section className="panel text-workbench">
            <div className="text-pane">
              <div className="pane-heading">
                <label htmlFor="lab-input">Input</label>
                <span>{normalizeLetters(input).length} letters</span>
              </div>
              <textarea
                id="lab-input"
                value={input}
                onChange={(event) => {
                  setInput(event.target.value);
                  setPreset('Custom');
                  setLogged(false);
                }}
                spellCheck={false}
              />
            </div>

            <button
              className="swap-button"
              onClick={swapInputOutput}
              title="Move output to input and reverse operation"
              aria-label="Swap input and output"
            >
              <ArrowDownUp size={18} />
            </button>

            <div className="text-pane output-pane">
              <div className="pane-heading">
                <label htmlFor="lab-output">Output</label>
                <span>{fingerprint.letters} letters</span>
              </div>
              {error ? (
                <div className="transform-error" id="lab-output">
                  <TriangleAlert size={20} />
                  <div>
                    <strong>Invalid parameters</strong>
                    <span>{error}</span>
                  </div>
                </div>
              ) : (
                <textarea id="lab-output" value={output} readOnly spellCheck={false} />
              )}
            </div>

            <div className="workbench-actions">
              <button className="button button-quiet" onClick={copyOutput} disabled={!output || !!error}>
                {copied ? <Check size={15} /> : <Clipboard size={15} />}
                {copied ? 'Copied' : 'Copy output'}
              </button>
              <button className="button button-primary" onClick={logRun} disabled={!output || !!error}>
                {logged ? <Check size={15} /> : <Plus size={15} />}
                {logged ? 'Logged' : 'Log experiment'}
              </button>
            </div>
          </section>

          <section className="diagnostic-strip">
            <div>
              <span>LETTERS</span>
              <strong>{fingerprint.letters}</strong>
            </div>
            <div>
              <span>UNIQUE</span>
              <strong>{fingerprint.unique}</strong>
            </div>
            <div>
              <span>IC</span>
              <strong>{fingerprint.ic.toFixed(4)}</strong>
            </div>
            <div>
              <span>ENTROPY</span>
              <strong>{fingerprint.entropy.toFixed(3)}</strong>
            </div>
            <div>
              <span>REPEATS</span>
              <strong>{fingerprint.repeats}</strong>
            </div>
          </section>

          <section className="panel analysis-panel">
            <div className="analysis-tabs" role="tablist" aria-label="Output analysis">
              <button role="tab" aria-selected={analysisTab === 'frequency'} className={analysisTab === 'frequency' ? 'active' : ''} onClick={() => setAnalysisTab('frequency')}>Frequency</button>
              <button role="tab" aria-selected={analysisTab === 'periods'} className={analysisTab === 'periods' ? 'active' : ''} onClick={() => setAnalysisTab('periods')}>Period IC</button>
              <button role="tab" aria-selected={analysisTab === 'repeats'} className={analysisTab === 'repeats' ? 'active' : ''} onClick={() => setAnalysisTab('repeats')}>Repeated n-grams</button>
            </div>

            {analysisTab === 'frequency' && (
              <div className="frequency-chart" role="tabpanel">
                {frequencies.map((item) => (
                  <div className="frequency-item" key={item.letter}>
                    <span>{item.letter}</span>
                    <div className="frequency-track">
                      <i style={{ height: `${(item.count / maxFrequency) * 100}%` }} />
                    </div>
                    <small>{item.count}</small>
                  </div>
                ))}
              </div>
            )}

            {analysisTab === 'periods' && (
              <div className="period-chart" role="tabpanel">
                {periods.map((item) => (
                  <div className="period-item" key={item.period}>
                    <span>{item.period}</span>
                    <div className="period-track">
                      <i style={{ width: Number.isFinite(item.ic) ? `${(item.ic / maxPeriodIc) * 100}%` : '0%' }} />
                    </div>
                    <code>{Number.isFinite(item.ic) ? item.ic.toFixed(4) : '—'}</code>
                  </div>
                ))}
              </div>
            )}

            {analysisTab === 'repeats' && (
              <div className="repeat-table" role="tabpanel">
                {repeats.length ? repeats.map((item) => (
                  <div key={`${item.value}-${item.positions.join('-')}`}>
                    <code>{item.value}</code>
                    <span>positions {item.positions.join(', ')}</span>
                    <span>distances {item.distances.join(', ')}</span>
                  </div>
                )) : (
                  <div className="empty-inline"><RotateCcw size={16} /> No repeated 2–4 grams in this output.</div>
                )}
              </div>
            )}
          </section>
        </div>
      </section>
    </div>
  );
}
