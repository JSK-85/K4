import {
  Check,
  CircleAlert,
  ExternalLink,
  KeyRound,
  Plus,
  ShieldCheck,
} from 'lucide-react';
import { useState } from 'react';
import { K4Strip } from '../components/K4Strip';
import {
  K4_CIPHER,
  K4_CRIBS,
  K4_KNOWN_PLAIN,
  KRYPTOS_ALPHABET,
  STANDARD_ALPHABET,
} from '../data/kryptos';
import { RESEARCH_SOURCES } from '../data/research';
import { deriveKeystream } from '../lib/analysis';
import { normalizeLetters } from '../lib/ciphers';
import type { Experiment } from '../types';
import { contentFingerprint } from '../lib/validation';

interface CribBenchProps {
  addExperiment: (experiment: Experiment) => void;
}

export function CribBench({ addExperiment }: CribBenchProps) {
  const [start, setStart] = useState(1);
  const [plainText, setPlainText] = useState('');
  const [alphabetMode, setAlphabetMode] = useState<'standard' | 'kryptos'>('standard');
  const [logged, setLogged] = useState(false);

  const plain = normalizeLetters(plainText).slice(0, K4_CIPHER.length - start + 1);
  const cipher = K4_CIPHER.slice(start - 1, start - 1 + plain.length);
  const alphabet = alphabetMode === 'standard' ? STANDARD_ALPHABET : KRYPTOS_ALPHABET;
  const keyStream = deriveKeystream(cipher, plain, alphabet);
  const end = plain.length ? start + plain.length - 1 : start;
  const conflicts = plain.split('').flatMap((char, index) => {
    const known = K4_KNOWN_PLAIN[start - 1 + index];
    return known && known !== char
      ? [{ position: start + index, expected: known, supplied: char }]
      : [];
  });

  const logCrib = () => {
    if (!plain) return;
    addExperiment({
      id: crypto.randomUUID(),
      createdAt: new Date().toISOString(),
      title: `K4 crib ${start}–${end}: ${plain}`,
      section: 'K4',
      method: 'Vigenere crib-derived keystream',
      operation: 'diagnose',
      key: keyStream,
      alphabet,
      input: cipher,
      output: keyStream,
      notes: conflicts.length
        ? `${conflicts.length} conflict(s) with confirmed public plaintext.`
        : 'No conflicts with confirmed public plaintext positions.',
      status: conflicts.length ? 'rejected' : 'tested',
      provenance: {
        appVersion: '0.1.0',
        inputFingerprint: contentFingerprint(cipher),
        indexConvention: 'one-based local K4 positions 1–97',
        parameters: {
          start: String(start),
          end: String(end),
          proposedPlaintext: plain,
          alphabet,
          arithmetic: 'cipher minus plaintext modulo alphabet length',
        },
        searchSpace: 'single fixed-position crib diagnostic',
        corpus: 'not used',
        scoring: 'exact positional comparison',
        seed: 'not applicable',
        elapsedMs: 0,
        hardware: navigator.userAgent,
        candidatesTested: 1,
        holdout: 'not applied; record is a local crib diagnostic',
        negativeControl: 'not run',
      },
    });
    setLogged(true);
    window.setTimeout(() => setLogged(false), 1600);
  };

  return (
    <div className="page-stack crib-page">
      <header className="page-header">
        <div>
          <span className="eyebrow">KNOWN-PLAINTEXT CONTROL</span>
          <h1>Crib bench</h1>
          <p>
            Every public plaintext character is locked to its one-based K4 position.
            Inspect the implied streams and test new cribs without shifting the evidence.
          </p>
        </div>
        <div className="header-token">
          <ShieldCheck size={18} />
          <span>24 confirmed / 73 undisclosed</span>
        </div>
      </header>

      <section className="panel crib-map-panel">
        <div className="panel-heading split-heading">
          <div>
            <span className="section-number">01 / CANONICAL MAP</span>
            <h2>All 97 local positions</h2>
          </div>
          <div className="map-axis-note">TOP: CIPHER / BOTTOM: PLAIN</div>
        </div>
        <K4Strip
          focusStart={plain.length ? start : undefined}
          focusEnd={plain.length ? end : undefined}
        />
      </section>

      <section className="crib-evidence-grid">
        {K4_CRIBS.map((crib) => {
          const source = RESEARCH_SOURCES.find((item) => item.id === crib.sourceId);
          return (
            <article className="crib-evidence-card" key={crib.id}>
              <div className="crib-position">{crib.start}–{crib.end}</div>
              <div className="crib-pair">
                <code>{crib.cipher}</code>
                <span>↓</span>
                <strong>{crib.plain}</strong>
              </div>
              <p>{crib.announced}</p>
              {source && (
                <a href={source.url} target="_blank" rel="noreferrer">
                  {source.publisher} <ExternalLink size={12} />
                </a>
              )}
            </article>
          );
        })}
      </section>

      <section className="workbench-split">
        <div className="panel custom-crib-panel">
          <div className="panel-heading">
            <span className="section-number">02 / DRAG A CRIB</span>
            <h2>Derive a candidate stream</h2>
            <p>Uses C − P modulo the selected alphabet, with no hidden offset.</p>
          </div>

          <div className="field-row crib-fields">
            <div className="field-group position-field">
              <label className="field-label" htmlFor="crib-start">Start</label>
              <input
                id="crib-start"
                type="number"
                min="1"
                max="97"
                value={start}
                onChange={(event) => {
                  setStart(Math.max(1, Math.min(97, Number(event.target.value))));
                  setLogged(false);
                }}
              />
            </div>
            <div className="field-group">
              <label className="field-label" htmlFor="crib-text">Proposed plaintext</label>
              <input
                id="crib-text"
                value={plainText}
                placeholder="ENTER A WORD OR PHRASE"
                onChange={(event) => {
                  setPlainText(event.target.value.toUpperCase());
                  setLogged(false);
                }}
                spellCheck={false}
              />
            </div>
          </div>

          <div className="segmented-control compact-segment" aria-label="Crib alphabet">
            <button aria-pressed={alphabetMode === 'standard'} className={alphabetMode === 'standard' ? 'active' : ''} onClick={() => setAlphabetMode('standard')}>Standard A–Z</button>
            <button aria-pressed={alphabetMode === 'kryptos'} className={alphabetMode === 'kryptos' ? 'active' : ''} onClick={() => setAlphabetMode('kryptos')}>KRYPTOS alphabet</button>
          </div>

          <div className="crib-output-stack">
            <div>
              <span>CIPHER {plain ? `${start}–${end}` : ''}</span>
              <code>{cipher || '—'}</code>
            </div>
            <div>
              <span>PLAIN</span>
              <code>{plain || '—'}</code>
            </div>
            <div className="derived-key-row">
              <span>IMPLIED STREAM</span>
              <code>{keyStream || '—'}</code>
            </div>
          </div>

          {conflicts.length > 0 && (
            <div className="conflict-alert">
              <CircleAlert size={17} />
              <div>
                <strong>Conflicts with confirmed plaintext</strong>
                <span>
                  {conflicts
                    .map(
                      (conflict) =>
                        `${conflict.position}: ${conflict.supplied} ≠ ${conflict.expected}`,
                    )
                    .join(' · ')}
                </span>
              </div>
            </div>
          )}

          <button className="button button-primary button-wide" onClick={logCrib} disabled={!plain}>
            {logged ? <Check size={15} /> : <Plus size={15} />}
            {logged ? 'Added to notebook' : 'Log crib analysis'}
          </button>
        </div>

        <div className="panel stream-panel">
          <div className="panel-heading">
            <span className="section-number">03 / CONFIRMED STREAMS</span>
            <h2>What simple Vigenere would require</h2>
            <p>
              Different implied strings across the public blocks do not disprove a
              nonperiodic stream, but they constrain repeating-key claims.
            </p>
          </div>
          <div className="known-streams">
            {K4_CRIBS.map((crib) => (
              <article key={crib.id}>
                <div>
                  <span>{crib.start}–{crib.end}</span>
                  <strong>{crib.plain}</strong>
                </div>
                <dl>
                  <div>
                    <dt>A–Z</dt>
                    <dd>{deriveKeystream(crib.cipher, crib.plain, STANDARD_ALPHABET)}</dd>
                  </div>
                  <div>
                    <dt>KRYPTOS</dt>
                    <dd>{deriveKeystream(crib.cipher, crib.plain, KRYPTOS_ALPHABET)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>
          <div className="stream-caveat">
            <KeyRound size={18} />
            <p>
              These are arithmetic diagnostics, not candidate keys. A transposition
              before substitution would break direct positional interpretation.
            </p>
          </div>
        </div>
      </section>

      <section className="panel holdout-panel">
        <div className="panel-heading">
          <span className="section-number">04 / ANTI-OVERFITTING PROTOCOL</span>
          <h2>Fit one block. Hold back the other.</h2>
        </div>
        <div className="holdout-steps">
          <div><span>01</span><strong>Train</strong><p>Use EASTNORTHEAST to select parameters.</p></div>
          <div><span>02</span><strong>Hold out</strong><p>Test BERLINCLOCK without any adjustment.</p></div>
          <div><span>03</span><strong>Reverse</strong><p>Swap the blocks and repeat the experiment.</p></div>
          <div><span>04</span><strong>Calibrate</strong><p>Compare success with matched random controls.</p></div>
          <div><span>05</span><strong>Disclose</strong><p>Report parameters, trials, score and full output.</p></div>
        </div>
      </section>
    </div>
  );
}
