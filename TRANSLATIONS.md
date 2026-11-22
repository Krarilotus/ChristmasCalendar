# Translation Notes — A Crusader's Christmas (Wave 1: Doors 01–21)

> **Important:** All seven target languages (`fr`, `ru`, `hu`, `tr`, `ch`, `es`, `fa`) in this folder are **machine translations** generated from the English (`DoorNN_en.html`) and German (`DoorNN_de.html`) originals and **require review by native speakers** before final release.

> **Also needing native review:** the plugin's option and door-page texts (`plugin/locale/<lang>.yml`) and descriptions (`plugin/locale/description-<lang>.md`) in fr, ru, hu, tr, ch, es and fa. They were translated by Claude Opus 5.5 from the English texts while the Neon translator was out of quota. Menu names are given translated with the English name in brackets, because each language edition's exact wording wasn't checked.

---

## General Notes & Cross-Language Conventions
- **HTML parity:** Every translated file preserves the exact tag sequence, nesting (`<strong><span ...>` vs `<span ...><strong>`), `<br />` placement, `<details>/<summary>`, and color hex/named values of `DoorNN_en.html`.
- **Encoding:** UTF-8 without BOM; plain UTF-8 characters throughout (only `&gt;` retained in `Door03` for the `-&gt;` progression arrows).
- **EN vs DE differences handled:**
  - `Door06` & `Door08`: English writes "Father Christmas day" for December 6, whereas German writes "Sankt Nikolaustag" (Dec 6 is St. Nicholas Day in Germany). Translated as St. Nicholas Day / Saint-Nicolas / Mikulás napja / День святого Николая / Aziz Nikola Günü / 圣尼古拉节 / día de San Nicolás / روز سنت نیکلاس to fit Door 06 accurately; native reviewers may adjust if a more generic Christmas wording is preferred.
  - `Door11`: `Door11_de.html` accidentally puts the closing `<p>` inside the last `<details>` tag; all translations follow `Door11_en.html`, where it is properly outside `<details>`.
  - `Door15`: `Door15_de.html` names the headquarters `Hauptquartier Waheeb` with an extra colored span; translations follow `Door15_en.html` ("headquarters, represented by the light blue pieces...") to preserve exact EN HTML tag parity.
  - `Door20`: `Door20_en.html` has no colored `<span>` tags in paragraph 2 (unlike `Door20_de.html`); translations follow `Door20_en.html` for exact tag parity.

---

## Per-Language Uncertain Terms & Lord Names for Native Review

### French (`fr`)
- **Lord names used:** le Rat, le Serpent, le Porc, le Loup, Saladin, le Calife, le Sultan (Sultan Abdul), Richard, Frédéric, Philippe, le Vizir, l'Émir, Nizar, le Shérif, l'Abbé.
- **Nicknames & flavor terms to review:**
  - `Door05`: `Duc Truffe` (kept), `le Duc de Pigsbury`, `« Le Verrat »` ("The Hog").
  - `Door08`: `Vizir « Le Fléau »` ("The Scourge"), `Vizir « Le Terrible »` ("The Terrible"), `montagnes de joie` / `montagne de tourment`.
  - `Door15`: `Richard « Le Désespéré »`, `la Terre de Production` ("Land of Production").
  - `Door21`: `ordre « attaquer ici »` ("attack-here").
- **Register:** Uses informal `tu` throughout to match the author's playful voice (with mock-formal `Monseigneur, vous voulez…` in `Door14` line 2 matching EN/DE). Native reviewers should confirm tone consistency.

### Russian (`ru`)
- **Lord names used:** Крыса, Змея, Кабан (official Buka/1C SHC name for The Pig), Волк, Саладин, Калиф (classic Buka SHC spelling; some players use Халиф), Султан (Султан Абдул), Ричард, Фридрих, Филипп, Визирь, Эмир, Низар, Шериф, Аббат.
- **Nicknames & terms to review:**
  - `Door05`: `Дюк Трюфф`, `Герцог Пигсбери`, `«Хряк»`.
  - `Door08`: `Визирь «Бич»`, `Визирь «Грозный»`.
  - `Door15`: `Ричард «Отчаянный»`, `Земля Производства`.
  - `Door13` Hint 1: `бойницы` ("arrow slits") — verify against Russian SHC UI term.
  - `Door19`/`Door20`/`Door21`: gamer loanword `раш` / `рашить` ("rush") used idiomatically; native reviewers may prefer `быстрый штурм` / `ранняя атака`.
  - `Door21` Hint 20: `«Атаковать здесь»` ("attack-here") — verify against Russian SHC UI wording.
  - Sign-off: `от Krarilotus` (alternative: `автор: Krarilotus`).

