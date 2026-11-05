import {
  Beaker,
  Binary,
  BookOpen,
  ClipboardCheck,
  FlaskConical,
  Menu,
  NotebookPen,
  Radar,
  X,
} from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { INITIAL_TECHNIQUE_STATUSES } from './data/techniques';
import { usePersistentState } from './hooks/usePersistentState';
import { useMediaQuery } from './hooks/useMediaQuery';
import {
  isExperimentArray,
  isResearchNotes,
  isTechniqueStatusMap,
  mergeExperimentRecords,
} from './lib/validation';
import { CipherLab } from './pages/CipherLab';
import { CribBench } from './pages/CribBench';
import { MissionOverview } from './pages/MissionOverview';
import { Notebook } from './pages/Notebook';
import { ResearchLibrary } from './pages/ResearchLibrary';
import { ShadowRuns } from './pages/ShadowRuns';
import { TechniqueRegistry } from './pages/TechniqueRegistry';
import type { Experiment, TechniqueStatus } from './types';

export type ViewId =
  | 'mission'
  | 'lab'
  | 'cribs'
  | 'techniques'
  | 'runs'
  | 'research'
  | 'notebook';

const NAV_ITEMS = [
  { id: 'mission' as const, label: 'Mission', icon: Radar },
  { id: 'lab' as const, label: 'Cipher Lab', icon: FlaskConical },
  { id: 'cribs' as const, label: 'Crib Bench', icon: Binary },
  { id: 'techniques' as const, label: 'Methods', icon: ClipboardCheck },
  { id: 'runs' as const, label: 'Shadow Runs', icon: Beaker },
  { id: 'research' as const, label: 'Research', icon: BookOpen },
  { id: 'notebook' as const, label: 'Notebook', icon: NotebookPen },
];

