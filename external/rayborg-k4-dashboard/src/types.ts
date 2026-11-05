export type SectionId = 'K1' | 'K2' | 'K3' | 'K4';

export type TechniqueStatus =
  | 'pending'
  | 'active'
  | 'tested'
  | 'rejected'
  | 'promising'
  | 'validated';

export type TechniquePriority = 'high' | 'medium' | 'exploratory';

export interface KryptosSection {
  id: SectionId;
  title: string;
  cipherText: string;
  letterCount: number;
  status: string;
  method: string;
  key?: string;
  plainText?: string;
  note: string;
}

export interface K4Crib {
  id: string;
  start: number;
  end: number;
  cipher: string;
  plain: string;
  announced: string;
  sourceId: string;
  confidence: 'confirmed' | 'reported';
}

export interface Technique {
  id: string;
  category: string;
  title: string;
  rationale: string;
  priority: TechniquePriority;
  initialStatus: TechniqueStatus;
  evidence?: string;
}

export interface Experiment {
  id: string;
  createdAt: string;
  title: string;
  section: SectionId | 'custom';
  method: string;
  operation: string;
  key: string;
  alphabet: string;
  input: string;
  output: string;
  notes: string;
  status: TechniqueStatus;
  provenance: {
    appVersion: string;
    inputFingerprint: string;
    indexConvention: string;
    parameters: Record<string, string>;
    searchSpace: string;
    corpus: string;
    scoring: string;
    seed: string;
    elapsedMs: number;
    hardware: string;
    candidatesTested: number;
    holdout: string;
    negativeControl: string;
  };
}

export interface ResearchSource {
  id: string;
  title: string;
  publisher: string;
  date: string;
  url: string;
  tier: 'primary' | 'institutional' | 'academic' | 'reporting' | 'community';
  scope: string;
}

export interface TimelineEvent {
  date: string;
  title: string;
  detail: string;
  sourceIds: string[];
  kind: 'artwork' | 'solution' | 'clue' | 'archive';
}

export interface ShadowRun {
  id: string;
  section: SectionId;
  title: string;
  method: string;
  parameters: Record<string, string>;
  expected: string;
  actual: string;
  passed: boolean;
  detail: string;
}
