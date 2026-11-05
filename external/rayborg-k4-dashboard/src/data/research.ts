import type { ResearchSource, TimelineEvent } from '../types';

export const RESEARCH_AS_OF = '2026-07-27';

export const RESEARCH_SOURCES: ResearchSource[] = [
  {
    id: 'cia-kryptos',
    title: '“Kryptos” Sculpture',
    publisher: 'Central Intelligence Agency',
    date: 'Current institutional record',
    url: 'https://www.cia.gov/legacy/headquarters/kryptos-sculpture/',
    tier: 'institutional',
    scope:
      'Commission, dedication, materials, installation anatomy, canonical panel transcription and tableau.',
  },
  {
    id: 'cia-stein',
    title: 'Cracking the Courtyard Crypto',
    publisher: 'CIA Reading Room / Studies in Intelligence',
    date: '1999; declassified 2013',
    url: 'https://www.cia.gov/readingroom/document/06712772',
    tier: 'institutional',
    scope: 'David Stein’s pencil-and-paper K1–K3 solution account and discovery process.',
  },
  {
    id: 'cia-foia-history',
    title: 'Kryptos institutional record',
    publisher: 'CIA Reading Room',
    date: 'Declassified record',
    url: 'https://www.cia.gov/readingroom/document/06498615',
    tier: 'institutional',
    scope: 'Commission background and Agency description of Sanborn’s collaboration.',
  },
  {
    id: 'smithsonian-papers',
    title: 'Jim Sanborn papers, circa 1945–2024',
    publisher: 'Smithsonian Archives of American Art',
    date: 'Finding aid updated 2026',
    url: 'https://www.aaa.si.edu/collections/jim-sanborn-papers-22298',
    tier: 'institutional',
    scope: '16.1-linear-foot archive provenance, scope and 2023/2026 donations.',
  },
  {
    id: 'smithsonian-series',
    title: 'Series 3: Commission Files',
    publisher: 'Smithsonian Archives of American Art',
    date: 'Finding aid updated 2026',
    url: 'https://www.aaa.si.edu/collections/jim-sanborn-papers-22298/series-3',
    tier: 'institutional',
    scope: 'Kryptos pre-production, code research, dedication, attempts and cracked-code folders.',
  },
  {
    id: 'smithsonian-oral-history',
    title: 'Oral history interview with Jim Sanborn',
    publisher: 'Smithsonian Archives of American Art',
    date: '2009; artist-reviewed 2020',
    url: 'https://www.aaa.si.edu/collections/interviews/oral-history-interview-jim-sanborn-15700',
    tier: 'primary',
    scope: 'Six-and-a-half-hour creator interview on the commission and Sanborn’s wider practice.',
  },
  {
    id: 'sanborn-site',
    title: 'Jim Sanborn: Kryptos and public works',
    publisher: 'Jim Sanborn',
    date: 'Current artist site',
    url: 'https://www.jimsanborn.net/main.html',
    tier: 'primary',
    scope: 'Artist statement, dimensions, materials, related works and 2025 archive notice.',
  },
  {
    id: 'sanborn-interview-2005',
    title: 'Questions for Kryptos’ Creator',
    publisher: 'WIRED',
    date: '2005-01-20',
    url: 'https://www.wired.com/2005/01/questions-for-kryptos-creator/',
    tier: 'primary',
    scope:
      'Direct Sanborn interview on five or six techniques, visual systems, WW, related works and on-site effects.',
  },
  {
    id: 'nyt-1999',
    title: 'C.I.A.’s Artistic Enigma Yields All but Final Clue',
    publisher: 'The New York Times',
    date: '1999-06-16',
    url: 'https://archive.nytimes.com/www.nytimes.com/library/tech/99/06/biztech/articles/16code.html',
    tier: 'reporting',
    scope: 'Contemporary account of Gillogly’s public solution and CIA acknowledgment.',
  },
  {
    id: 'wired-nsa-2013',
    title: 'Documents Reveal How the NSA Cracked Kryptos',
    publisher: 'WIRED',
    date: '2013-07-10',
    url: 'https://www.wired.com/2013/07/nsa-cracked-kryptos-before-cia/',
    tier: 'reporting',
    scope: 'NSA FOIA records, 1992–93 task force, cipher diagnoses and solution chronology.',
  },
  {
    id: 'npr-clue-2010',
    title: 'Kryptos Sculptor Drops New Clue',
    publisher: 'NPR',
    date: '2010-11-22',
    url: 'https://www.npr.org/2010/11/22/131520768/-kryptos-sculptor-drops-new-clue-in-20-year-mystery',
    tier: 'primary',
    scope: 'Creator interview accompanying the BERLIN crib release.',
  },
  {
    id: 'wired-clue-2014',
    title: 'Finally, a New Clue to Solve Kryptos',
    publisher: 'WIRED',
    date: '2014-11-20',
    url: 'https://www.wired.com/2014/11/second-kryptos-clue/',
    tier: 'primary',
    scope: 'CLOCK release and Sanborn’s then-stated interest in Binninger’s Mengenlehreuhr.',
  },
  {
    id: 'nyt-clue-2020',
    title: 'This Sculpture Holds a Decades-Old C.I.A. Mystery',
    publisher: 'The New York Times',
    date: '2020-01-29',
    url: 'https://www.nytimes.com/interactive/2020/01/29/climate/kryptos-sculpture-final-clue.html',
    tier: 'primary',
    scope: 'NORTHEAST release, exact positions and Scheidt’s “masking technique” statement.',
  },
  {
    id: 'bean-2021',
    title: 'Cryptodiagnosis of “Kryptos K4”',
    publisher: 'HistoCrypt 2021',
    date: '2021-08-09',
    url: 'https://doi.org/10.3384/ecp183153',
    tier: 'academic',
    scope:
      'Peer-reviewed permutation tests, one-to-one relationship evidence and Gromark hypothesis.',
  },
  {
    id: 'matrix-paper',
    title: 'James Sanborn’s Kryptos and the matrix encryption conjecture',
    publisher: 'Cryptologia 40(6)',
    date: '2016',
    url: 'https://doi.org/10.1080/01611194.2016.1141556',
    tier: 'academic',
    scope: 'Technical examination of proposed matrix-encryption approaches to K4.',
  },
  {
    id: 'k2-correction',
    title: 'The Kryptos Group announces a corrected answer to Part 2',
    publisher: 'Elonka Dunin / Kryptos Group',
    date: '2006-04-19',
    url: 'https://www.elonka.com/kryptos/CorrectedK2Announcement.html',
    tier: 'community',
    scope: 'Reproducible missing-S correction from IDBYROWS to XLAYERTWO, confirmed by Sanborn.',
  },
  {
    id: 'sanborn-letter-aug-2025',
    title: 'Open letter to the Kryptos community',
    publisher: 'Jim Sanborn via Elonka Dunin',
    date: '2025-08-14',
    url: 'https://elonka.com/kryptos/OpenLetterAug2025.html',
    tier: 'primary',
    scope:
      'Creator statement marking “what’s the point?” and the power of secrecy as a clue, and linking K4’s continuing riddle to K5.',
  },
  {
    id: 'wired-auction-2025',
    title: 'The Kryptos Key Is Going Up for Sale',
    publisher: 'WIRED',
    date: '2025-08-14',
    url: 'https://www.wired.com/story/jim-sanborn-auctions-kryptos-key/',
    tier: 'reporting',
    scope:
      'Direct Sanborn interview and report that K4’s text is an instruction that may involve the wider installation.',
  },
  {
    id: 'sciam-discovery-2025',
    title: 'A Solution to the CIA’s Kryptos Code Is Found after 35 Years',
    publisher: 'Scientific American',
    date: '2025-10-16',
    url: 'https://www.scientificamerican.com/article/a-solution-to-the-cias-kryptos-code-is-found-after-35-years/',
    tier: 'reporting',
    scope:
      'Sanborn-confirmed archival plaintext discovery; confirms EAST NORTHEAST and BERLIN CLOCK.',
  },
  {
    id: 'wired-discovery-2025',
    title: 'Inside the Messy, Accidental Kryptos Reveal',
    publisher: 'WIRED',
    date: '2025-10-24',
    url: 'https://www.wired.com/story/kryptos-code-reveal/',
    tier: 'reporting',
    scope: 'Participant interviews, archive discovery sequence and “discovered, not deciphered” distinction.',
  },
  {
    id: 'sciam-final-clues-2025',
    title: 'Final Clues to Mystery of CIA Kryptos Puzzle Released',
    publisher: 'Scientific American',
    date: '2025-11-12',
    url: 'https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/',
    tier: 'reporting',
    scope:
      'Reported account with direct Sanborn quotations and a link to his final open letter.',
  },
  {
    id: 'sanborn-letter-2025',
    title: 'Open letter to the Kryptos community',
    publisher: 'Jim Sanborn via DocumentCloud',
    date: '2025-11-12',
    url: 'https://www.documentcloud.org/documents/26229389-adobe-scan-nov-12-2025/',
    tier: 'primary',
    scope:
      'Creator’s final written clues: Egypt, Berlin Wall, World Clock, message delivery, hypothetical hidden-site conditions and K5.',
  },
  {
    id: 'rr-auction-2025',
    title: 'The Complete Secrets of Kryptos: Jim Sanborn’s Private Archive',
    publisher: 'RR Auction',
    date: 'Closed 2025-11-20',
    url: 'https://www.rrauction.com/auctions/lot-detail/350761607302001-the-complete-secrets-of-kryptos-jim-sanborns-private-archive/',
    tier: 'primary',
    scope: 'Archive inventory, disclosures and $962,500 sale result including buyer’s premium.',
  },
  {
    id: 'paradigm-2026',
    title: 'Project Kryptos',
    publisher: 'Paradigm',
    date: '2026-06-12',
    url: 'https://www.paradigm.xyz/writing/kryptos',
    tier: 'primary',
    scope:
      'Current steward’s self-reported answer-blind design, $1 submission fee and future K5 release.',
  },
  {
    id: 'paradigm-index',
    title: 'Kryptos K4 indexed transcription',
    publisher: 'Paradigm',
    date: '2026',
    url: 'https://paradigm.xyz/kryptos/',
    tier: 'primary',
    scope: 'Current owner’s one-based, letter-by-letter K4 transcription and verifier entry point.',
  },
];