export default function App() {
  const [view, setView] = useState<ViewId>('mission');
  const [menuOpen, setMenuOpen] = useState(false);
  const isMobile = useMediaQuery('(max-width: 760px)');
  const sidebarRef = useRef<HTMLElement>(null);
  const menuButtonRef = useRef<HTMLButtonElement>(null);
  const mainRef = useRef<HTMLElement>(null);
  const [techniqueStatuses, setTechniqueStatuses, techniqueStorage, resetTechniques] = usePersistentState<
    Record<string, TechniqueStatus>
  >('k4-fieldbook-techniques-v1', INITIAL_TECHNIQUE_STATUSES, {
    validate: isTechniqueStatusMap,
    mergeExternal: (local, external) => ({ ...local, ...external }),
  });
  const [experiments, setExperiments, experimentStorage, resetExperiments] = usePersistentState<Experiment[]>(
    'k4-fieldbook-experiments-v1',
    [],
    { validate: isExperimentArray, mergeExternal: mergeExperimentRecords },
  );
  const [researchNotes, setResearchNotes, noteStorage, resetNotes] = usePersistentState(
    'k4-fieldbook-research-notes-v1',
    '',
    { validate: isResearchNotes, maxBytes: 600_000 },
  );
  const storageErrors = [techniqueStorage, experimentStorage, noteStorage].filter(
    (state) => state.status === 'error',
  );

  const resetInvalidStorage = () => {
    if (!window.confirm('Reset the local records that currently report a storage error?')) return;
    if (techniqueStorage.status === 'error') resetTechniques();
    if (experimentStorage.status === 'error') resetExperiments();
    if (noteStorage.status === 'error') resetNotes();
  };

  const navigate = (next: ViewId) => {
    setView(next);
    setMenuOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
    window.setTimeout(() => mainRef.current?.focus(), 0);
  };

  const closeMenu = () => {
    setMenuOpen(false);
    window.setTimeout(() => menuButtonRef.current?.focus(), 0);
  };

  useEffect(() => {
    if (!isMobile || !menuOpen) return;
    window.setTimeout(
      () => sidebarRef.current?.querySelector<HTMLButtonElement>('.nav-item-active')?.focus(),
      0,
    );
  }, [isMobile, menuOpen]);

  const trapSidebarFocus = (event: React.KeyboardEvent<HTMLElement>) => {
    if (!isMobile || !menuOpen) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      closeMenu();
      return;
    }
    if (event.key !== 'Tab') return;
    const focusable = [...(sidebarRef.current?.querySelectorAll<HTMLElement>('button:not(:disabled), a[href]') ?? [])];
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  };

  const addExperiment = (experiment: Experiment) => {
    setExperiments((current) => [experiment, ...current]);
  };

  const currentNav = NAV_ITEMS.find((item) => item.id === view)!;

  return (
    <div className="app-shell">
      <aside
        className={`sidebar ${menuOpen ? 'sidebar-open' : ''}`}
        id="primary-sidebar"
        ref={sidebarRef}
        role={isMobile ? 'dialog' : undefined}
        aria-modal={isMobile && menuOpen ? true : undefined}
        aria-label={isMobile ? 'Dashboard navigation' : undefined}
        aria-hidden={isMobile ? !menuOpen : undefined}
        inert={isMobile && !menuOpen}
        onKeyDown={trapSidebarFocus}
      >
        <div className="brand-block">
          <div className="brand-mark" aria-hidden="true">
            <span>K</span>
            <span>4</span>
          </div>
          <div>
            <strong>K4 Fieldbook</strong>
            <small>Private cryptanalysis desk</small>
          </div>
        </div>

        <nav className="primary-nav" aria-label="Dashboard">
          {NAV_ITEMS.map((item, index) => {
            const Icon = item.icon;
            return (
              <button
                className={view === item.id ? 'nav-item nav-item-active' : 'nav-item'}
                key={item.id}
                onClick={() => navigate(item.id)}
                aria-current={view === item.id ? 'page' : undefined}
              >
                <span className="nav-number">0{index + 1}</span>
                <Icon size={18} strokeWidth={1.7} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-foot">
          <div className={`privacy-indicator ${storageErrors.length ? 'storage-error' : ''}`}>
            <span className="privacy-dot" />
            <span>{storageErrors.length ? 'Local save error' : 'Local storage only'}</span>
          </div>
          {storageErrors.length ? (
            <button className="storage-reset" onClick={resetInvalidStorage} title={storageErrors.map((state) => state.error).join('\n')}>
              Inspect and reset affected data
            </button>
          ) : (
            <p>No analytics, remote fonts, or external APIs.</p>
          )}
        </div>
      </aside>

      {menuOpen && (
        <button
          className="sidebar-scrim"
          onClick={closeMenu}
          aria-label="Close navigation"
        />
      )}

      <div className="main-column">
        <header className="topbar">
          <button
            className="menu-button"
            ref={menuButtonRef}
            onClick={() => setMenuOpen((open) => !open)}
            aria-label={menuOpen ? 'Close navigation' : 'Open navigation'}
            aria-expanded={menuOpen}
            aria-controls="primary-sidebar"
          >
            {menuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          <div className="topbar-location">
            <span>Workspace /</span>
            <strong>{currentNav.label}</strong>
          </div>
          <div className="topbar-status">
            <span className="status-pulse" />
            K4 / PUBLICLY UNDECIPHERED
          </div>
        </header>

        <main className="page-wrap" ref={mainRef} tabIndex={-1}>
          {view === 'mission' && (
            <MissionOverview
              techniqueStatuses={techniqueStatuses}
              experiments={experiments}
              navigate={navigate}
            />
          )}
          {view === 'lab' && <CipherLab addExperiment={addExperiment} />}
          {view === 'cribs' && <CribBench addExperiment={addExperiment} />}
          {view === 'techniques' && (
            <TechniqueRegistry
              statuses={techniqueStatuses}
              setStatuses={setTechniqueStatuses}
            />
          )}
          {view === 'runs' && <ShadowRuns />}
          {view === 'research' && (
            <ResearchLibrary notes={researchNotes} setNotes={setResearchNotes} persistence={noteStorage} />
          )}
          {view === 'notebook' && (
            <Notebook experiments={experiments} setExperiments={setExperiments} persistence={experimentStorage} />
          )}
        </main>
      </div>
    </div>
  );
}
