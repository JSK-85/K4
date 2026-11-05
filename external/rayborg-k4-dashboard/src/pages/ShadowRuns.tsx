import {
  CheckCircle2,
  CircleX,
  Clock3,
  Play,
  RefreshCw,
  ShieldCheck,
} from 'lucide-react';
import { useState } from 'react';
import { createShadowRuns } from '../lib/shadowRuns';

function shorten(text: string, length = 132) {
  const flattened = text.replace(/\s+/g, '');
  return flattened.length > length ? `${flattened.slice(0, length)}…` : flattened;
}

export function ShadowRuns() {
  const [runs, setRuns] = useState(createShadowRuns);
  const [lastRun, setLastRun] = useState(() => new Date());
  const passed = runs.filter((run) => run.passed).length;

  const execute = () => {
    setRuns(createShadowRuns());
    setLastRun(new Date());
  };

  return (
    <div className="page-stack shadow-page">
      <header className="page-header">
        <div>
          <span className="eyebrow">KNOWN-ANSWER VALIDATION</span>
          <h1>Shadow runs</h1>
          <p>
            The dashboard attacks solved K1–K3 with the same core primitives used in
            the lab. Exact recovery and round-trip checks expose implementation drift.
          </p>
        </div>
        <button className="button button-primary" onClick={execute}>
          <Play size={15} /> Run all controls
        </button>
      </header>

      <section className="run-summary-banner">
        <div className={passed === runs.length ? 'run-seal passed' : 'run-seal failed'}>
          {passed === runs.length ? <ShieldCheck size={28} /> : <CircleX size={28} />}
        </div>
        <div>
          <span>CONTROL SUITE</span>
          <strong>{passed === runs.length ? 'ALL SYSTEMS CONSISTENT' : 'REGRESSION DETECTED'}</strong>
          <p>{passed} of {runs.length} executable controls passed.</p>
        </div>
        <div className="run-time">
          <Clock3 size={14} />
          <span>Last run</span>
          <strong>{lastRun.toLocaleTimeString()}</strong>
        </div>
      </section>

      <section className="run-list">
        {runs.map((run, index) => (
          <article className={`panel run-card ${run.passed ? 'run-passed' : 'run-failed'}`} key={run.id}>
            <div className="run-card-index">{String(index + 1).padStart(2, '0')}</div>
            <div className="run-card-main">
              <div className="run-card-heading">
                <div>
                  <span className="run-section">{run.section}</span>
                  <h2>{run.title}</h2>
                </div>
                <div className="run-result">
                  {run.passed ? <CheckCircle2 size={17} /> : <CircleX size={17} />}
                  {run.passed ? 'PASS' : 'FAIL'}
                </div>
              </div>
              <p className="run-method">{run.method}</p>
              <div className="run-parameters">
                {Object.entries(run.parameters).map(([key, value]) => (
                  <div key={key}><span>{key}</span><code>{value}</code></div>
                ))}
              </div>
              <div className="run-compare">
                <div>
                  <span>EXPECTED</span>
                  <code>{shorten(run.expected)}</code>
                </div>
                <div>
                  <span>ACTUAL</span>
                  <code>{shorten(run.actual)}</code>
                </div>
              </div>
              <p className="run-detail">{run.detail}</p>
            </div>
          </article>
        ))}
      </section>

      <section className="shadow-notes-grid">
        <article className="panel">
          <RefreshCw size={19} />
          <h3>Why round trips matter</h3>
          <p>
            A readable prefix can survive a broken transformation. Re-encryption checks
            every output position and catches route orientation or key-index errors.
          </p>
        </article>
        <article className="panel">
          <ShieldCheck size={19} />
          <h3>What this does not prove</h3>
          <p>
            Passing K1–K3 proves implementation consistency only. It does not imply
            that K4 reuses any solved method or that a hybrid search is correctly scoped.
          </p>
        </article>
      </section>
    </div>
  );
}
