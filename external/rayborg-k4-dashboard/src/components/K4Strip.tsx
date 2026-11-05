import { K4_CIPHER, K4_KNOWN_PLAIN } from '../data/kryptos';

interface K4StripProps {
  compact?: boolean;
  focusStart?: number;
  focusEnd?: number;
}

export function K4Strip({ compact = false, focusStart, focusEnd }: K4StripProps) {
  return (
    <div className={`k4-strip ${compact ? 'k4-strip-compact' : ''}`}>
      {K4_CIPHER.split('').map((char, index) => {
        const position = index + 1;
        const plain = K4_KNOWN_PLAIN[index];
        const focused =
          typeof focusStart === 'number' &&
          typeof focusEnd === 'number' &&
          position >= focusStart &&
          position <= focusEnd;
        return (
          <div
            className={`k4-cell ${plain ? 'is-known' : ''} ${focused ? 'is-focused' : ''}`}
            key={position}
            title={`K4 position ${position}${plain ? `: ${char} → ${plain}` : `: ${char}`}`}
          >
            <span className="k4-index">{position}</span>
            <span className="k4-cipher-char">{char}</span>
            <span className="k4-plain-char">{plain || '·'}</span>
          </div>
        );
      })}
    </div>
  );
}
