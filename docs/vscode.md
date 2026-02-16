# VSCode + VPS: szybki start (Bash, Python, Markdown, Git)

Ten dokument opisuje minimalny setup VSCode do pracy z Linuxowym VPS-em (przez SSH) oraz codziennego dłubania w Bash/Python/Markdown i wersjonowania w Git.

## 1. Podstawy: jak pracujemy z VPS w VSCode

### Wtyczka obowiązkowa

- **Remote - SSH** (`ms-vscode-remote.remote-ssh`)
  - Pozwala otwierać foldery *na VPS* jakby były lokalne.
  - Terminal w VSCode działa wtedy "na serwerze".

### Minimalny workflow

1. Zainstaluj wtyczkę **Remote - SSH**
2. `F1` -> `Remote-SSH: Connect to Host...`
3. Dodaj hosta (albo edytuj `~/.ssh/config`) i połącz się.
4. `File -> Open Folder...` i wybierz katalog na VPS (np. `/srv/pz2026`).

> Tip: jak folder jest "na VPS", to wtyczki typu Python/Bash działają "po stronie serwera" (VSCode doinstaluje swój server + rozszerzenia w zdalnym środowisku).

## 2. Profile w VSCode

**Profile** to paczki ustawień + wtyczek. Dzięki temu możesz mieć:

- profil "pz2026 Linux (VPS)"
- profil "Moje projekty"
- profil "Prezentacja / Lekcja"

### Jak używać profili

- Kliknij ikonę profilu (lewy dolny róg) -> **Profiles**
- Utwórz profil "`pz2026` Linux (VPS)"
- Zainstaluj w nim tylko rzeczy potrzebne na zajęcia

> Dodatkowo możesz włączyć **Settings Sync**, ale na `pz2026` często lepiej trzymać konfigurację lokalnie.

## 3. Wtyczki

Poniżej jest lista zalecanych wtyczek VSCode. Pełna ich lista jest w `.vscode/extensions.json`.

### A. VPS / SSH

- **Remote - SSH** - `ms-vscode-remote.remote-ssh`

### B. Bash

- **ShellCheck** - `timonwong.shellcheck` (linter, wykrywa typowe błędy)
- **Bash IDE** - `mads-hartmann.bash-ide-vscode` (podpowiedzi, symbolika)

### C. Python (w przyszłości)

- **Python** - `ms-python.python`
- **Pylance** - `ms-python.vscode-pylance` (podpowiedzi, typy)
- **Ruff** - `charliermarsh.ruff` (lint + format, szybkie)

### D. Markdown

- **Markdown All in One** - `yzhang.markdown-all-in-one` (TOC, skróty, autoformat)
- **markdownlint** - `davidanson.vscode-markdownlint` (porządek w stylu)

### E. Git

- Wbudowany Git w VSCode jest OK, ale warto:
- **Git Graph** - `mhutchie.git-graph` (ładna historia commitów)

### F. Jakość życia

- **EditorConfig** - `editorconfig.editorconfig` (spójne wcięcia/końcówki linii)
- **ident-rainbow** - `oderwat.indent-rainbow` - ładne kolorwanie wcięć (ah ten Python)

## 4. Podstawowa konfiguracja VSCode (polecane ustawienia)

### A. Terminal

- Ustaw domyślny shell: **bash** (zwłaszcza na zajęciach)
- Włącz czytelne kopiowanie i przewijanie (zwykle jest OK domyślnie)

**Kopiowanie:**

- `terminal.integrated.copyOnSelection`
Jeśli true, zaznaczenie automatycznie kopiuje (jak w terminalach linuksowych).
- `terminal.integrated.rightClickBehavior`
Co robi PPM: wkleja / pokazuje menu. Na macOS często chcesz “Paste”.

**Przewijanie / historia:**

- `terminal.integrated.scrollback`
Ile linii historii trzyma terminal. Domyślnie bywa ok, ale przy logach z CI albo buildów możesz chcieć więcej (np. 100000).
- `terminal.integrated.fastScrollSensitivity` i `...mouseWheelScrollSensitivity`
Gdy scroll jest za szybki/za wolny.

**Czytelność:**

- `terminal.integrated.gpuAcceleration`
Jeśli przewijanie laguje lub font się rwie, czasem pomaga przełączenie.

### B. Formatowanie i zapisywanie

Polecam "format on save" tylko tam, gdzie macie narzędzie formatujące (Python/Markdown), a nie globalnie na wszystko.

### C. Pliki i whitespace

W repo `pz2026` bardzo pomaga spójne ustawienie formatowania m. in. takich rzeczy jak:

- trimowanie spacji na końcu linii
- final newline

Przykładowe `settings.json` (użytkownika lub workspace):

```json
{
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "editor.rulers": [100],
  "editor.minimap.enabled": false,

  "python.analysis.typeCheckingMode": "basic",
  "python.defaultInterpreterPath": "python3",

  "editor.formatOnSave": true,
  "[markdown]": { "editor.formatOnSave": true },
  "[python]": { "editor.formatOnSave": true },
  "[shellscript]": { "editor.formatOnSave": false }
}
```

## 5. Konfiguracja repo

### A. Rekomendowane wtyczki dla repo

W repo dodaj plik `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "be5invis.toml",
    "bierner.markdown-mermaid",
    "charliermarsh.ruff",
    "davidanson.vscode-markdownlint",
    "editorconfig.editorconfig",
    "gruntfuggly.todo-tree",
    "mads-hartmann.bash-ide-vscode",
    "marp-team.marp-vscode",
    "mechatroner.rainbow-csv",
    "mhutchie.git-graph",
    "ms-python.debugpy",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.vscode-python-envs",
    "ms-vscode-remote.remote-ssh",
    "ms-vscode-remote.remote-ssh-edit",
    "ms-vscode.remote-explorer",
    "oderwat.indent-rainbow",
    "samuelcolvin.jinjahtml",
    "shd101wyy.markdown-preview-enhanced",
    "timonwong.shellcheck",
    "tomoki1207.pdf",
    "usernamehw.errorlens",
    "vscodevim.vim",
    "xubylele.jinja2-html-enhancer",
    "yzhang.markdown-all-in-one"
  ]
}
```

### B. .editorconfig

W repo dodaj plik `.editorconfig`:

```editorconfig
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[*.md]
trim_trailing_whitespace = false
```
