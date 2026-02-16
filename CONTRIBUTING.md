# CONTRIBUTING (zasady pracy w repo)

## 1. Gdzie wrzucać i co?

- Notatki z dnia: `journal/YYYY-MM-DD.md`
- Rozwiązania zadań: `labs/<lab>/solutions/<nick>/...`
- Krótkie przydatne kawałki: `snippets/`
- Dłuższe materiały: `docs/`

## 2. Nazwy plików

- Daty zawsze w formacie: `YYYY-MM-DD`
- Skrypty bash: `*.sh`
- Skrypty python: `*.py`
- Notatki: `*.md`

## 3. Commit messages (prosto)

- `journal: YYYY-MM-DD`
- `lab: <temat>`
- `fix: <krótki opis>`
- `chore: housekeeping`

## 4. Minimalny checklist przed pushem

- `git status` jest czysty po commicie
- nie commitujesz sekretów (`.env`, tokeny, klucze prywatne)
- dopisałeś wpis w journalu

## 5. Konflikty merge

Jeśli pracujemy na jednej gałęzi:

- najpierw `git pull`
- dopiero potem commit/push
