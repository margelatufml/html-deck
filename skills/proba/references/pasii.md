# Cei cinci pași, cu criterii de trecere

Fiecare pas are: întrebarea pe care o pune, întrebările de sondare când răspunsul e vag, **criteriul de
trecere** (verificabil, nu declarativ) și **artefactul** pe care îl produce.

Nu treci mai departe fără artefact. Un pas fără artefact nu s-a întâmplat.

---

## P — Problema
**Din POLC: Planning** · ~20 min din 48h · *„Pe cine ajut și ce îl doare?”*

### Întrebarea de deschidere
„Spune-mi ideea în maximum două propoziții, oricât de brută e.”

Apoi, indiferent ce spun, mergi la șablon.

### Șablonul
```
[CINE] nu poate [SĂ FACĂ CE]
pentru că [OBSTACOL],
și acum îl costă [CE ANUME].
```

### Întrebări de sondare, când răspunsul e vag
- „Cine, concret? Vârstă, context, ce face azi în loc.” — dacă răspunde „toată lumea” sau „studenții”, încă nu are un om.
- „Ce face omul ăsta **azi**, când dă de problemă?” — dacă nu știe, problema poate să nu existe.
- „Cât îl costă? Timp, bani, nervi, oportunitate ratată.” — fără cost, e o observație, nu o problemă.
- „De ce acum? De ce nu s-a rezolvat până acum?”

### Criteriul de trecere
O singură propoziție care conține **toate trei**:
1. un grup de oameni pe care îl poți numi și descrie în zece cuvinte,
2. o acțiune concretă pe care nu o pot face,
3. un cost măsurabil sau cel puțin numibil.

Dacă lipsește oricare, nu treci. Spune care lipsește.

### Cuvinte care opresc pasul
`platformă` · `ecosistem` · `soluție` · `toată lumea` · `ar fi mișto` · `oamenii au nevoie de`

Fiecare înseamnă că a sărit la răspuns fără să aibă întrebarea. Numește cuvântul și cere concretul.

### Artefactul
Propoziția problemei, scrisă. Se pune pe masă, fizic. Când echipa se ceartă în ora 30, foaia aia decide.

---

## R — Research
**Pasul pe care POLC nu îl are** · ~2 ore · *„E reală și încape în 48h?”*

Detaliile complete: `research-2ore.md`. Rezumat aici.

### Cele patru întrebări
1. **Există problema?** — minimum 3 urme independente (postări, forumuri, întrebări reale, articole).
2. **Cine o are, concret?** — un grup numit și ce face azi în loc.
3. **Există deja o soluție?** — aproape sigur da. Întrebarea reală: *de ce nu o folosesc oamenii tăi?*
4. **Poți arăta ceva în 48h?** — care e cea mai mică felie care demonstrează ideea?

### Regula de onestitate, spusă cu voce tare
Tu, ca model, **poți inventa surse care sună perfect**. Spune-le asta. Apoi cere-le:
- să deschidă fiecare link — chiar să-l deschidă;
- să verifice că fiecare cifră are **an** și **autor**;
- să pună aceeași întrebare invers („de ce e o idee proastă?”) și să compare răspunsurile.

### Criteriul de trecere
- 3 urme independente că problema există, cu linkuri care chiar se deschid;
- 1 utilizator numit;
- 3 alternative existente, cu motivul pentru care nu sunt folosite;
- 1 decizie scrisă: **mergem / schimbăm / tăiem**.

### Semnalul de STOP
| Ce vezi | Ce faci |
|---|---|
| Zero urme că problema există | Schimbi **problema**, nu soluția |
| Există deja, gratis, bine făcut | Schimbi unghiul: alt utilizator, alt context, altă felie |
| Nu încape în 48h nici tăiat la os | Tai până la o singură funcție demonstrabilă |

Spune-le direct: în ora 2, schimbarea e gratis. În ora 30, costă tot hackathonul.

### Artefactul
Tabelul de concurență (3 rânduri) plus decizia scrisă într-o propoziție.

---

## O — Organizare
**Din POLC: Organizing** · ~1 oră · *„Cine decide ce, și ce tăiem?”*

### Bugetul, nu maratonul
48 de ore nu sunt 48 de ore de lucru. Două nopți × ~5h de somn = ~10h care nu sunt ale echipei.
**Bugetul real e ~38h.** Echipele care „nu dorm” livrează în ora 44 cod pe care nu îl pot demonstra.

### Rolurile — patru oameni, și doi nu scriu cod principal
| Rol | Deține | Decide |
|---|---|---|
| **Product** | problema și felia | ce **nu** intră; singurul care vorbește cu mentorii |
| **Build 1 (core)** | funcția care demonstrează ideea | nimic altceva |
| **Build 2 (shell)** | ecranul, datele false, deploy-ul | începe cu demo-ul |
| **Story** | pitch-ul, slide-urile, înregistrarea demo-ului | începe în ora 4, nu în ora 44 |

Dacă sunt trei: dispare **Build 2**, nu Story. Un produs nedemonstrat nu există.

### Scope: demo, MVP sau produs — alegi unul
- **Demo** — o cale, date pregătite, merge pe laptopul tău. ✅ fezabil în 48h
- **MVP** — mai multe căi, date reale, alții îl pot folosi. ⚠ rar fezabil
- **Produs** — conturi, plăți, erori tratate, scalare. ❌ nu în 48h

