# Repo zajęć (VPS + Bash + Python + Markdown + Git)

To repo jest wspólnym dziennikiem oraz zbiorem ćwiczeń z praktyk zawodowych **pz2026** realizowanych w obszarze Linuksa na VPS. Celem praktyk jest poznanie podstaw pracy w środowisku deweloperskim opartym o system Linux: od poruszania się po systemie i pracy z terminalem, przez zdalny dostęp i sieć, aż po automatyzację, dokumentację i pracę z Gitem.

## Zakres

- Linux (terminal, pliki, uprawnienia, procesy, usługi)
- Markdown (notatki i instrukcje)
- Git (współpraca i wersjonowanie)
- SSH i praca zdalna
- Bash / Python (automatyzacja)
- Sieć w praktyce (diagnostyka, porty, firewall)

## Dodatkowo

- Moduły opcjonalne (w zależności od czasu i potrzeb)
- Projekt końcowy: wdrożone na VPS rozwiązanie + dokumentacja + demo

## Szybki start

### 1. Wymagania

- VSCode
- Git
- Dostęp do VPS (konto + klucz SSH)
- Klucz SSH do GitHuba (osobny od VPS)

### 2. VSCode

Zajrzyj do [docs/vscode.md](docs/vscode.md).

## Jak korzystamy z repo

### Każdy dzień zajęć = 3 rzeczy

1. **Wpis do dziennika** - `journal/YYYY-MM-DD.md`
2. **Kod / pliki z ćwiczeń** - `labs/...`
3. **Commit + push** na koniec zajęć

Przykład commit message:

- `journal: 2026-02-16`
- `lab: users and perms`
- `fix: bash script quoting`

Więcej w [CONTRIBUTING.md](CONTRIBUTING.md)

## Struktura katalogów

```bash
├── .vscode/
│   ├── extensions.md
│   └── settings.md
├── docs/
│   ├── faq.md
│   ├── markdown.md
│   ├── ssh.md
│   └── vscode.md
├── journal/
│   ├── _template.md
│   └── 2026-02-16.md
├── labs/
│   ├── 01-shell/
│   │   ├── README.md
│   │   └── solutions/
│   │       ├── jakub/
│   │       ├── maciej/
│   │       ├── natalia/
│   │       └── team/
│   ├── .../
├── scripts/
├── snippets/
│   ├── bash/
│   └── python/
├── .editorconfig
├── CONTRIBUTING.md
├── README.md
```

**Zasada prosta:**

- `docs/` = dłuższe opisy / materiały
- `journal/` = notatki z dnia (co robiliśmy, komendy, wnioski)
- `labs/` = ćwiczenia i rozwiązania (konkretne zadania)
- `snippets/` = krótkie, przydatne kawałki (ściągi, one-linery)

## Dziennik zajęć (journal)

### Tworzenie wpisu na dany dzień

Skopiuj szablon:

```bash
cp journal/_template.md journal/$(date +%F).md
```

Uzupełnij i dodaj do commita.

## Praca z labami (labs)

**Gdzie wrzucać swoje pliki?**

Każdy lab ma:

- `labs/<nr-temat>/README.md` - treść ćwiczeń
- `labs/<nr-temat>/solutions/<nick>/...` - Twoje rozwiązania

Przykład:

- `labs/01-shell/solutions/natalia/notes.md`
- `labs/01-shell/solutions/natalia/task1.sh`

Jeśli robimy coś wspólnie jako grupa, wrzucamy do solutions/team/.

## Git: podstawowe komendy (koniec zajęć)

Orientacyjny skrót:

- fetch/pull (lepiej mieć to w nawyku)
- status
- add
- commit
- push

## Ustawienia VSCode i spójny styl w repo

### Wtyczki i ustawienia

Repo zawiera:

- `.vscode/extensions.json` - VSCode podpowie instalację właściwych rozszerzeń.

### Styl plików

Repo zawiera `.editorconfig`, żeby:

- wszyscy mieli te same wcięcia i końcówki linii
- nie było "czemu u mnie działa, a u ciebie nie" przez whitespace

## Zasady bezpieczeństwa (VPS)

- Logujemy się tylko SSH kluczami
- Nie wrzucamy do repo żadnych sekretów: haseł, tokenów, prywatnych kluczy, plików .env
- Jeśli coś wygląda jak sekret -> nie commituj, tylko zgłoś prowadzącemu

## Licencja / prawa autorskie

**Code** (e.g. `journal/`, `lab/`, configuration files intended as code) is licensed under **MIT**.
**Documentation** and educational materials (e.g. `docs/`, `README.md`) are licensed under **CC BY 4.0**.