export const TIMELINE: TimelineEvent[] = [
  {
    date: '1988',
    title: 'Sanborn selected',
    detail:
      'A joint GSA/CIA panel selected Jim Sanborn’s proposal for a $250,000 Art-in-Architecture commission in November.',
    sourceIds: ['cia-kryptos'],
    kind: 'artwork',
  },
  {
    date: '1988–1990',
    title: 'Codes and installation developed',
    detail:
      'Sanborn worked about four months with retired CIA cryptographer Edward M. Scheidt, then modified historical systems and added visual systems of his own.',
    sourceIds: ['cia-kryptos', 'sanborn-interview-2005'],
    kind: 'artwork',
  },
  {
    date: '1990-11-03',
    title: 'Kryptos dedicated',
    detail:
      'The two-part installation was dedicated at CIA headquarters. The encoded screen, entrance plates, Morse, compass, lodestone, granite, water and petrified wood form one artwork.',
    sourceIds: ['cia-kryptos'],
    kind: 'artwork',
  },
  {
    date: '1991',
    title: 'NSA transcription begins',
    detail: 'NSA visitors copied the panel text during a CIA visit and brought it back for analysis.',
    sourceIds: ['wired-nsa-2013'],
    kind: 'solution',
  },
  {
    date: '1992–1993',
    title: 'NSA solves K1–K3',
    detail:
      'An informal NSA task force responding to a CIA challenge solved the first three sections, then stopped work on short K4 as disproportionate to operational priorities.',
    sourceIds: ['wired-nsa-2013'],
    kind: 'solution',
  },
  {
    date: '1998',
    title: 'David Stein solves K1–K3',
    detail: 'The CIA analyst used pencil and paper over roughly 400 lunch-hour hours.',
    sourceIds: ['cia-stein'],
    kind: 'solution',
  },
  {
    date: '1999-06',
    title: 'Jim Gillogly announces public solution',
    detail:
      'Gillogly independently solved and publicly announced K1–K3 with computer assistance, prompting acknowledgment of earlier internal solutions.',
    sourceIds: ['nyt-1999'],
    kind: 'solution',
  },
  {
    date: '2006-04',
    title: 'K2 ending corrected',
    detail:
      'A ciphertext S omitted for visual balance was virtually restored, changing the accidental IDBYROWS ending to intended XLAYERTWO.',
    sourceIds: ['k2-correction'],
    kind: 'solution',
  },
  {
    date: '2010',
    title: 'BERLIN crib released',
    detail: 'K4 positions 64–69, NYPVTT, were confirmed to decrypt to BERLIN.',
    sourceIds: ['npr-clue-2010'],
    kind: 'clue',
  },
  {
    date: '2014',
    title: 'CLOCK crib released',
    detail:
      'Positions 70–74 extended the phrase to BERLINCLOCK. Sanborn highlighted Binninger’s unusual set-theory clock at the time.',
    sourceIds: ['wired-clue-2014'],
    kind: 'clue',
  },
  {
    date: '2020',
    title: 'NORTHEAST crib released',
    detail:
      'Positions 26–34 were disclosed. Scheidt described K4 as using an additional masking technique.',
    sourceIds: ['nyt-clue-2020'],
    kind: 'clue',
  },
  {
    date: '2021',
    title: 'Peer-reviewed cryptodiagnosis',
    detail:
      'Richard Bean reported strong statistical evidence for a positionwise one-to-one relation and identified Gromark as a family worth prioritizing, not a solution.',
    sourceIds: ['bean-2021'],
    kind: 'solution',
  },
  {
    date: '2025-08-14',
    title: 'Point, power and instruction clues',
    detail:
      'Sanborn marked “what’s the point? Power resides with a secret, not without it” as a clue and wrote that K4’s riddle persists as K5. WIRED reported that K4’s text is an instruction that may involve the wider installation. No new plaintext positions were disclosed.',
    sourceIds: ['sanborn-letter-aug-2025', 'wired-auction-2025'],
    kind: 'clue',
  },
  {
    date: '2025-09',
    title: 'Plaintext recovered from archive',
    detail:
      'Jarett Kobek and Richard Byrne reconstructed K4 plaintext from Sanborn papers photographed at the Smithsonian. Sanborn confirmed it; they did not publish it or derive the cipher method.',
    sourceIds: ['sciam-discovery-2025', 'wired-discovery-2025'],
    kind: 'archive',
  },
  {
    date: '2025-11-12',
    title: 'Final creator clues',
    detail:
      'Sanborn said his late-1986 Egypt trip and the 1989 fall of the Berlin Wall influenced plaintext he was writing in 1988, leaving a chronology conflict. He identified the World Clock and “delivering a message,” tied K5 to K2 and the same-position BERLINCLOCK, and said any hypothetical on-site remnant would need to be “semi ephemeral, undetectable and carefully hidden.”',
    sourceIds: ['sanborn-letter-2025', 'sciam-final-clues-2025'],
    kind: 'clue',
  },
  {
    date: '2025-11-20',
    title: 'Private archive sold',
    detail:
      'The archive, represented by Sanborn and RR as containing the K4 plaintext and method, original charts and K5 material, sold for $962,500 including premium.',
    sourceIds: ['rr-auction-2025'],
    kind: 'archive',
  },
  {
    date: '2026-06-12',
    title: 'Paradigm reveals stewardship',
    detail:
      'Paradigm announced it had bought the archive and says it remained answer-blind while deploying a SHA-256/HMAC-backed verifier. It reports K4 still publicly unsolved.',
    sourceIds: ['paradigm-2026'],
    kind: 'archive',
  },
];

