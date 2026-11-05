import type { Experiment, SectionId, TechniqueStatus } from '../types';

export const EXPERIMENT_SCHEMA = 'k4-fieldbook-experiments-v1';
export const MAX_EXPERIMENTS = 2_000;

const TECHNIQUE_STATUSES: TechniqueStatus[] = [
  'pending',
  'active',
  'tested',
  'rejected',
  'promising',
  'validated',
];
const SECTIONS: Array<SectionId | 'custom'> = ['K1', 'K2', 'K3', 'K4', 'custom'];

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isBoundedString(value: unknown, maxLength: number): value is string {
  return typeof value === 'string' && value.length <= maxLength;
}

export function isTechniqueStatus(value: unknown): value is TechniqueStatus {
  return typeof value === 'string' && TECHNIQUE_STATUSES.includes(value as TechniqueStatus);
}

export function isTechniqueStatusMap(value: unknown): value is Record<string, TechniqueStatus> {
  return (
    isRecord(value) &&
    Object.entries(value).every(
      ([key, status]) => key.length <= 100 && isTechniqueStatus(status),
    )
  );
}

export function isResearchNotes(value: unknown): value is string {
  return isBoundedString(value, 500_000);
}

export function isExperiment(value: unknown): value is Experiment {
  if (!isRecord(value) || !isRecord(value.provenance)) return false;
  const provenance = value.provenance;
  if (!isRecord(provenance.parameters)) return false;

  return (
    isBoundedString(value.id, 100) &&
    isBoundedString(value.createdAt, 50) &&
    !Number.isNaN(Date.parse(value.createdAt)) &&
    isBoundedString(value.title, 500) &&
    typeof value.section === 'string' &&
    SECTIONS.includes(value.section as SectionId | 'custom') &&
    isBoundedString(value.method, 500) &&
    isBoundedString(value.operation, 100) &&
    isBoundedString(value.key, 20_000) &&
    isBoundedString(value.alphabet, 1_000) &&
    isBoundedString(value.input, 500_000) &&
    isBoundedString(value.output, 500_000) &&
    isBoundedString(value.notes, 100_000) &&
    isTechniqueStatus(value.status) &&
    isBoundedString(provenance.appVersion, 50) &&
    isBoundedString(provenance.inputFingerprint, 200) &&
    isBoundedString(provenance.indexConvention, 500) &&
    isBoundedString(provenance.searchSpace, 2_000) &&
    isBoundedString(provenance.corpus, 2_000) &&
    isBoundedString(provenance.scoring, 2_000) &&
    isBoundedString(provenance.seed, 500) &&
    typeof provenance.elapsedMs === 'number' &&
    Number.isFinite(provenance.elapsedMs) &&
    provenance.elapsedMs >= 0 &&
    isBoundedString(provenance.hardware, 2_000) &&
    typeof provenance.candidatesTested === 'number' &&
    Number.isInteger(provenance.candidatesTested) &&
    provenance.candidatesTested >= 0 &&
    isBoundedString(provenance.holdout, 2_000) &&
    isBoundedString(provenance.negativeControl, 2_000) &&
    Object.entries(provenance.parameters).every(
      ([key, parameter]) => key.length <= 200 && isBoundedString(parameter, 20_000),
    )
  );
}

export function isExperimentArray(value: unknown): value is Experiment[] {
  return (
    Array.isArray(value) &&
    value.length <= MAX_EXPERIMENTS &&
    value.every(isExperiment) &&
    new Set(value.map((experiment) => experiment.id)).size === value.length
  );
}

export function mergeExperimentRecords(
  local: Experiment[],
  external: Experiment[],
): Experiment[] {
  const records = new Map<string, Experiment>();
  local.forEach((experiment) => records.set(experiment.id, experiment));
  external.forEach((experiment) => records.set(experiment.id, experiment));
  return [...records.values()]
    .sort((a, b) => b.createdAt.localeCompare(a.createdAt) || a.id.localeCompare(b.id))
    .slice(0, MAX_EXPERIMENTS);
}

export function contentFingerprint(value: string): string {
  let hash = 0x811c9dc5;
  for (let index = 0; index < value.length; index += 1) {
    hash ^= value.charCodeAt(index);
    hash = Math.imul(hash, 0x01000193);
  }
  return `fnv1a32:${(hash >>> 0).toString(16).padStart(8, '0')}:${value.length}`;
}
