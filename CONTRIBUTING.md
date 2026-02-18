# CONTRIBUTING (zasady pracy w repo)

## Gdzie wrzucać i co?

- Notatki z dnia: `journal/YYYY-MM-DD.md`
- Rozwiązania zadań: `labs/<lab>/solutions/<nick>/...`
- Krótkie przydatne kawałki: `snippets/`
- Dłuższe materiały: `docs/`

## File namse

- Daty zawsze w formacie: `YYYY-MM-DD`
- Skrypty bash: `*.sh`
- Skrypty python: `*.py`
- Notatki: `*.md`

## Commit messages

Commit ma krótko mówić **co** i (czasem) **po co**. Używamy formatu:

`<kategoria>: <opis>`

### Kategorie

| Kategoria   | Typ                                             |
| ----------- | ----------------------------------------------- |
| `feature:`  | nowa funkcjonalność                             |
| `fix:`      | poprawka błędu                                  |
| `refactor:` | porządki w kodzie bez zmiany działania          |
| `chore:`    | utrzymanie/konfiguracje/narzędzia/formatowanie  |
| `docs:`     | dokumentacja (README, CONTRIBUTING, instrukcje) |
| `lab:`      | rozwiązanie zadania / ćwiczenia laboratoryjnego |
| `journal:`  | wpisy do dziennika / notatki / podsumowania     |
| `test:`     | testy                                           |

### Zasady

- opis w czasie teraźniejszym, tryb rozkazujący (np. "Dodaj", "Popraw", "Uprość")
- bez kropki na końcu
- max ~72 znaki w pierwszej linii (żeby ładnie wyglądało w logach np. `git log --oneline`)
- body jest opcjonalne, ale zalecane przy większych zmianach
    (można tutaj wytłumaczyć "dlaczego tak, a nie inaczej")

### Przykłady nazw commitów

- `lab: dodaj skrypt do parsowania journalctl`
- `journal: podsumowanie dnia 2026-02-18`
- `docs: opisz flow PR i code review`
- `feature: dodaj generator tabeli IP z geolokalizacja`
- `fix: popraw filtrowanie nieudanych logowan`
- `refactor: rozdziel parser na modul i utils`
- `chore: dodaj shellcheck do CI`
- `test: dodaj testy dla parsera logow`

### Przykład (większy commit z listą)

`lab: dodaj skrypt do analizy nieudanych logowan`

- parsuj `journalctl` z ostatniego bootu
- generuj tabele: data | ip | kraj | link do mapy
- dodaj README z przykladem uzycia

## Branch namse

Używamy krótkich, czytelnych nazw w formacie:

`<kategoria>/<krotki-opis>`

- małe litery
- słowa rozdzielone myślnikiem `-` (nie korzystamy z podłóg `_`)
- bez polskich znaków (ą,ę,ł...), bez spacji
- opis krótki (najlepiej 2-6 słów)
- opcjonalnie można dodać numer zadania: `zad12-...`

### Kategorie funkcjonalności

**Kod / funkcjonalność:**

- `feature/` - nowa funkcjonalność (np. nowa komenda, nowy skrypt, nowy moduł)
- `fix/` - poprawka błędu (coś nie działało, crash, zła logika)
- `refactor/` - zmiana struktury bez zmiany działania (porządki w kodzie)
- `chore/` - rzeczy techniczne/utrzymaniowe (konfiguracje, CI, formatowanie, zależności)

**Materiały z zajęć i repo:**

- `lab/` - rozwiązanie zadania / ćwiczenia laboratoryjnego (kod + opis)
  - używaj, gdy robisz konkretne zadanie typu "Zrób skrypt X" albo "Napisz program Y"
- `journal/` - notatki, dziennik pracy, podsumowania dnia/tygodnia
  - używaj, gdy dopisujesz obserwacje, wnioski, log z wykonania, checklisty, "co dziś robiłem"
- `docs/` - dokumentacja i instrukcje (README, CONTRIBUTING, opisy narzędzi)
  - używaj, gdy zmiana jest typowo tekstowa/dokumentacyjna, a nie "journal"
- `test/` - testy (dodanie/zmiana testów), bez zmian funkcjonalnych poza testowaniem

### Jak wybrać kategorię?

| Problem                                                    | Kategoria      |
| ---------------------------------------------------------- | -------------- |
| Aktualizujesz **instrukcję / README / opis narzędzia**     | `docs/...`     |
| Dopisujesz **notatki z dnia / podsumowanie / dziennik**    | `journal/...`  |
| Robisz **zadanie z labów**                                 | `lab/...`      |
| Zmieniasz **konfiguracje, formatowanie, pliki pomocnicze** | `chore/...`    |
| Naprawiasz **coś, co było zepsute**                        | `fix/...`      |
| Dodajesz **nową rzecz, która ma działać**                  | `feature/...`  |
| Przestawiasz kod "żeby było ładniej", ale działa tak samo  | `refactor/...` |

### Przykłady nazw branchy

- `lab/zad03-journalctl-tabela-ip`
- `journal/2026-02-18-podsumowanie-ssh`
- `docs/opis-pr-flow`
- `feature/skrypt-setup-ssh`
- `fix/blad-parsowania-logow`
- `refactor/podzial-pliku-na-moduly`
- `chore/formatowanie-shellcheck`
- `test/dodanie-testow-parsera`

## Minimalny checklist przed pushem

- `git fetch` / `git push`, czy faktycznie jetesmy up-to-date
- `git status` jest czysty po commicie
- nie commitujesz sekretów (`.env`, tokeny, klucze prywatne)
- dopisałeś wpis w journalu

## Konflikty merge

Jeśli pracujemy na jednej gałęzi:

- najpierw `git pull`
- dopiero potem commit/push
