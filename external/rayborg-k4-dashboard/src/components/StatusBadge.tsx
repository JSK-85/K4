import type { TechniqueStatus } from '../types';

export const STATUS_LABELS: Record<TechniqueStatus, string> = {
  pending: 'Not run',
  active: 'Active',
  tested: 'Tested',
  rejected: 'Rejected',
  promising: 'Promising',
  validated: 'Validated',
};

export function StatusBadge({ status }: { status: TechniqueStatus }) {
  return <span className={`status-badge status-${status}`}>{STATUS_LABELS[status]}</span>;
}