### Hungarian (`hu`)
- **Lord names used:** Patkány, Kígyó, Disznó (some Hungarian SHC players use `Malac` or `Sertés`—please verify official Hungarian localization), Farkas, Szaladin, Kalifa, Szultán (Abdul szultán), Richárd, Frigyes, Fülöp, Vezír (note `extension-ucp2-legacy/locale/hu.yml` uses `Wazir` once; `Vezír` is proper Hungarian), Emír, Nizar, Seriff, Apát.
- **Nicknames & terms to review:**
  - `Door05`: `Duc Truffe`, `Pigsbury hercege`, `„A Kan”` ("The Hog").
  - `Door08`: `Vezír, „Az Ostor”`, `Vezír, „A Rettenetes”`.
  - `Door15`: `„A Kétségbeesett” Richárd`, `a Termelés Földje`.
  - `Door01`–`Door21`: `ajtó` used for calendar "door" (alternative: `ablak` for Advent calendar windows; `ajtó` fits hinges/curtains/prying open).
  - `Door07`/`Door11`: `csapdaverem` ("killing pits") — verify against Hungarian SHC UI (`ölőverem` / `gyilkos verem`).
  - `Door21` Hint 20: `„támadás itt”` ("attack-here") — verify exact Hungarian SHC UI command.

### Turkish (`tr`)
- **Lord names used:** Fare (some Turkish players use `Sıçan`), Yılan, Domuz, Kurt, Selahaddin, Halife, Sultan (Sultan Abdül), Richard, Frederick, Phillip (kept European spellings; native reviewers may prefer `Frederik` / `Filip`), Vezir, Emir, Nizar, Şerif, Başrahip.
- **Nicknames & terms to review:**
  - `Door05`: `Duc Truffe`, `Pigsbury Dükü`, `"Azılı Domuz"` ("The Hog").
  - `Door08`: `Vezir "Kırbaç"`, `Vezir "Korkunç"`.
  - `Door15`: `"Çaresiz" Richard`, `Üretim Diyarı`.
  - `Door07`/`Door11`: `ölüm çukurları` ("killing pits") and `eczacı` ("apothecary") — verify against Turkish SHC community patch terminology.
  - `Door19`/`Door20`/`Door21`: `erken baskın` / `erken saldırı` used for "rush".
  - `Door21` Hint 20: `"buraya saldır"` ("attack-here").

### Simplified Chinese (`ch`)
- **Lord names used:** 老鼠, 蛇 (some players say `毒蛇`), 猪 (some players say `野猪`), 狼 (some players say `恶狼`), 萨拉丁, 哈里发, 苏丹 (苏丹阿卜杜勒), 理查 (`Chinese.yml` uses `狮心王` in one place; `理查` was chosen to pair cleanly with nicknames like `“绝望者”理查`), 腓特烈 (`Chinese.yml` uses `皇帝` in one place; `腓特烈` matches `Frederick`), 菲利普, 维奇尔, 埃米尔, 尼扎尔, 治安官 (some players say `警长`), 修道院长.
- **Nicknames & terms to review:**
  - `Door05`: `特吕夫公爵（Duc Truffe）`, `猪堡公爵`, `“大野猪”`.
  - `Door08`: `维奇尔“天灾”`, `维奇尔“恐怖者”`.
  - `Door15`: `“绝望者”理查`, `“生产之地”`.
  - `Door06`: `麦酒` ("ale") — verify whether SHC Chinese players prefer `啤酒` or `麦酒`.
  - `Door07`/`Door11`: `陷阱坑` ("killing pits") — some Chinese SHC patches use `陷坑` or `尖刺陷阱`.
  - `Door15`/`Door17`/`Door19`/`Door20`: `药剂师` ("apothecary") — verify against Chinese SHC building name (`药房`/`药剂师`).
  - `Door21` Hint 20: `“攻击此处”` ("attack-here").

### Spanish (`es`)
- **Lord names used:** la Rata, la Serpiente, el Cerdo, el Lobo, Saladino, el Califa, el Sultán (Sultán Abdul), Ricardo, Federico, Felipe, el Visir, el Emir, Nizar, el Sheriff (alternative: `el Alguacil`), el Abad.
- **Nicknames & terms to review:**
  - `Door05`: `Duc Truffe`, `el Duque de Pigsbury`, `«El Jabalí»` ("The Hog").
  - `Door08`: `Visir «El Azote»`, `Visir «El Terrible»`.
  - `Door15`: `Ricardo «El Desesperado»`, `la Tierra de la Producción`.
  - `Door07`/`Door11`: `fosos mortales` ("killing pits") — verify against FX Interactive Spanish SHC (`pozos mortales` / `fosos con estacas`).
  - `Door13` Hint 1: `aspilleras` ("arrow slits").
  - `Door21` Hint 20: `«atacar aquí»` ("attack-here").

