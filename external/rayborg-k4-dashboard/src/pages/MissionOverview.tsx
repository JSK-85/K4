import {
  ArrowRight,
  CheckCircle2,
  CircleDashed,
  Clock3,
  Database,
  Fingerprint,
  LockKeyhole,
} from 'lucide-react';
import type { ViewId } from '../App';
import { K4Strip } from '../components/K4Strip';
import { K4_CIPHER, KRYPTOS_SECTIONS } from '../data/kryptos';
import { RESEARCH_AS_OF, TIMELINE } from '../data/research';
import { TECHNIQUES } from '../data/techniques';
import { textFingerprint } from '../lib/analysis';
import type { Experiment, TechniqueStatus } from '../types';

interface MissionOverviewProps {
  techniqueStatuses: Record<string, TechniqueStatus>;
  experiments: Experiment[];
  navigate: (view: ViewId) => void;
}

export function MissionOverview({
  techniqueStatuses,
  experiments,
  navigate,
}: MissionOverviewProps) {
  const fingerprint = textFingerprint(K4_CIPHER);
  const complete = Object.values(techniqueStatuses).filter((status) =>
    ['tested', 'rejected', 'promising', 'validated'].includes(status),
  ).length;
  const active = Object.values(techniqueStatuses).filter(
    (status) => status === 'active' || status === 'promising',
  ).length;
  const progress = Math.round((complete / TECHNIQUES.length) * 100);
  const latestEvents = TIMELINE.slice(-4).reverse();

  return (
    <div className="page-stack mission-page">
      <section className="mission-hero">
        <div className="hero-copy">
          <div className="eyebrow">OPERATIONS FIELDBOOK / RESEARCH AS OF {RESEARCH_AS_OF}</div>
          <h1>
            Break the method.
            <br />
            <em>Not just the message.</em>
          </h1>
          <p>
            A reproducible workbench for the 97-letter K4 passage of Jim Sanborn’s
            Kryptos installation. Every lead is indexed, every method is logged, and
            every primitive must first survive K1–K3.
          </p>
          <div className="hero-actions">
            <button className="button button-primary" onClick={() => navigate('lab')}>
              Open cipher lab <ArrowRight size={16} />
            </button>
            <button className="button button-quiet" onClick={() => navigate('research')}>
              Read source brief
            </button>
          </div>
        </div>

        <div className="hero-dossier">
          <div className="dossier-corner dossier-corner-tl" />
          <div className="dossier-corner dossier-corner-br" />
          <div className="dossier-stamp">ACTIVE FILE</div>
          <div className="dossier-heading">
            <span>KRYPTOS / SECTION FOUR</span>
            <strong>K4–097</strong>
          </div>
          <div className="dossier-string">{K4_CIPHER}</div>
          <dl className="dossier-facts">
            <div>
              <dt>Public plaintext</dt>
              <dd>24 / 97</dd>
            </div>
            <div>
              <dt>Unknown positions</dt>
              <dd>73</dd>
            </div>
            <div>
              <dt>Method</dt>
              <dd>Undisclosed</dd>
            </div>
            <div>
              <dt>Verifier</dt>
              <dd>Live / external</dd>
            </div>
          </dl>
          <div className="dossier-status">
            <span /> Plaintext privately held; public derivation still open
          </div>
        </div>
      </section>

      <section className="metric-grid" aria-label="K4 metrics">
        <article className="metric-card">
          <Fingerprint size={18} />
          <span className="metric-label">Cipher length</span>
          <strong>097</strong>
          <small>prime number of letters</small>
        </article>
        <article className="metric-card">
          <Database size={18} />
          <span className="metric-label">Index of coincidence</span>
          <strong>{fingerprint.ic.toFixed(4)}</strong>
          <small>English baseline ≈ 0.0667</small>
        </article>
        <article className="metric-card">
          <CheckCircle2 size={18} />
          <span className="metric-label">Methods processed</span>
          <strong>
            {complete}<i>/{TECHNIQUES.length}</i>
          </strong>
          <small>{progress}% of registry</small>
        </article>
        <article className="metric-card">
          <CircleDashed size={18} />
          <span className="metric-label">Active leads</span>
          <strong>{String(active).padStart(2, '0')}</strong>
          <small>{experiments.length} notebook records</small>
        </article>
      </section>

      <section className="panel k4-overview-panel">
        <div className="panel-heading split-heading">
          <div>
            <span className="section-number">01 / POSITION MAP</span>
            <h2>Known plaintext, fixed in place</h2>
          </div>
          <div className="legend-row">
            <span><i className="legend-swatch legend-known" /> Confirmed</span>
            <span><i className="legend-swatch legend-unknown" /> Undisclosed</span>
          </div>
        </div>
        <K4Strip compact />
        <div className="crib-summary-row">
          <div>
            <span>22–34</span>
            <strong>EASTNORTHEAST</strong>
          </div>
          <div>
            <span>64–74</span>
            <strong>BERLINCLOCK</strong>
          </div>
          <button className="text-button" onClick={() => navigate('cribs')}>
            Inspect all positions <ArrowRight size={14} />
          </button>
        </div>
      </section>

      <section className="overview-split">
        <div className="panel">
          <div className="panel-heading">
            <span className="section-number">02 / SECTION CONTROL</span>
            <h2>Shadow corpus</h2>
            <p>The solved passages are executable controls, not decorative history.</p>
          </div>
          <div className="section-control-list">
            {KRYPTOS_SECTIONS.map((section) => (
              <article className={`section-control section-${section.id.toLowerCase()}`} key={section.id}>
                <div className="section-id">{section.id}</div>
                <div className="section-control-copy">
                  <strong>{section.title}</strong>
                  <span>{section.method}</span>
                </div>
                <div className="section-control-meta">
                  <span>{section.letterCount} L</span>
                  {section.id === 'K4' ? <LockKeyhole size={15} /> : <CheckCircle2 size={15} />}
                </div>
              </article>
            ))}
          </div>
          <button className="button button-wide button-quiet" onClick={() => navigate('runs')}>
            View executable shadow runs <ArrowRight size={15} />
          </button>
        </div>

        <div className="panel">
          <div className="panel-heading">
            <span className="section-number">03 / CURRENT RECORD</span>
            <h2>Latest verified developments</h2>
            <p>Claims are retained with dates because the record changed materially in 2025–26.</p>
          </div>
          <div className="mini-timeline">
            {latestEvents.map((event) => (
              <article key={`${event.date}-${event.title}`}>
                <div className={`timeline-marker marker-${event.kind}`}>
                  <Clock3 size={13} />
                </div>
                <div>
                  <time>{event.date}</time>
                  <strong>{event.title}</strong>
                  <p>{event.detail}</p>
                </div>
              </article>
            ))}
          </div>
          <button className="button button-wide button-quiet" onClick={() => navigate('research')}>
            Open full source ledger <ArrowRight size={15} />
          </button>
        </div>
      </section>

      <section className="protocol-banner">
        <div>
          <span className="section-number">RESEARCH RULE 01</span>
          <strong>No crib gets moved to make a method fit.</strong>
        </div>
        <p>
          Fit one public block, validate against the other, disclose every searched
          parameter, and compare the result with random controls.
        </p>
      </section>
    </div>
  );
}