export const ESTABLISHED_FACTS = [
  {
    label: 'Physical system',
    value:
      'Two-part installation: entrance granite/copper works plus courtyard copper screen, pools, granite, petrified wood, lodestone and compass rose.',
    sourceIds: ['cia-kryptos'],
  },
  {
    label: 'Screen count',
    value:
      '1,735 alphabetic cutouts across both screen halves. The encoded side has 865 letters plus four question marks.',
    sourceIds: ['cia-kryptos'],
  },
  {
    label: 'K4 indexing',
    value:
      'Exactly 97 letters, beginning O at local position 1. Keep punctuation-counted and global indices separate.',
    sourceIds: ['cia-kryptos', 'paradigm-index'],
  },
  {
    label: 'Known K4 plaintext',
    value:
      'Positions 22–34 are EASTNORTHEAST; positions 64–74 are BERLINCLOCK. 24 of 97 positions are public.',
    sourceIds: ['sciam-discovery-2025', 'nyt-clue-2020', 'wired-clue-2014'],
  },
  {
    label: '2025 contextual clues',
    value:
      'Sanborn marked “what’s the point? Power resides with a secret, not without it” as a clue; WIRED reported K4’s text as an instruction that may involve the wider installation. Later clues added Egypt, the Berlin Wall, the World Clock, message delivery, K5 overlap and a hypothetical “semi ephemeral, undetectable and carefully hidden” on-site remnant. None fixes a new K4 plaintext position.',
    sourceIds: [
      'sanborn-letter-aug-2025',
      'wired-auction-2025',
      'sanborn-letter-2025',
      'sciam-final-clues-2025',
    ],
  },
  {
    label: 'Present status',
    value:
      'The private plaintext was recovered and confirmed by Sanborn, but no public derivation, key or method exists. “Recovered” and “deciphered” are not interchangeable here.',
    sourceIds: ['wired-discovery-2025', 'paradigm-2026'],
  },
];