**Taie primul, fără discuție:** autentificare · roluri și permisiuni · setări · dark mode · responsive pe
telefon · bază de date reală (folosește un fișier) · tratarea erorilor pe căile pe care nu le demonstrezi.

### Criteriul de trecere
Fiecare om știe ce deține și ce decide singur; lista „ce nu construim” e scrisă și are minimum 5 rânduri.

### Artefactul
Tabelul de roluri plus lista „ce NU construim”.

---

## B — Build
**Din POLC: Leading** · restul timpului · *„Ce arătăm, și în ce ordine îl construim?”*

### Demo-first
Ordinea de construcție, nu ordinea logică:
```
Ecranul final (date false) → calea care îl umple → funcția reală în spate → restul, dacă mai e timp
```
Dacă rămâi fără timp la pasul 3, **tot ai un demo**. Dacă începi cu backend-ul și rămâi fără timp, nu ai
nimic de arătat.

### Patru decizii care mănâncă un hackathon
| Decizia | Cât te costă* | Ce faci în loc |
|---|---|---|
| Autentificare reală | 4–8h | un utilizator hardcodat, buton „Intră ca Ana” |
| Bază de date + migrări | 3–6h | un fișier JSON, sau date în memorie |
| Deploy în cloud | 2–5h + stres | rulezi local, înregistrezi demo-ul ca backup |
| Stack nou „ca să învățăm” | imprevizibil | stack-ul știut deja de cel mai lent din echipă |

\* estimări orientative, din experiență, nu măsurători.

Fiecare dintre astea e o decizie de produs deghizată în decizie tehnică.

### AI la build — ce delegi și ce nu
**Deleagă fără frică:** boilerplate, configurări, date false realiste, transformări între formate, regex,
CSS, traducerea unui exemplu între limbaje, explicarea unei erori.

**Nu delega:** alegerea feliei care se demonstrează, ce tai din scope, arhitectura pe care o vei apăra în
Q&A, ce spui în pitch.

Capcana: **codul care merge dar pe care nu îl înțelegi.** Juriul întreabă „de ce ai făcut așa?”. Dacă
răspunsul e „așa a generat”, ai pierdut. *Poți livra cod pe care nu l-ai scris; nu poți apăra cod pe care
nu l-ai citit.*

### Checkpoint-uri — o întrebare, un răspuns da/nu, o acțiune dacă e nu
| Ora | Întrebarea | Dacă nu |
|---|---|---|
| **12** | Avem ecranul final, chiar și cu date false? | oprește tot, fă-l acum |
| **24** | Funcția care demonstrează ideea merge o dată, pe o cale? | taie o funcție |
| **36** | — | **îngheață scope-ul. Nimic nou după ora 36.** |
| **44** | Putem face demo-ul de la zero, pe alt laptop, fără să ne rugăm? | înregistrează-l acum |

### Criteriul de trecere
Există o cale completă, de la ecran la rezultat, care merge de la capăt la capăt fără intervenție.

### Artefactul
Demo-ul care rulează, plus înregistrarea lui.

---

## A — Arată și Ajustează
**Din POLC: Controlling** · ~4 ore · *„Merge de 3 ori la rând, în fața altcuiva?”*

### Ce măsori, ce arăți, ce ajustezi
- **Măsori:** merge calea? de câte ori din 5?
- **Arăți:** o cale, până la capăt, fără scuze verbale.
- **Ajustezi:** ce a picat la repetiție — nu ce ai fi vrut să adaugi.

**Repetă demo-ul de trei ori** înainte. A treia oară cronometrat. Prima repetiție găsește întotdeauna ceva.

### Pitch-ul de 3 minute
| Timp | Ce |
|---|---|
| `0:00–0:30` | **Omul și durerea.** Un nume, o situație. Fără „în ziua de azi”. |
| `0:30–1:00` | **De ce nu merge azi.** Ce face omul acum în loc, și de ce e prost. |
| `1:00–2:00` | **Demo.** Live, o cale. **Taci și arată.** |
| `2:00–2:30` | **Cum e construit.** O propoziție tehnică pe care o poți apăra. |
| `2:30–3:00` | **Ce urmează.** Ce ai tăia, ce ai adăuga, ce ai măsura. |

Nu începe cu echipa, cu tehnologiile sau cu „ne-am gândit că”. Începe cu omul.

### Cele cinci întrebări ale juriului
| Întrebarea | Răspunsul prost | Răspunsul bun |
|---|---|---|
| Cine e utilizatorul? | „Oricine” | grupul concret din pasul P |
| Există deja asta? | „Nu” | „Da, X și Y. Noi diferim prin Z, pentru W.” |
| Cât e făcut de AI? | defensivă | „Boilerplate-ul. Deciziile sunt ale noastre, uite care.” |
| Ce nu merge? | „Totul merge” | două limite concrete, numite fără ezitare |
| Ce faci mai departe? | listă de funcții | ce ai **măsura** prima dată cu utilizatori reali |

„Nu știu, dar uite cum aș afla” este un răspuns bun. „Totul merge” nu este niciodată.

### Criteriul de trecere
Demo-ul a rulat de trei ori la rând, în fața cuiva din afara echipei, fără intervenție.

### Artefactul
Pitch-ul repetat și cronometrat, plus înregistrarea demo-ului ca plasă de siguranță.
