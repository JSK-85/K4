import { describe, expect, it } from 'vitest';
import { createShadowRuns, punctuationLayout } from './shadowRuns';

describe('K1–K3 shadow suite', () => {
  it('executes a control for every solved section', () => {
    const sections = new Set(createShadowRuns().map((run) => run.section));
    expect(sections).toEqual(new Set(['K1', 'K2', 'K3']));
  });

  it('passes every exact-answer control', () => {
    const runs = createShadowRuns();
    expect(runs).toHaveLength(5);
    expect(runs.filter((run) => !run.passed)).toEqual([]);
  });

  it('tracks punctuation at alphabetic offsets', () => {
    expect(punctuationLayout('AB?CD!')).toBe('2:?|4:!');
    expect(punctuationLayout('ABCD')).not.toBe(punctuationLayout('AB?CD'));
  });
});