export const OPEN_QUESTIONS = [
  {
    title: 'What is the masking technique?',
    detail:
      'Scheidt confirmed an extra layer but no public source defines its mechanics. Test hybrids without treating “masking” as a named cipher.',
  },
  {
    title: 'How do earlier instructions bind to K4?',
    detail:
      'Sanborn said earlier text contains instructions referring to later text; WIRED later reported that K4’s text is itself an instruction that may involve the wider installation. XLAYERTWO, anomalies, directions and physical layout remain live evidence, not established keys.',
  },
  {
    title: 'What is “the point”?',
    detail:
      'Sanborn explicitly paired “what’s the point?” with “Power resides with a secret, not without it.” Compass, clock, location, punctuation, purpose and secrecy readings must be tested separately; the clue supplies no fixed positions.',
  },
  {
    title: 'Which Berlin clock mechanics matter?',
    detail:
      'The 2014 interview emphasized the Mengenlehreuhr; in 2025 Sanborn said the plaintext reference means the World Clock. Preserve the chronology and test each hypothesis separately.',
  },
  {
    title: 'What does “delivering a message” constrain?',
    detail:
      'It may describe theme, tradecraft, route, medium or mechanism. It supplies no fixed positions and must not be overfit.',
  },
  {
    title: 'How does K5 overlap?',
    detail:
      'Sanborn says the future 97-character K5 uses a similar system, repeats BERLINCLOCK at the same positions and relates to K2’s buried-message theme. His hypothetical “semi ephemeral, undetectable and carefully hidden” language does not prove an object exists. K5’s ciphertext is not yet public.',
  },
];

export const TRANSCRIPTION_NOTES = [
  'K1 has 63 letters and preserves IQLUSION.',
  'K2 has 369 physical letters plus three question marks. A virtual S inserted nine positions from the end restores key alignment and XLAYERTWO.',
  'K3 has 336 letters plus the terminal sculpture question mark. The plaintext uses DESPARATLY and ends with the encoded separator Q.',
  'K4 starts at O in ...DOHW?OBKR. The question mark belongs to K3 under the standard 97-letter sectioning.',
  'K4 begins at alphabet-only global position 769, or visible-character position 773 when the four earlier question marks are counted.',
  'Plaintext spaces and punctuation are editorial. X and Q carry separator/punctuation roles in the solved sections.',
];
