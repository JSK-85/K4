import {
  Archive,
  BookMarked,
  ChevronDown,
  ExternalLink,
  FileQuestion,
  Landmark,
  Library,
  Search,
  ShieldAlert,
} from 'lucide-react';
import type { Dispatch, SetStateAction } from 'react';
import { useState } from 'react';
import type { PersistenceState } from '../hooks/usePersistentState';
import {
  ESTABLISHED_FACTS,
  OPEN_QUESTIONS,
  RESEARCH_AS_OF,
  RESEARCH_SOURCES,
  TIMELINE,
  TRANSCRIPTION_NOTES,
} from '../data/research';

interface ResearchLibraryProps {
  notes: string;
  setNotes: Dispatch<SetStateAction<string>>;
  persistence: PersistenceState;
}

type ResearchTab = 'brief' | 'timeline' | 'sources';

const TIER_LABELS = {
  primary: 'Primary / owner',
  institutional: 'Institutional',
  academic: 'Peer reviewed',
  reporting: 'Reporting',
  community: 'Community record',
};

export function ResearchLibrary({ notes, setNotes, persistence }: ResearchLibraryProps) {
  const [tab, setTab] = useState<ResearchTab>('brief');
  const [query, setQuery] = useState('');
  const [tier, setTier] = useState<'all' | keyof typeof TIER_LABELS>('all');

  const sourceById = (id: string) => RESEARCH_SOURCES.find((source) => source.id === id);
  const filteredSources = RESEARCH_SOURCES.filter((source) => {
    const haystack = `${source.title} ${source.publisher} ${source.scope}`.toLowerCase();
    return haystack.includes(query.toLowerCase()) && (tier === 'all' || source.tier === tier);
  });

  return (
    <div className="page-stack research-page">
      <header className="page-header research-header">
        <div>
          <span className="eyebrow">EVIDENCE LIBRARY / CURRENT THROUGH {RESEARCH_AS_OF}</span>
          <h1>Research record</h1>
          <p>
            Creator statements, institutional records, academic analysis and reporting
            are kept at distinct evidence levels. Contradictions remain visible.
          </p>
        </div>
        <div className="header-token">
          <Library size={18} />
          <span>{RESEARCH_SOURCES.length} cited sources</span>
        </div>
      </header>

      <nav className="research-tabs" aria-label="Research sections" role="tablist">
        <button role="tab" aria-selected={tab === 'brief'} className={tab === 'brief' ? 'active' : ''} onClick={() => setTab('brief')}>
          <BookMarked size={16} /> Evidence brief
        </button>
        <button role="tab" aria-selected={tab === 'timeline'} className={tab === 'timeline' ? 'active' : ''} onClick={() => setTab('timeline')}>
          <Landmark size={16} /> Chronology
        </button>
        <button role="tab" aria-selected={tab === 'sources'} className={tab === 'sources' ? 'active' : ''} onClick={() => setTab('sources')}>
          <Archive size={16} /> Source ledger
        </button>
      </nav>

      {tab === 'brief' && (
        <>
          <section className="status-clarification">
            <div className="clarification-code">STATUS / 2026</div>
            <div>
              <span>ARCHIVALLY RECOVERED</span>
              <strong>≠</strong>
              <span>PUBLICLY DECIPHERED</span>
            </div>
            <p>
              The plaintext was reconstructed from accidentally available Smithsonian
              papers in September 2025 and confirmed by Sanborn. It remains
              unpublished; no public method derives it from the 97-letter ciphertext.
            </p>
            <div className="inline-citations">
              {['sciam-discovery-2025', 'wired-discovery-2025', 'paradigm-2026'].map((id) => {
                const source = sourceById(id)!;
                return <a key={id} href={source.url} target="_blank" rel="noreferrer">{source.publisher} <ExternalLink size={11} /></a>;
              })}
            </div>
          </section>

          <section className="research-grid">
            <div className="panel evidence-facts">
              <div className="panel-heading">
                <span className="section-number">01 / ESTABLISHED</span>
                <h2>Facts with traceable support</h2>
              </div>
              {ESTABLISHED_FACTS.map((fact) => (
                <article key={fact.label}>
                  <strong>{fact.label}</strong>
                  <p>{fact.value}</p>
                  <div className="citation-chips">
                    {fact.sourceIds.map((id) => {
                      const source = sourceById(id);
                      return source ? (
                        <a href={source.url} target="_blank" rel="noreferrer" key={id}>{source.publisher}</a>
                      ) : null;
                    })}
                  </div>
                </article>
              ))}
            </div>

            <div className="panel open-questions">
              <div className="panel-heading">
                <span className="section-number">02 / UNRESOLVED</span>
                <h2>Questions, not facts</h2>
              </div>
              {OPEN_QUESTIONS.map((question, index) => (
                <article key={question.title}>
                  <span>{String(index + 1).padStart(2, '0')}</span>
                  <div>
                    <strong>{question.title}</strong>
                    <p>{question.detail}</p>
                  </div>
                </article>
              ))}
            </div>
          </section>

          <section className="panel installation-panel">
            <div className="panel-heading">
              <span className="section-number">03 / THE WHOLE WORK</span>
              <h2>Kryptos is not only a copper cipher panel</h2>
              <p>
                The CIA describes a two-part installation organized around intelligence
                gathering and information moving toward an unknown destination.
              </p>
            </div>
            <div className="installation-map">
              <article>
                <span>ENTRANCE</span>
                <strong>Granite “pages”</strong>
                <p>Copper layers carry International Morse and older cipher forms.</p>
              </article>
              <div className="map-connector"><i /><span>increasing sophistication</span><i /></div>
              <article>
                <span>ORIENTATION</span>
                <strong>Lodestone + compass</strong>
                <p>Natural magnetism, navigational direction and invisible forces.</p>
              </article>
              <div className="map-connector"><i /><span>into the courtyard</span><i /></div>
              <article>
                <span>COURTYARD</span>
                <strong>Screen + water</strong>
                <p>Encoded copper, keyed tableau, petrified wood and circulating pools.</p>
              </article>
            </div>
            <div className="source-footnote">
              Source: <a href={sourceById('cia-kryptos')!.url} target="_blank" rel="noreferrer">CIA institutional history and transcription <ExternalLink size={11} /></a>
            </div>
          </section>

          <section className="research-grid transcription-grid">
            <div className="panel">
              <div className="panel-heading">
                <span className="section-number">04 / TRANSCRIPTION CONTROL</span>
                <h2>Boundaries and anomalies</h2>
              </div>
              <div className="transcription-list">
                {TRANSCRIPTION_NOTES.map((note, index) => (
                  <div key={note}><span>{String(index + 1).padStart(2, '0')}</span><p>{note}</p></div>
                ))}
              </div>
            </div>
            <div className="panel provenance-warning">
              <ShieldAlert size={22} />
              <div className="panel-heading">
                <span className="section-number">EVIDENCE CAUTION</span>
                <h2>Creator statements can evolve</h2>
              </div>
              <p>
                In 2014 Sanborn emphasized the Mengenlehreuhr. In his November 2025
                final clues he identified BERLINCLOCK as the Berlin World Clock. The
                dashboard records both statements with dates instead of silently
                choosing one historical narrative.
              </p>
              <p>
                Likewise, production charts and the K2 omission show that not every
                anomaly should be presumed intentional, even when later described that way.
              </p>
            </div>
          </section>

          <section className="panel research-notes-panel">
            <div className="panel-heading split-heading">
              <div>
                <span className="section-number">05 / PRIVATE MARGIN</span>
                <h2>Research notes</h2>
              </div>
              <span className={`autosave-label ${persistence.status === 'error' ? 'save-error' : ''}`}>
                {persistence.status === 'saved' ? 'SAVED IN LOCAL STORAGE' : 'LOCAL SAVE ERROR'}
              </span>
            </div>
            {persistence.error && <p className="save-error-message">{persistence.error}</p>}
            <textarea
              value={notes}
              onChange={(event) => setNotes(event.target.value)}
              placeholder="Record source follow-ups, contradictions, or hypotheses here…"
            />
          </section>
        </>
      )}

      {tab === 'timeline' && (
        <section className="panel full-timeline-panel">
          <div className="panel-heading">
            <span className="section-number">CHRONOLOGY / 1988–2026</span>
            <h2>Artwork, solutions, clues and custody</h2>
          </div>
          <div className="full-timeline">
            {TIMELINE.map((event) => (
              <article key={`${event.date}-${event.title}`}>
                <time>{event.date}</time>
                <div className={`full-timeline-marker marker-${event.kind}`}><i /></div>
                <div className="timeline-event-copy">
                  <span className={`event-kind kind-${event.kind}`}>{event.kind}</span>
                  <h3>{event.title}</h3>
                  <p>{event.detail}</p>
                  <div className="citation-chips">
                    {event.sourceIds.map((id) => {
                      const source = sourceById(id);
                      return source ? <a key={id} href={source.url} target="_blank" rel="noreferrer">{source.publisher}</a> : null;
                    })}
                  </div>
                </div>
              </article>
            ))}
          </div>
        </section>
      )}

      {tab === 'sources' && (
        <section className="panel source-ledger-panel">
          <div className="panel-heading split-heading">
            <div>
              <span className="section-number">SOURCE LEDGER</span>
              <h2>Research provenance</h2>
            </div>
            <span className="ledger-count">{filteredSources.length} records</span>
          </div>
          <div className="source-toolbar">
            <label className="search-field">
              <Search size={16} />
              <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search title, publisher, or scope" />
            </label>
            <label className="select-field">
              <select value={tier} onChange={(event) => setTier(event.target.value as typeof tier)} aria-label="Filter evidence tier">
                <option value="all">All evidence tiers</option>
                {Object.entries(TIER_LABELS).map(([value, label]) => <option value={value} key={value}>{label}</option>)}
              </select>
              <ChevronDown size={14} />
            </label>
          </div>
          <div className="source-list">
            {filteredSources.map((source, index) => (
              <article key={source.id}>
                <div className="source-index">S{String(index + 1).padStart(2, '0')}</div>
                <div className="source-copy">
                  <div>
                    <span className={`source-tier tier-${source.tier}`}>{TIER_LABELS[source.tier]}</span>
                    <time>{source.date}</time>
                  </div>
                  <h3>{source.title}</h3>
                  <strong>{source.publisher}</strong>
                  <p>{source.scope}</p>
                </div>
                <a className="source-open" href={source.url} target="_blank" rel="noreferrer" aria-label={`Open ${source.title}`}>
                  <ExternalLink size={17} />
                </a>
              </article>
            ))}
            {!filteredSources.length && (
              <div className="empty-state"><FileQuestion size={22} /><strong>No sources match these filters.</strong></div>
            )}
          </div>
        </section>
      )}
    </div>
  );
}