### Persian (`fa`)
- **Lord names used:** موش, مار, خوک, گرگ, صلاح‌الدین, خلیفه, سلطان (سلطان عبدل), ریچارد, فردریک, فیلیپ, وزیر, امیر, نزار, کلانتر (iconic Persian SHC dub name for Sheriff; alternative: `شریف`), راهب بزرگ (natural match for `راهبان` = monks; some players use `ابوت`).
- **Nicknames & terms to review:**
  - `Door05`: `دوک تروف (Duc Truffe)`, `دوک پیگزبری`, `«گراز»`.
  - `Door08`: `وزیر «بلا»` ("The Scourge"; alternative: `«تازیانه»`), `وزیر «مهیب»` ("The Terrible").
  - `Door15`: `ریچارد «ناامید»`, `سرزمین تولید`.
  - `Door06`/`Door08`/`Door13`/`Door16`: "ale" translated as `نوشیدنی` and "inn" as `میخانه` (common in Persian SHC dubs; native reviewers may prefer `آبجو` / `مسافرخانه` or `کاروانسرا`).
  - `Door15`/`Door17`/`Door19`/`Door20`: `عطاری` ("apothecary"; alternative: `داروخانه` / `داروساز`).
  - `Door21` Hint 20: `«حمله به اینجا»` ("attack-here").
  - Uses polite-conversational `شما` throughout, standard Persian `ی`/`ک`, ZWNJ where appropriate, and no `dir` attributes.

---

## Source Typos & Unclear Phrasing Found (English & German)

| File | Original text | Issue / Intended meaning |
|---|---|---|
| `Door01_en.html` (line 22) | `Its time to head into battle.` | Missing apostrophe: `It's time to head into battle.` |
| `Door02_en.html` (line 1) | `Behind the curtains of the second door lies and invitation` | Typo `and` → `an` (`lies an invitation`). |
| `Door02_en.html` (line 2) | `Now its your turn to clean it up!` | Missing apostrophe: `it's`. |
| `Door02_en.html` (line 10) | `The farmland has more space then you might think.` | `then` → `than`. |
| `Door02_en.html` (line 14) | `Your enemies units seem to suffer` | Missing possessive apostrophe: `Your enemies' units`. |
| `Door02_de.html` (line 2, 10), `Door05_de.html` (line 14), `Door06_de.html` (line 15) | `Schlammassel`, `Brotuktion` | Typos for `Schlamassel` and `Brotproduktion`. |
| `Door03_en.html` (line 1) | `couldn’t resist to open the third door` | Non-idiomatic infinitive; translated as "couldn't resist opening". |
| `Door04_en.html` (lines 2–3) | `a concurrent thread of assassins` / `Emir, the other thread` | Typo `thread` → `threat` (confirmed by DE `Bedrohung`). Also `straight forward` → `straightforward`. |
| `Door04_en.html` (line 4) | `As this might be your first map to attempt at least twice. I can shorten your time spent, if you are out of ideas with these useful insights:` | Period splits a single sentence; translated as one coherent sentence. |
| `Door05_en.html` (lines 10, 18) | `at all time`, `wont`, `Fredericks castle` | Missing `s`/apostrophes: `at all times`, `won't`, `Frederick's castle`. |
| `Door06_en.html` (lines 1, 2, 4, 9, 17, 23, 29, 39, 42) | `wont`, `continuate`, `i collected`, `loose your access`, `the Rats castle`, `layed out`, `Wolfs gates`, `crossbowman`, `You should better be ready!`, `where got to know` | Typos/grammar for `won't`, `continue`, `I collected`, `lose your access`, `the Rat's castle`, `laid out`, `Wolf's gates`, `crossbowmen`, `You had better be ready!`, `where you got to know`. Also `Door06_de.html` line 1 has `Sankt Nikaolaustag` → `Sankt Nikolaustag`. |
| `Door07_en.html` (lines 1, 2, 7, 25) | `a deep and though through mission`, `perimiter`, `havily`, `monsterous`, `ofthem`, `try to stockpile` (lowercase after `.`) | Typos for `thought-through`, `perimeter`, `heavily`, `monstrous`, `of them`, `Try to stockpile`. Also `Door07_de.html` line 17 mentions `Kalif und Nizar` while `Door07_en.html` says `enemies` generically. |
| `Door08_en.html` (lines 15, 53, 55) | `better of`, `Wazirs castles`, `which Wazir i easier` | Typos for `better off`, `Wazirs' castles`, `which Wazir is easier`. |
| `Door09_en.html` (lines 1, 8) | `complete the objective to to leave`, `so abbot attacks you` | Duplicate word `to to`; lowercase `abbot`. |
| `Door10_en.html` (line 1) | `Richard, who’s huge castle` | `who's` → `whose`. |
| `Door11_en.html` (line 8) | `Remember Door4?` | Missing space (`Door 4`). Also `Door11_de.html` lines 20–22 misplace closing `<p>` inside `<details>`. |
| `Door15_en.html` (lines 2, 4, 24) | `Door8`, `engineer’s guild`, `A trebuchet and catapult line shoot` | Missing space (`Door 8`); singular possessive; slightly awkward subject-verb agreement (clarified via DE: "a trebuchet and a line of catapults fire from Richard's side"). |
