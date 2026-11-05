# Kryptos Research Dossier

**Research cutoff:** 2026-07-27
**Scope:** the complete Kryptos installation, K1-K4 cryptanalysis, public clues, archival developments, source conflicts, and reproducible K4 research priorities.

## Executive Finding

K1, K2, and K3 have publicly known plaintexts and reproducible methods. K4 has a more nuanced status:

- Writers Jarett Kobek and Richard Byrne reconstructed its plaintext from Jim Sanborn papers that were available at the Smithsonian Archives of American Art in September 2025. Sanborn confirmed that their text was correct; it has not been independently reproduced from the cipher method. They have not published it. [Scientific American, 2025](https://www.scientificamerican.com/article/a-solution-to-the-cias-kryptos-code-is-found-after-35-years/), [WIRED, 2025](https://www.wired.com/story/kryptos-code-reveal/)
- They did not derive the plaintext from the sculpture's 97-letter ciphertext and did not recover Sanborn's encryption method. Sanborn's distinction was: "They only discovered it, they did not decipher it." [WIRED, 2025](https://www.wired.com/story/kryptos-code-reveal/)
- Sanborn's private archive, including his K4 plaintext, method, working charts, and K5 material, sold on November 20, 2025 for **$962,500 including buyer's premium**. [RR Auction](https://www.rrauction.com/auctions/lot-detail/350761607302001-the-complete-secrets-of-kryptos-jim-sanborns-private-archive/)
- Paradigm identified itself as the buyer on June 12, 2026. It says its personnel deliberately avoided seeing the answer. Sanborn typed the plaintext on a dedicated new computer; software hashed it with SHA-256 and sent the hash to Google Cloud KMS for an HMAC verification tag, after which the computer was wiped. Paradigm now offers a paid verifier and continues to describe K4 as unsolved. These answer-blind and verifier-integrity claims are self-reported; no independent audit or public implementation was identified. [Paradigm, 2026](https://www.paradigm.xyz/writing/kryptos)

The precise project status is therefore **plaintext privately recovered and confirmed by Sanborn; plaintext unpublished; encryption method publicly unsolved**.

## Commission And Intent

- Kryptos was commissioned for the CIA's New Headquarters Building through the federal General Services Administration Art-in-Architecture program. The selection team combined CIA Fine Arts Commission members, CIA employees, and outside experts led by the National Endowment for the Arts. [CIA](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- The commission was **$250,000**. The panel selected Washington-area sculptor Jim Sanborn's proposal in November 1988. *Kryptos* is Greek for "hidden." [CIA](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- CIA calls it a two-part installation whose theme is **"intelligence gathering."** It begins at the entrance to the New Headquarters Building and continues into the northwest courtyard. [CIA](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- The CIA gives the dedication date as **November 3, 1990**. The copyright/conception mark is 1988, while Sanborn's own catalog labels the work *Kryptos, 1989*. These dates describe different stages rather than necessarily conflicting. [CIA](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/), [Jim Sanborn](https://www.jimsanborn.net/main.html)
- Sanborn worked for about four months with Edward M. Scheidt, retired chairman of the CIA Cryptographic Center. Scheidt introduced historical and contemporary systems; Sanborn modified systems and added visual methods of his own. [CIA](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/), [Sanborn interview](https://www.wired.com/2005/01/questions-for-kryptos-creator/)
- Sanborn estimated that he used "five or six" cryptographic techniques. He said earlier text contains instructions referring to later text and emphasized visual systems that are individual to the artwork. [Sanborn interview](https://www.wired.com/2005/01/questions-for-kryptos-creator/)
- CIA says Sanborn wrote the encoded content in collaboration with a prominent fiction writer, but no authoritative public source identifies that person. Unsupported internet attributions should not be promoted to fact. [CIA](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)

## The Complete Installation

The famous S-shaped screen is only the courtyard centerpiece.

### Entrance

- Two red-granite and copperplate constructions flank the walkway.
- Their layered copper carries International Morse code and older cipher forms.
- A naturally magnetized lodestone is co-located with a navigational compass rose.
- Sanborn described the code systems as increasing in sophistication as a visitor proceeds farther into CIA grounds.

### Courtyard

- A large S-shaped copper screen resembles paper emerging from a printer.
- Petrified wood supports or stands alongside the screen.
- A bubbling pool sits within the curving screen; a calm reflecting pool, layered granite slabs, grasses, benches, and additional stones complete the landscape.
- CIA says the petrified wood refers both to trees formerly on the site and to historical writing material. The bubbling water represents information being disseminated toward an unknown destination.
- Sanborn lists the materials as granite, quartz, lodestone, copper, encoded text, and water, and gives overall dimensions of **12 x 20 x 10 feet**. [Jim Sanborn](https://www.jimsanborn.net/main.html)

Primary institutional description: [CIA Kryptos sculpture](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/).

## Screen And Transcription Controls

- The copper screen has **1,735 alphabetic cutouts** across its two halves. [CIA](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- The encoded half contains 865 letters plus four physical question marks, or 869 visible encoded characters.
- The opposite half contains the keyed tableau and ordinary alphabet margins. The mixed alphabet is `KRYPTOSABCDEFGHIJLMNQUVWXZ`, each letter used once.
- From the courtyard front, the tableau is intentionally viewed from its reverse side.
- Section boundaries are inferred, not physically labeled.

| Section | Letters | Question marks | Standard boundary |
|---|---:|---:|---|
| K1 | 63 | 0 | `EMU...MFD` |
| K2 | 369 | 3 | `VFP...ETG` |
| K3 | 336 | 1 | `END...OHW?` |
| K4 | 97 | 0 | `OBK...CAR` |

The standard K3/K4 split is `...TVDOHW?OBKR...`: the question mark completes K3 and K4 begins at `O`. Older transcriptions sometimes display `?OBKR` together, but counting the question mark in K4 would contradict its established 97-letter length.

### K4 Canonical Ciphertext

```text
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
```

One-based local positions are the required reporting convention. Paradigm provides an owner-maintained indexed transcription. [Paradigm indexed K4](https://paradigm.xyz/kryptos/)

Global alternatives must be labeled explicitly:

- K4 begins at alphabet-only global position **769**.
- K4 begins at visible encoded-character position **773** if K2's three question marks and K3's final question mark are counted.

### Physical And Spelling Anomalies

- `IQLUSION` appears in K1 plaintext.
- `UNDERGRUUND` appears in K2 plaintext.
- `DESPARATLY` appears in K3 plaintext.
- K2 is missing a ciphertext `S` near its end. This is a documented production/editing error, not merely an eccentric spelling.
- Three raised letters commonly transcribed as `YAR` occur near the beginning of K3. Their meaning is not established.
- Plaintext spacing and ordinary punctuation are editorial. `X` often works as a stop/separator; K3's `Q` represents the final spoken question marker before the physical `?`.

Sanborn has sometimes described misspellings as intentional, but surviving coding-chart evidence and his acknowledged K2 omission show that each anomaly must be assessed independently.

## Morse Layer, Sometimes Called K0

CIA confirms that entrance copperplates contain International Morse code, but it does not publish an authoritative complete transcription. Photographic community transcriptions commonly include fragments such as:

```text
VIRTUALLY INVISIBLE
DIGETAL
INTERPRETATIT
SHADOW FORCES
LUCID MEMORY
T IS YOUR POSITION
SOS
RQ
```

Many isolated dots can be read as `E` or as spacing/filler. `DIGETAL` is visibly misspelled. The ending of `INTERPRETATIT` is disputed across transcriptions. K0 wording, order, punctuation, and isolated signals should therefore be tagged as community reconstruction, not equated with the CIA's K1-K4 transcription.

## K1

### Cipher And Method

- 63 letters
- Keyed alphabet: `KRYPTOSABCDEFGHIJLMNQUVWXZ`
- Indicator key: `PALIMPSEST`
- Family: periodic polyalphabetic substitution, commonly described as a Quagmire III variant or keyed-alphabet Vigenere
- The operation can be reproduced by indexing both ciphertext and key in the mixed alphabet and subtracting key index from ciphertext index.

### Plaintext

```text
BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION
```

The NSA described ten repeating alphabets, matching the ten-letter key. [NSA history reported from FOIA documents](https://www.wired.com/2013/07/nsa-cracked-kryptos-before-cia/)

Sanborn has said `IQLUSION` was intentional. Some reported working-chart evidence instead suggests a key anomaly such as `PALIMPCEST` may have produced it. The plaintext itself is certain; the production intent behind the anomaly is less certain.

## K2

### Cipher And Method

- 369 physical letters plus three question marks
- Keyed alphabet: `KRYPTOSABCDEFGHIJLMNQUVWXZ`
- Indicator key: `ABSCISSA`
- Same broad keyed-polyalphabetic family as K1
- Question marks are preserved and do not advance the alphabetic key

### Plaintext

```text
IT WAS TOTALLY INVISIBLE. HOW'S THAT POSSIBLE?
THEY USED THE EARTH'S MAGNETIC FIELD. X
THE INFORMATION WAS GATHERED AND TRANSMITTED UNDERGRUUND
TO AN UNKNOWN LOCATION. X
DOES LANGLEY KNOW ABOUT THIS? THEY SHOULD: IT'S BURIED OUT THERE SOMEWHERE. X
WHO KNOWS THE EXACT LOCATION? ONLY WW. THIS WAS HIS LAST MESSAGE. X
THIRTY EIGHT DEGREES FIFTY SEVEN MINUTES SIX POINT FIVE SECONDS NORTH.
SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST. X LAYER TWO.
```

- Sanborn confirmed that `WW` means William Webster, CIA director when Kryptos was completed. [Sanborn interview](https://www.wired.com/2005/01/questions-for-kryptos-creator/)
- The coordinates are part of the plaintext. Public claims that they prove a specific buried object or mark the later CIA Berlin Wall monument are hypotheses, not established results.
- `UNDERGRUUND` is the sculpture's recovered spelling.

### Missing-S Correction

Earlier solutions ended `...WESTIDBYROWS`. In 2006 Sanborn disclosed that he had removed a ciphertext character for visual balance without realizing the downstream key-alignment effect. Inserting ciphertext `S` nine letters from the end changes:

```text
...UPLGEWJLLAETG  ->  ...UPLGESWJLLAETG
...WESTIDBYROWS   ->  ...WESTXLAYERTWO
```

The Kryptos Group reconstructed this insertion and Sanborn confirmed the corrected plaintext. [Detailed K2 correction record](https://www.elonka.com/kryptos/CorrectedK2Announcement.html)

The physical and corrected versions are both valuable regression fixtures: software should reproduce the accidental result from the sculpture and the intended result from the documented virtual insertion.

## K3

### Plaintext

K3 paraphrases Howard Carter's account of opening Tutankhamun's tomb in November 1922. It is not a verbatim diary quotation.

```text
SLOWLY, DESPARATLY SLOWLY, THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED
THE LOWER PART OF THE DOORWAY WAS REMOVED. WITH TREMBLING HANDS I MADE A
TINY BREACH IN THE UPPER LEFT HAND CORNER. AND THEN, WIDENING THE HOLE A
LITTLE, I INSERTED THE CANDLE AND PEERED IN. THE HOT AIR ESCAPING FROM THE
CHAMBER CAUSED THE FLAME TO FLICKER, BUT PRESENTLY DETAILS OF THE ROOM
WITHIN EMERGED FROM THE MIST. X CAN YOU SEE ANYTHING? Q
```

Lord Carnarvon's question is represented; Carter's famous answer is not.

### Exact Reproducible Route

Over the 336 letters, excluding the physical final question mark:

1. Write plaintext row-major into an `8 x 42` grid.
2. Read columns left to right, each column bottom to top.
3. Write that stream row-major into a `24 x 14` grid.
4. Again read columns left to right, each column bottom to top.

This produces the CIA's K3 ciphertext exactly. In geometric language, each stage is equivalent to a 90-degree clockwise rotation followed by row-major serialization. Several public reverse descriptions are equivalent; an equivalent reconstruction should not automatically be labeled Sanborn's original construction sequence.

The NSA correctly diagnosed a transposition family by inspection and recovered the text by hand. [WIRED / NSA documents](https://www.wired.com/2013/07/nsa-cracked-kryptos-before-cia/)

## Solution Chronology

- NSA interns transcribed the sculpture during a 1991 CIA visit.
- After a formal CIA challenge, an NSA task force formed in November 1992. Declassified records say three analysts solved K1-K3 rapidly, with the accomplishment reported internally in June 1993. Work on K4 stopped because a short text under suspected methods would demand resources disproportionate to the recreational task. [WIRED / NSA records](https://www.wired.com/2013/07/nsa-cracked-kryptos-before-cia/)
- CIA analyst David Stein independently solved K1-K3 in 1998 with pencil and paper after roughly 400 hours. [CIA Reading Room](https://www.cia.gov/readingroom/document/06712772)
- Computer scientist Jim Gillogly independently solved and publicly announced K1-K3 in June 1999 using computer assistance. He was the first public independent announcer, not the first person known to have solved them. [Contemporary New York Times report](https://archive.nytimes.com/www.nytimes.com/library/tech/99/06/biztech/articles/16code.html)
- The K2 correction was established and confirmed in April 2006.

## K4 Public Plaintext

| Positions | Ciphertext | Plaintext | Public record |
|---:|---|---|---|
| 22-25 | `FLRV` | `EAST` | Confirmed in the Sanborn-verified 2025 archival recovery |
| 26-34 | `QQPRNGKSS` | `NORTHEAST` | Released by Sanborn in 2020 |
| 64-69 | `NYPVTT` | `BERLIN` | Released by Sanborn in 2010 |
| 70-74 | `MZFPK` | `CLOCK` | Released by Sanborn in 2014 |

The two contiguous confirmed blocks are:

```text
22-34  EASTNORTHEAST
64-74  BERLINCLOCK
```

That fixes 24 plaintext letters and leaves 73 undisclosed.

Sources: [2020 New York Times clue](https://www.nytimes.com/interactive/2020/01/29/climate/kryptos-sculpture-final-clue.html), [2014 WIRED clue](https://www.wired.com/2014/11/second-kryptos-clue/), [2025 Scientific American archival report](https://www.scientificamerican.com/article/a-solution-to-the-cias-kryptos-code-is-found-after-35-years/).

## K4 Method Evidence

### Additional Masking

Scheidt told *The New York Times* that K4 uses a **masking technique**, an additional obfuscating layer. This supports testing composed systems but does not identify one formal cipher named "masking." [New York Times, 2020](https://www.nytimes.com/interactive/2020/01/29/climate/kryptos-sculpture-final-clue.html)

Reasonable bounded interpretations include:

- substitution followed by transposition
- transposition followed by substitution
- nulls or extracted masks
- multiple alphabets or periodically switched streams
- split/interleaved streams
- visual or layout-derived position maps

### One-To-One Statistical Evidence

Richard Bean's peer-reviewed HistoCrypt 2021 paper used permutation tests and Monte Carlo sampling on public crib/cipher relationships. It reported strong evidence of an unusual positionwise one-to-one relationship and identified Gromark as a family capable of explaining many observed properties. Bean's companion repository reports 39 five-digit base-10 primer possibilities compatible with known blocks under flexible alphabet choices. This prioritizes a family; it is not a K4 solution. [Paper and DOI](https://doi.org/10.3384/ecp183153), [research repository](https://github.com/RichardBean/k4testing)

### Matrix Conjectures

The CIA says Sanborn combined its tableau with matrix coding systems in the first three passages. Bauer, Link, and Molle examined a matrix-encryption conjecture for K4 in *Cryptologia*. Matrix and Hill-family tests remain legitimate, but meaningful negative results must report dimension, modulus, alphabet map, block alignment, padding, and the searched space. [DOI](https://doi.org/10.1080/01611194.2016.1141556)

### Creator Constraints

The underlying system was designed around 1988-1990 by a visual artist working with an experienced cryptographer. High-priority mechanisms should be feasible with printed tables, grids, handwriting, simple calculators, and period cryptographic references. GPUs, SAT solvers, stochastic optimization, and language models can search a space today, but they should not be mistaken for the historical encryption mechanism.

## Public Clues And Their Evolution

### Berlin Clocks

In 2014 Sanborn told WIRED he was especially intrigued by Dieter Binninger's Berlin Clock, or Mengenlehreuhr, which displays time through groups of lamps. [WIRED, 2014](https://www.wired.com/2014/11/second-kryptos-clue/)

In a November 12, 2025 open letter and public event, Sanborn said `BERLINCLOCK` in the plaintext refers to the **World Clock in Berlin**. [Scientific American, 2025](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/)

These are dated creator statements, not a reason to erase the older lead. The World Clock now has the stronger direct semantic identification; the Mengenlehreuhr remains historically relevant to Sanborn's research and possible mechanics.

### August 2025 Point, Power, And Instruction Clues

In an August 14 open letter, Sanborn explicitly marked this sentence as a clue: **"what's the point? Power resides with a secret, not without it."** In the same letter he wrote, **"Even when K4 has been solved, its riddle will persist as K5."** [Sanborn open letter](https://elonka.com/kryptos/OpenLetterAug2025.html)

In a direct interview published the same day, WIRED reported that Sanborn had indicated K4's plaintext is an instruction for how to solve it and may involve parts of the installation beyond the copper screen. That is a reported functional constraint, not a released instruction or a position-fixed crib. [WIRED, 2025](https://www.wired.com/story/jim-sanborn-auctions-kryptos-key/)

The point/power wording permits several distinct readings: compass point, clock point, geographic point, punctuation, purpose, or secrecy itself. Those interpretations must be tagged and tested separately rather than collapsed into a claimed plaintext word.

### Final 2025 Clues

Sanborn's final public clues stated that:

- a trip he took to Egypt in **1986** figures in the solution
- the **1989 fall of the Berlin Wall** figures in the solution
- `BERLINCLOCK` means Berlin's **World Clock**
- the Kryptos codes concern **"delivering a message"**
- K5 is thematically connected to K2's "it's buried out there somewhere"
- anything Sanborn hypothetically left at the CIA site would have to be **"semi ephemeral, undetectable and carefully hidden"** because workers and the site were closely monitored

The hidden-site statement is conditional and does not establish that a recoverable object exists. Sanborn also described K5 as a separate future 97-character ciphertext with a system similar to K4, `BERLINCLOCK` at the same positions, and an intended home in a public space. K5 is intended to become solvable after K4, but its ciphertext has not been publicly released. [Sanborn's November 2025 letter](https://www.documentcloud.org/documents/26229389-adobe-scan-nov-12-2025/), [Scientific American, 2025](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/), [Paradigm, 2026](https://www.paradigm.xyz/writing/kryptos)

The November letter contains an unresolved chronology conflict: Sanborn said both events influenced plaintext he was writing in 1988, although the Berlin Wall fell in 1989. The project preserves that inconsistency rather than silently changing either date.

## 2025 Archive Discovery

- The Smithsonian finding aid describes **16.1 linear feet** of Jim Sanborn papers dating circa 1945-2024, donated in 2023 and 2026. [Finding aid](https://www.aaa.si.edu/collections/jim-sanborn-papers-22298)
- Its commission series lists Kryptos pre-production notes, code research, dedication material, attempted solutions, and "Cracked Codes and Charts." [Commission inventory](https://www.aaa.si.edu/collections/jim-sanborn-papers-22298/series-3)
- Reporting places Byrne's photography immediately before Kobek contacted Sanborn on September 3, 2025 with reconstructed plaintext; the exact photography date is part of the reported chronology rather than a Smithsonian record. The visible scraps contained known `BERLIN CLOCK` and `EAST NORTHEAST` phrases, strongly corroborating their relevance before Sanborn confirmed the complete reconstruction. [Scientific American](https://www.scientificamerican.com/article/a-solution-to-the-cias-kryptos-code-is-found-after-35-years/), [WIRED](https://www.wired.com/story/kryptos-code-reveal/)
- The researchers declined to release the text. Contemporary reporting and the auction listing said the relevant files were restricted for 50 years after Sanborn contacted the Smithsonian. The updated 2026 [collection access page](https://www.aaa.si.edu/collections/jim-sanborn-papers-22298/how-to-use) now describes the collection as open for research, while the [Kryptos inventory](https://www.aaa.si.edu/collections/jim-sanborn-papers-22298/series-3) offers appointment/reproduction controls. Neither page documents whether the sensitive plaintext scraps remain separately withheld, so their present access status is unresolved rather than confirmed as a continuing 50-year seal.
- RR Auction disclosed that it had not independently examined Sanborn's secret archive and relied on his representations about its contents. [Auction record](https://www.rrauction.com/auctions/lot-detail/350761607302001-the-complete-secrets-of-kryptos-jim-sanborns-private-archive/)

## Archive Sale And Current Stewardship

The RR Auction lot described:

- original handwritten K4 plaintext with a signed Scheidt letter
- original K4 coding system
- screen-cutting plaintext pieces
- original K1-K3 coding charts
- unpublished alternate 1988 K1 material
- an unpublished alternate K4 plaintext/chart now called K5
- scrambled texts shown during CIA review
- Sanborn's CIA badge, commission contract, dedication materials, photographs, and proof-of-concept copper plate

The lot closed November 20, 2025 at $962,500 including premium. [RR Auction](https://www.rrauction.com/auctions/lot-detail/350761607302001-the-complete-secrets-of-kryptos-jim-sanborns-private-archive/)

Paradigm's June 2026 statement says:

- it bought the archive and sees itself as steward of the secret
- no member of its team viewed the K4 plaintext during verifier setup
- the verifier compares a submitted plaintext through SHA-256 and a cloud-held HMAC mechanism
- submissions cost $1 to discourage brute force
- Paradigm also holds K5's 97-character ciphertext and plans a future release
- it launched ten separate Kryptos-style capture-the-flag puzzles to encourage tool development

[Paradigm's primary statement](https://www.paradigm.xyz/writing/kryptos)

These are current-owner representations. No independent technical audit was found establishing that no Paradigm team member saw the plaintext or that the retained verification value corresponds to Sanborn's confirmed text.

## High-Priority Research Program

1. Freeze transcription, indexing, punctuation, and crib positions.
2. Reproduce K1-K3 as exact known-answer controls.
3. Reproduce published crib statistics and one-to-one diagnostics with randomized controls.
4. Exhaust Gromark and tightly related running-digit families under declared alphabet constraints.
5. Exhaust Quagmire I-IV, Vigenere/Beaufort variants, and autokey systems under standard and Kryptos alphabets.
6. Compose one bounded masking/transposition layer in both orders.
7. Test K3-style and physical-layout routes as invertible position maps.
8. Treat World Clock mechanics, Mengenlehreuhr mechanics, directions, K2 coordinates, tableau material, and `XLAYERTWO` as separate tagged hypotheses.
9. Use one crib block to choose parameters and the other as a holdout.
10. Require complete output, independent reproduction, and verifier success before claiming a solution.

The dashboard's master registry expands this program into more than 90 individually trackable techniques.

## Common Failure Modes

- moving a crib or mixing local and global indices
- fitting all 24 public letters with a custom alphabet and no holdout
- reporting only attractive words instead of all 97 output letters
- searching an unreported number of keys or routes
- calling a high language-model score a decryption
- treating one failed key as rejection of an entire cipher family
- inventing ciphertext or positional constraints for unreleased K5
- treating every sculpture feature as a key simultaneously
- calling archival possession a cryptanalytic derivation
- calling any plausible anonymous online plaintext a solution without a method and verifier result

## Source Conflicts And Cautions

- **Dedication:** CIA's exact institutional date is November 3, 1990. A 1999 *New York Times* article says October 1990. Prefer CIA for the exact date.
- **Artwork year:** 1988 copyright/conception, 1989 catalog date, and 1990 installation/dedication can all be true.
- **Webster's envelope:** 1999 reporting said the complete answer had been given to William Webster. Sanborn said in 2005 that he definitely did not give Webster the final section. Prefer the later direct creator statement while acknowledging deliberate deception is part of Sanborn's account.
- **"Solved":** ordinary-language headlines call the recovered plaintext a solution. Cryptanalytic usage requires a derivation. Always state which meaning is intended.
- **K4 length:** one 2025 article refers once to 79 letters, apparently confusing Sanborn's age with the cipher length; the same article later says 97. Physical transcription, CIA, Paradigm, and the entire research record establish 97.
- **Buried object:** K2's wording and Sanborn's ambiguity do not establish that a recoverable cache exists at the coordinates.
- **1988/1989 chronology:** Sanborn's November 2025 letter says the 1989 fall of the Berlin Wall influenced plaintext he was writing in 1988. Preserve the conflict as stated.
- **Morse text:** no institutionally settled complete K0 transcription was found.

## Related Sanborn Works

Sanborn's broader practice matters because he explicitly advised cryptanalysts to gather information about it and described visual systems as part of Kryptos.

- *Invisible Forces* (1985): lodestone, compasses, sandstone, light
- *Thunderhead Horizon* (1985): sandstone, lodestone, shadow
- *Coriolis* (1985-1992): sandstone, specimens, whirlpool, light
- *Covert Obsolescence* works (1991-1993): copper screens, projected material, pulped CIA documents
- *Cyrillic Projector*: encoded Cyrillic material later decrypted as KGB text
- *Antipodes* (1997): copper, encoded text, petrified tree
- projection works using text, shadows, light, landscape, and directional geometry

Primary catalog: [Jim Sanborn official site](https://www.jimsanborn.net/main.html). These works support bounded hypotheses about direction, light, shadow, magnetism, water, and visual layout; they do not provide a known K4 key.

## Copyright, Ethics, And Verification

- Kryptos remains a copyrighted artwork. Sculpture and archive photographs should not be redistributed without permission.
- This project stores factual transcriptions necessary for cryptographic testing but does not bundle copyrighted imagery.
- Do not scrape, automate around, or attempt to bypass Paradigm's paid verifier.
- Do not solicit or publish archival plaintext obtained through unauthorized access.
- Independently deriving the method and plaintext is stronger evidence than possession of leaked text.

## Core Sources

All links were checked during research ending 2026-07-27.

### Primary And Institutional

- [CIA: Kryptos history, installation and canonical transcription](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/)
- [CIA Reading Room: David Stein, "Cracking the Courtyard Crypto"](https://www.cia.gov/readingroom/document/06712772)
- [CIA institutional FOIA record](https://www.cia.gov/readingroom/document/06498615)
- [Smithsonian: Jim Sanborn papers finding aid](https://www.aaa.si.edu/collections/jim-sanborn-papers-22298)
- [Smithsonian: Kryptos commission files](https://www.aaa.si.edu/collections/jim-sanborn-papers-22298/series-3)
- [Smithsonian oral history with Jim Sanborn](https://www.aaa.si.edu/collections/interviews/oral-history-interview-jim-sanborn-15700)
- [Jim Sanborn official catalog and statement](https://www.jimsanborn.net/main.html)
- [Sanborn's 2005 WIRED interview](https://www.wired.com/2005/01/questions-for-kryptos-creator/)
- [Sanborn's August 2025 open letter](https://elonka.com/kryptos/OpenLetterAug2025.html)
- [Sanborn's November 2025 open letter](https://www.documentcloud.org/documents/26229389-adobe-scan-nov-12-2025/)
- [RR Auction archive lot and sale result](https://www.rrauction.com/auctions/lot-detail/350761607302001-the-complete-secrets-of-kryptos-jim-sanborns-private-archive/)
- [Paradigm stewardship and verification statement](https://www.paradigm.xyz/writing/kryptos)
- [Paradigm indexed K4](https://paradigm.xyz/kryptos/)

### Academic

- Richard Bean, ["Cryptodiagnosis of 'Kryptos K4'"](https://doi.org/10.3384/ecp183153), HistoCrypt 2021, CC BY 4.0
- Bauer, Link, and Molle, ["James Sanborn's Kryptos and the matrix encryption conjecture"](https://doi.org/10.1080/01611194.2016.1141556), *Cryptologia* 40(6), 2016

### Historical And Contemporary Reporting

- [1999 New York Times public-solution report](https://archive.nytimes.com/www.nytimes.com/library/tech/99/06/biztech/articles/16code.html)
- [WIRED analysis of NSA FOIA records](https://www.wired.com/2013/07/nsa-cracked-kryptos-before-cia/)
- [NPR 2010 clue interview](https://www.npr.org/2010/11/22/131520768/-kryptos-sculptor-drops-new-clue-in-20-year-mystery)
- [WIRED 2014 CLOCK clue and Mengenlehreuhr discussion](https://www.wired.com/2014/11/second-kryptos-clue/)
- [New York Times 2020 NORTHEAST clue and masking statement](https://www.nytimes.com/interactive/2020/01/29/climate/kryptos-sculpture-final-clue.html)
- [WIRED August 2025 auction interview and K4 instruction report](https://www.wired.com/story/jim-sanborn-auctions-kryptos-key/)
- [Scientific American 2025 archival discovery](https://www.scientificamerican.com/article/a-solution-to-the-cias-kryptos-code-is-found-after-35-years/)
- [WIRED 2025 participant account](https://www.wired.com/story/kryptos-code-reveal/)
- [Scientific American 2025 final creator clues](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/)

### Technical Community Records

- [Elonka Dunin's Kryptos archive](https://www.elonka.com/kryptos/)
- [Detailed K2 correction announcement](https://www.elonka.com/kryptos/CorrectedK2Announcement.html)
- [K3 visual reverse reconstruction](https://www.elonka.com/kryptos/part3.html)
- [Richard Bean's K4 research code](https://github.com/RichardBean/k4testing), GPL-3.0
- [Auditable K1-K3 TypeScript reference](https://github.com/isaaclyman/kryptos-typescript)

Community pages are invaluable for reproducibility and history but are kept below direct creator, institutional, and peer-reviewed evidence when claims conflict.
