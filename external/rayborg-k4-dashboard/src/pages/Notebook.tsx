import {
  Check,
  ChevronDown,
  Download,
  FileJson,
  NotebookPen,
  Plus,
  Search,
  Shield,
  Trash2,
  Upload,
} from 'lucide-react';
import type { ChangeEvent, Dispatch, SetStateAction } from 'react';
import { useState } from 'react';
import { STATUS_LABELS, StatusBadge } from '../components/StatusBadge';
import type { PersistenceState } from '../hooks/usePersistentState';
import {
  EXPERIMENT_SCHEMA,
  MAX_EXPERIMENTS,
  contentFingerprint,
  isExperiment,
  mergeExperimentRecords,
} from '../lib/validation';
import type { Experiment, SectionId, TechniqueStatus } from '../types';

interface NotebookProps {
  experiments: Experiment[];
  setExperiments: Dispatch<SetStateAction<Experiment[]>>;
  persistence: PersistenceState;
}

const STATUSES = Object.keys(STATUS_LABELS) as TechniqueStatus[];

export function Notebook({ experiments, setExperiments, persistence }: NotebookProps) {
  const [query, setQuery] = useState('');
  const [status, setStatus] = useState<'all' | TechniqueStatus>('all');
  const [showManual, setShowManual] = useState(false);
  const [title, setTitle] = useState('');
  const [method, setMethod] = useState('');
  const [section, setSection] = useState<SectionId | 'custom'>('K4');
  const [notes, setNotes] = useState('');
  const [importMessage, setImportMessage] = useState('');

  const filtered = experiments.filter((experiment) => {
    const haystack = `${experiment.title} ${experiment.method} ${experiment.notes} ${experiment.output}`.toLowerCase();
    return haystack.includes(query.toLowerCase()) && (status === 'all' || experiment.status === status);
  });

  const addManual = () => {
    if (!title.trim()) return;
    setExperiments((current) => [
      {
        id: crypto.randomUUID(),
        createdAt: new Date().toISOString(),
        title: title.trim(),
        section,
        method: method.trim() || 'Manual hypothesis',
        operation: 'note',
        key: '',
        alphabet: '',
        input: '',
        output: '',
        notes: notes.trim(),
        status: 'active',
        provenance: {
          appVersion: '0.1.0',
          inputFingerprint: contentFingerprint(''),
          indexConvention: section === 'K4' ? 'one-based local K4 positions 1–97' : 'not specified',
          parameters: {},
          searchSpace: 'manual hypothesis; not yet executed',
          corpus: 'not specified',
          scoring: 'not specified',
          seed: 'not applicable',
          elapsedMs: 0,
          hardware: 'not recorded',
          candidatesTested: 0,
          holdout: 'not specified',
          negativeControl: 'not specified',
        },
      },
      ...current,
    ]);
    setTitle('');
    setMethod('');
    setNotes('');
    setShowManual(false);
  };

  const updateStatus = (id: string, next: TechniqueStatus) => {
    setExperiments((current) =>
      current.map((experiment) =>
        experiment.id === id ? { ...experiment, status: next } : experiment,
      ),
    );
  };

  const remove = (id: string) => {
    setExperiments((current) => current.filter((experiment) => experiment.id !== id));
  };

  const exportNotebook = () => {
    const payload = JSON.stringify(
      {
        schema: EXPERIMENT_SCHEMA,
        exportedAt: new Date().toISOString(),
        experiments,
      },
      null,
      2,
    );
    const blob = new Blob([payload], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `k4-fieldbook-${new Date().toISOString().slice(0, 10)}.json`;
    anchor.click();
    URL.revokeObjectURL(url);
  };

  const importNotebook = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    event.target.value = '';
    if (!file) return;
    if (file.size > 5_000_000) {
      setImportMessage('Import rejected: file exceeds 5 MB.');
      return;
    }
    try {
      const parsed: unknown = JSON.parse(await file.text());
      if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
        throw new Error('bundle must be a JSON object');
      }
      const bundle = parsed as Record<string, unknown>;
      if (bundle.schema !== EXPERIMENT_SCHEMA) {
        throw new Error(`expected schema ${EXPERIMENT_SCHEMA}`);
      }
      if (!Array.isArray(bundle.experiments)) throw new Error('missing experiments array');
      if (bundle.experiments.length > MAX_EXPERIMENTS) {
        throw new Error(`bundle exceeds ${MAX_EXPERIMENTS} records`);
      }
      const valid = bundle.experiments.filter(isExperiment);
      const unique = [...new Map(valid.map((record) => [record.id, record])).values()];
      const known = new Set(experiments.map((item) => item.id));
      const accepted = unique.filter((item) => !known.has(item.id));
      const rejected = bundle.experiments.length - valid.length;
      const duplicate = valid.length - unique.length + unique.filter((item) => known.has(item.id)).length;
      setExperiments((current) => mergeExperimentRecords(current, accepted));
      setImportMessage(
        `Accepted ${accepted.length}; rejected ${rejected}; skipped ${duplicate} duplicate${duplicate === 1 ? '' : 's'}. ${persistence.status === 'error' ? 'Local save is currently unavailable.' : 'Queued for local save.'}`,
      );
    } catch (error) {
      setImportMessage(`Import rejected: ${error instanceof Error ? error.message : 'invalid JSON'}`);
    }
  };

  const clearAll = () => {
    if (window.confirm('Delete every notebook experiment from this browser? Export first if needed.')) {
      setExperiments([]);
    }
  };

  return (
    <div className="page-stack notebook-page">
      <header className="page-header">
        <div>
          <span className="eyebrow">LOCAL WORK RECORD</span>
          <h1>Experiment notebook</h1>
          <p>
            Cipher-lab and crib runs land here with their inputs, parameters and full
            outputs. Export regularly; browser storage is not a durable backup.
          </p>
        </div>
        <button className="button button-primary" onClick={() => setShowManual((shown) => !shown)}>
          <Plus size={15} /> New hypothesis
        </button>
      </header>

      <section className="notebook-privacy-row">
        <Shield size={18} />
        <div>
          <strong>
            {persistence.status === 'saved'
              ? 'Private by default, not encrypted at rest.'
              : 'Local records are not currently saving.'}
          </strong>
          <span>{persistence.error || 'Records stay in this browser profile unless you export them.'}</span>
        </div>
        <div className="notebook-file-actions">
          <button className="button button-quiet" onClick={exportNotebook} disabled={!experiments.length}><Download size={14} /> Export JSON</button>
          <label className="button button-quiet file-button"><Upload size={14} /> Import JSON<input type="file" accept="application/json,.json" onChange={importNotebook} /></label>
        </div>
      </section>

      {importMessage && <div className="import-message"><FileJson size={15} /> {importMessage}</div>}

      {showManual && (
        <section className="panel manual-entry-panel">
          <div className="panel-heading split-heading">
            <div><span className="section-number">MANUAL ENTRY</span><h2>Record a hypothesis</h2></div>
            <button className="text-button" onClick={() => setShowManual(false)}>Cancel</button>
          </div>
          <div className="manual-entry-grid">
            <div className="field-group">
              <label className="field-label" htmlFor="note-title">Title</label>
              <input id="note-title" value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Short, falsifiable claim" />
            </div>
            <div className="field-group">
              <label className="field-label" htmlFor="note-method">Method</label>
              <input id="note-method" value={method} onChange={(event) => setMethod(event.target.value)} placeholder="Cipher family or diagnostic" />
            </div>
            <div className="field-group section-entry-field">
              <label className="field-label" htmlFor="note-section">Section</label>
              <select id="note-section" value={section} onChange={(event) => setSection(event.target.value as typeof section)}>
                <option>K4</option><option>K3</option><option>K2</option><option>K1</option><option value="custom">Custom</option>
              </select>
            </div>
            <div className="field-group notes-entry-field">
              <label className="field-label" htmlFor="note-body">Notes / rejection criterion</label>
              <textarea id="note-body" value={notes} onChange={(event) => setNotes(event.target.value)} placeholder="State the exact test, required evidence, and what would reject it." />
            </div>
          </div>
          <button className="button button-primary" onClick={addManual} disabled={!title.trim()}><Check size={14} /> Add active hypothesis</button>
        </section>
      )}

      <section className="panel notebook-ledger">
        <div className="notebook-toolbar">
          <label className="search-field">
            <Search size={16} />
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search notebook" />
          </label>
          <label className="select-field">
            <select value={status} onChange={(event) => setStatus(event.target.value as typeof status)} aria-label="Filter notebook status">
              <option value="all">All statuses</option>
              {STATUSES.map((item) => <option value={item} key={item}>{STATUS_LABELS[item]}</option>)}
            </select>
            <ChevronDown size={14} />
          </label>
          <span className="record-count">{filtered.length} / {experiments.length} records</span>
        </div>

        {filtered.length ? (
          <div className="experiment-list">
            {filtered.map((experiment) => (
              <article className="experiment-card" key={experiment.id}>
                <div className="experiment-rail"><span>{experiment.section}</span><i /></div>
                <div className="experiment-main">
                  <div className="experiment-heading">
                    <div>
                      <time>{new Date(experiment.createdAt).toLocaleString()}</time>
                      <h2>{experiment.title}</h2>
                      <p>{experiment.method} · {experiment.operation}</p>
                    </div>
                    <label className="status-select-wrap">
                      <StatusBadge status={experiment.status} />
                      <select value={experiment.status} onChange={(event) => updateStatus(experiment.id, event.target.value as TechniqueStatus)} aria-label={`Status for ${experiment.title}`}>
                        {STATUSES.map((item) => <option value={item} key={item}>{STATUS_LABELS[item]}</option>)}
                      </select>
                    </label>
                  </div>
                  {experiment.notes && <p className="experiment-notes">{experiment.notes}</p>}
                  {(experiment.key || experiment.alphabet) && (
                    <div className="experiment-params">
                      {experiment.key && <div><span>KEY / STREAM</span><code>{experiment.key}</code></div>}
                      {experiment.alphabet && <div><span>ALPHABET</span><code>{experiment.alphabet}</code></div>}
                    </div>
                  )}
                  {(experiment.input || experiment.output) && (
                    <details>
                      <summary>Inspect complete artifacts</summary>
                      <div className="artifact-grid">
                        <div><span>INPUT</span><pre>{experiment.input || '—'}</pre></div>
                        <div><span>OUTPUT</span><pre>{experiment.output || '—'}</pre></div>
                      </div>
                    </details>
                  )}
                  <details className="provenance-details">
                    <summary>Inspect provenance</summary>
                    <div className="provenance-grid">
                      <div><span>INPUT FINGERPRINT</span><code>{experiment.provenance.inputFingerprint}</code></div>
                      <div><span>INDEXING</span><code>{experiment.provenance.indexConvention}</code></div>
                      <div><span>SEARCH SPACE</span><code>{experiment.provenance.searchSpace}</code></div>
                      <div><span>CORPUS / SCORE</span><code>{experiment.provenance.corpus} / {experiment.provenance.scoring}</code></div>
                      <div><span>ELAPSED</span><code>{experiment.provenance.elapsedMs.toFixed(3)} ms</code></div>
                      <div><span>CANDIDATES</span><code>{experiment.provenance.candidatesTested}</code></div>
                      <div><span>HOLDOUT</span><code>{experiment.provenance.holdout}</code></div>
                      <div><span>NEGATIVE CONTROL</span><code>{experiment.provenance.negativeControl}</code></div>
                    </div>
                  </details>
                </div>
                <button className="delete-experiment" onClick={() => remove(experiment.id)} aria-label={`Delete ${experiment.title}`}><Trash2 size={15} /></button>
              </article>
            ))}
          </div>
        ) : (
          <div className="empty-state notebook-empty">
            <NotebookPen size={27} />
            <strong>{experiments.length ? 'No records match these filters.' : 'No experiments logged yet.'}</strong>
            <p>Run a transform in the cipher lab, analyze a crib, or add a manual hypothesis.</p>
          </div>
        )}

        {!!experiments.length && (
          <div className="clear-notebook-row"><button className="icon-text-button danger-text" onClick={clearAll}><Trash2 size={13} /> Clear notebook</button></div>
        )}
      </section>
    </div>
  );
}
