import {
  Check,
  ChevronDown,
  Filter,
  RotateCcw,
  Search,
  SlidersHorizontal,
} from 'lucide-react';
import type { Dispatch, SetStateAction } from 'react';
import { useState } from 'react';
import { STATUS_LABELS, StatusBadge } from '../components/StatusBadge';
import {
  INITIAL_TECHNIQUE_STATUSES,
  TECHNIQUE_CATEGORIES,
  TECHNIQUES,
} from '../data/techniques';
import type { TechniqueStatus } from '../types';

interface TechniqueRegistryProps {
  statuses: Record<string, TechniqueStatus>;
  setStatuses: Dispatch<SetStateAction<Record<string, TechniqueStatus>>>;
}

const ALL_STATUSES = Object.keys(STATUS_LABELS) as TechniqueStatus[];

export function TechniqueRegistry({ statuses, setStatuses }: TechniqueRegistryProps) {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('All methods');
  const [statusFilter, setStatusFilter] = useState<'all' | TechniqueStatus>('all');
  const [priority, setPriority] = useState<'all' | 'high' | 'medium' | 'exploratory'>('all');

  const filtered = TECHNIQUES.filter((item) => {
    const status = statuses[item.id] ?? item.initialStatus;
    const haystack = `${item.title} ${item.rationale} ${item.category}`.toLowerCase();
    return (
      haystack.includes(query.toLowerCase()) &&
      (category === 'All methods' || item.category === category) &&
      (statusFilter === 'all' || status === statusFilter) &&
      (priority === 'all' || item.priority === priority)
    );
  });

  const counts = ALL_STATUSES.reduce(
    (result, status) => ({
      ...result,
      [status]: TECHNIQUES.filter(
        (item) => (statuses[item.id] ?? item.initialStatus) === status,
      ).length,
    }),
    {} as Record<TechniqueStatus, number>,
  );
  const processed =
    counts.tested + counts.rejected + counts.promising + counts.validated;
  const completion = Math.round((processed / TECHNIQUES.length) * 100);

  const setOneStatus = (id: string, status: TechniqueStatus) => {
    setStatuses((current) => ({ ...current, [id]: status }));
  };

  const markVisible = (status: TechniqueStatus) => {
    setStatuses((current) => ({
      ...current,
      ...Object.fromEntries(filtered.map((item) => [item.id, status])),
    }));
  };

  const resetRegistry = () => {
    if (window.confirm('Reset every method to the researched baseline statuses?')) {
      setStatuses(INITIAL_TECHNIQUE_STATUSES);
    }
  };

  return (
    <div className="page-stack technique-page">
      <header className="page-header">
        <div>
          <span className="eyebrow">MASTER METHOD REGISTER</span>
          <h1>Technique registry</h1>
          <p>
            A living checklist of cipher families, physical hypotheses, diagnostics
            and search strategies. Status changes persist locally.
          </p>
        </div>
        <div className="completion-dial" style={{ '--completion': `${completion * 3.6}deg` } as React.CSSProperties}>
          <div><strong>{completion}%</strong><span>processed</span></div>
        </div>
      </header>

      <section className="status-summary-grid">
        {ALL_STATUSES.map((status) => (
          <button
            className={`status-summary status-summary-${status} ${statusFilter === status ? 'selected' : ''}`}
            key={status}
            onClick={() => setStatusFilter((current) => (current === status ? 'all' : status))}
            aria-pressed={statusFilter === status}
          >
            <span>{STATUS_LABELS[status]}</span>
            <strong>{counts[status]}</strong>
          </button>
        ))}
      </section>

      <section className="panel registry-panel">
        <div className="registry-toolbar">
          <label className="search-field">
            <Search size={16} />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search methods or rationale"
              aria-label="Search methods"
            />
          </label>
          <label className="select-field">
            <Filter size={15} />
            <select value={category} onChange={(event) => setCategory(event.target.value)} aria-label="Filter category">
              <option>All methods</option>
              {TECHNIQUE_CATEGORIES.map((item) => <option key={item}>{item}</option>)}
            </select>
            <ChevronDown size={14} />
          </label>
          <label className="select-field">
            <SlidersHorizontal size={15} />
            <select value={priority} onChange={(event) => setPriority(event.target.value as typeof priority)} aria-label="Filter priority">
              <option value="all">All priorities</option>
              <option value="high">High priority</option>
              <option value="medium">Medium priority</option>
              <option value="exploratory">Exploratory</option>
            </select>
            <ChevronDown size={14} />
          </label>
        </div>

        <div className="bulk-row">
          <span>{filtered.length} of {TECHNIQUES.length} methods shown</span>
          <div>
            <button className="text-button" onClick={() => markVisible('tested')}>Mark visible tested</button>
            <button className="text-button" onClick={() => markVisible('pending')}>Clear visible</button>
            <button className="icon-text-button" onClick={resetRegistry}><RotateCcw size={13} /> Reset baseline</button>
          </div>
        </div>

        <div className="technique-list">
          {filtered.map((item) => {
            const status = statuses[item.id] ?? item.initialStatus;
            const checked = ['tested', 'rejected', 'promising', 'validated'].includes(status);
            return (
              <article className={`technique-row technique-${status}`} key={item.id}>
                <button
                  className={`technique-check ${checked ? 'checked' : ''}`}
                  role="checkbox"
                  aria-checked={checked}
                  aria-label={`${checked ? 'Uncheck' : 'Check'} ${item.title}`}
                  onClick={() => setOneStatus(item.id, checked ? 'pending' : 'tested')}
                >
                  {checked && <Check size={15} />}
                </button>
                <div className="technique-copy">
                  <div className="technique-title-row">
                    <strong>{item.title}</strong>
                    <span className={`priority-tag priority-${item.priority}`}>{item.priority}</span>
                  </div>
                  <p>{item.rationale}</p>
                  {item.evidence && <small>{item.evidence}</small>}
                </div>
                <div className="technique-category">{item.category}</div>
                <label className="status-select-wrap">
                  <StatusBadge status={status} />
                  <select
                    value={status}
                    onChange={(event) => setOneStatus(item.id, event.target.value as TechniqueStatus)}
                    aria-label={`Status for ${item.title}`}
                  >
                    {ALL_STATUSES.map((option) => (
                      <option value={option} key={option}>{STATUS_LABELS[option]}</option>
                    ))}
                  </select>
                </label>
              </article>
            );
          })}
          {!filtered.length && (
            <div className="empty-state">
              <Search size={22} />
              <strong>No methods match these filters.</strong>
              <button className="text-button" onClick={() => {
                setQuery('');
                setCategory('All methods');
                setStatusFilter('all');
                setPriority('all');
              }}>Clear filters</button>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
