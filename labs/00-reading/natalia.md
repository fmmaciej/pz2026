## Kod
```bash
install_app() {
    ensure_local_dirs

    local root
    root="$(repo_root)"

    local item
    for item in "${COPY_ITEMS[@]}"; do
        path_exists_in_repo "$root" "$item" || die "COPY_ITEMS refers to missing path: $item"
    done

    # temp dir for atomic install
    local tmp
    tmp="$(mktemp -d "${INSTALL_DIR}.tmp.XXXXXX")"
    trap 'rm -rf -- "$tmp"' EXIT

    note "Copying files into temp dir: $tmp"
    for item in "${COPY_ITEMS[@]}"; do
        copy_item "$root" "$item" "$tmp"
    done

    # Ensure entrypoint exists in installed tree
    [[ -f "${tmp}/${ENTRYPOINT_REL}" ]] || die "Entrypoint not found after copy: ${ENTRYPOINT_REL}"
    make_executable_if_present "${tmp}/${ENTRYPOINT_REL}"

    # Swap install dir
    if [[ -d "$INSTALL_DIR" ]]; then
        note "Replacing existing install dir: $INSTALL_DIR"
        rm -rf -- "$INSTALL_DIR"
    fi

    mkdir -p "$(dirname -- "$INSTALL_DIR")"
    mv -- "$tmp" "$INSTALL_DIR"
    trap - EXIT

    # Symlink in ~/.local/bin
    if [[ -L "$LINK_PATH" || -e "$LINK_PATH" ]]; then
        note "Removing existing bin entry: $LINK_PATH"
        rm -f -- "$LINK_PATH"
    fi

    ln -s -- "${INSTALL_DIR}/${ENTRYPOINT_REL}" "$LINK_PATH"

    note "Installed."
    note "Run: $BIN_NAME --help"
}
```


## Analiza

### 1) Co robi ta funkcja?
Funkcja install_app() instaluje aplikację gen-license:
- tworzy potrzebne katalogi (~/.local/bin, ~/.local/share)
- kopiuje pliki aplikacji z repozytorium do tymczasowego katalogu
- sprawdza, czy plik gen-license.sh istnieje i nadaje mu prawa do wykonywania
- podmienia stary katalog instalacji na nowy
- usuwa istniejący plik lub link i tworzy nowy link symboliczny do entrypointu


### 2) Zależności

#### Wywoływane funkcje:
- `ensure_local_dirs()` - tworzy wymagane katalogi (~/.local/bin, ~/.local/share)
- `repo_root()` - zwraca ścieżkę do katalogu repozytorium, gdzie znajduje się plik install.sh
- `path_exists_in_repo()` - sprawdza czy plik istnieje w repozytorium
- `copy_item()` - kopiuje pliki lub katalog do katalogu docelowego
- `make_executable_if_present()` - nadaje prawo do wykonywania pliku, jeżeli istnieje (chmod +x)
- `note()` - wypisuje komunikaty
- `die()` - wyświetla komunikat o błędzie i przerywa skrypt

#### Używane zmienne:
a) lokalne:
- `root` - ścieżka do katalogu repozytorium
- `item` - aktualny plik w pętli kopiowania
- `tmp` - katalog tymczasowy do instalacji

b) globalne:
- `COPY_ITEMS` - lista plików do skopiowania
- `INSTALL_DIR` - ścieżka katalogu do instalacji
- `ENTRYPOINT_REL` - nazwa pliku wykonywalnego (gen-license.sh)
- `LINK_PATH` - ścieżka do linku symbolicznego


### 3) Analiza krok po kroku

#### 1. Utworzenie wymaganych katalogów
```bash
ensure_local_dirs
```


#### 2. Określenie katalogu repozytorium
```bash
local root
root="$(repo_root)"
```
- stworzenie zmiennej lokalnej `root`
- funkcja `repo_root()` zwraca katalog, gdzie znajduje się plik `install.sh`


#### 3. Sprawdzenie czy pliki do skopiowania istnieją
```bash
local item
for item in "${COPY_ITEMS[@]}"; do
    path_exists_in_repo "$root" "$item" || die "COPY_ITEMS refers to missing path: $item"
done
```
- stworzenie zmiennej lokalnej `item`
#### Warunek:
```bash
path_exists_in_repo "$root" "$item"
```
- sprawdza, czy dany plik istnieje w repozytorium
- operator `||` jest logicznym lub, jeżeli poprzednie polecenie zwróci fałsz, to wykona kolejne polecenie

#### Gałąź "tak":
- kontynuacja pętli po elementach `COPY_ITEMS`

#### Gałąź "nie":
```bash
die "COPY_ITEMS refers to missing path: $item"
```
- zostaje wywołana funkcja `die()`, która przerywa instalację


#### 4. Utworzenie katalogu tymczasowego
```bash
local tmp
tmp="$(mktemp -d "${INSTALL_DIR}.tmp.XXXXXX")"
trap 'rm -rf -- "$tmp"' EXIT
```
- stworzenie zmiennej lokalnej `tmp`
- tworzony jest tymczasowy katalog potrzebny do instalacji
- `trap` zapewnia, że w przypadku błędu podczas instalacji katalog tymczasowy zostanie usunięty


#### 5. Kopiowanie plików do katalogu tymczasowego
```bash
note "Copying files into temp dir: $tmp"
for item in "${COPY_ITEMS[@]}"; do
    copy_item "$root" "$item" "$tmp"
done
```
- wypisuje komunikat o rozpoczęciu kopiowania do katalogu tymczasowego
- pętla iteruje po tablicy `COPY_ITEMS`
- wywołuje się funkcja `copy_item()`, która kopiuje pliki do katalogu tymczasowego


#### 6. Sprawdzenie entrypointu
```bash
[[ -f "${tmp}/${ENTRYPOINT_REL}" ]] || die "Entrypoint not found after copy: ${ENTRYPOINT_REL}"
make_executable_if_present "${tmp}/${ENTRYPOINT_REL}"
```
#### Warunek:
```bash
[[ -f "${tmp}/${ENTRYPOINT_REL}" ]]
```
- sprawdza czy plik `gen-license.sh` istnieje po kopiowaniu
#### Gałąź "tak":
- kontynuacja instalacji
- zostaje wywołana funkcja `make_executable_if_present`, która nadaje prawo wykonywania pliku
#### Gałąź "nie":
```bash
die "Entrypoint not found after copy: ${ENTRYPOINT_REL}"
```
- zostaje wywołana funkcja `die()`, która przerywa instalację


#### 7. Nadpisanie poprzedniej instalacji
```bash
if [[ -d "$INSTALL_DIR" ]]; then
    note "Replacing existing install dir: $INSTALL_DIR"
    rm -rf -- "$INSTALL_DIR"
fi
```
#### Warunek:
```bash
if [[ -d "$INSTALL_DIR" ]]; then
```
- sprawdza czy katalog instalacyjny istnieje
#### Gałąź "tak":
```bash
note "Replacing existing install dir: $INSTALL_DIR"
rm -rf -- "$INSTALL_DIR"
```
- wypisuje komunikat o nadpisaniu starej instalacji
- następuje usunięcie poprzedniej instalacji z wszystkim plikami w środku katalogu
#### Gałąź "nie":
- nic się nie dzieje


#### 8. Przeniesienie katalogu tymczasowego do miejsca docelowego
```bash
mkdir -p "$(dirname -- "$INSTALL_DIR")"
mv -- "$tmp" "$INSTALL_DIR"
trap - EXIT
```
- przenosi katalog tymczasowy na miejsce docelowe
- `trap` wyłącza automatyczne usuwanie katalogu tymczasowego


#### 9. Usunięcie linku i utworzenie nowego
```bash
    if [[ -L "$LINK_PATH" || -e "$LINK_PATH" ]]; then
        note "Removing existing bin entry: $LINK_PATH"
        rm -f -- "$LINK_PATH"
    fi
```
#### Warunek:
```bash
if [[ -L "$LINK_PATH" || -e "$LINK_PATH" ]]; then
```
- sprawdza czy `$LINK_PATH` istnieje i jest linkiem symbolicznym lub istnieje w ogóle
#### Gałąź "tak":
- wyświetlany jest komunikat o usunięciu istniejącego linku, po czym link zostaje usunięty
#### Gałąź "nie":
- nic się nie dzieje


#### 10. Utworzenie linku do entrypointu w katalogu instalacji
```bash
ln -s -- "${INSTALL_DIR}/${ENTRYPOINT_REL}" "$LINK_PATH"
```


#### 11. Wyświetlenie komunikatów końcowych
```bash
note "Installed."
note "Run: $BIN_NAME --help"
```
- wyświetlenie komunikatu o ukończeniu instalacji


### 4) Skutki uboczne

- tworzy katalogi (`~/.local/bin`, `~/.local/share`)
- kopiuje pliki z `COPY_ITEMS` do katalogu tymczasowego
- usuwa istniejący katalog instalacyjny, jeśli istniał
- usuwa istniejący symlink lub plik w `LINK_PATH`
- tworzy symlink do entrypointu aplikacji


### 5) Scenariusze testowe

#### a. `INSTALL_DIR` i `LINK_PATH` nie istnieją
```text
Tworzony jest katalog tymczasowy, pliki są kopiowane z repozytorium, tworzy się nowy katalog instalacji i symlink, instalacja kończy się komunikatem `"Installed`.
```

#### b. `INSTALL_DIR` istnieje, `LINK_PATH` istnieje jako symlink
```text
Stary katalog instalacji zostaje usunięty, stary symlink w `LINK_PATH` zostaje usunięty, tworzy się nowy katalog instalacji i nowy symlink.
 
```

#### c. `INSTALL_DIR` istnieje, `LINK_PATH` nie istnieje
```text
Stary katalog instalacji zostaje usunięty, tworzony jest nowy katalog instalacji oraz nowy symlink.
```

#### d. `INSTALL_DIR` nie istnieje, `LINK_PATH` istnieje jako zwykły plik
```text
Tworzony jest katalog instalacji, stary plik pod `LINK_PATH` zostaje usunięty, zostaje utworzony nowy symlink.
```

#### e. Brakuje elementu w `COPY_ITEM`
```text
`path_exists_in_repo()` zwraca błąd, wywołana zostaje funkcja `die()`, wyświetla się komunikat `"COPY_ITEMS refers to missing path: $item"`, instalacja zostaje przerwana
```

#### f. Entrypoint nie istnieje po kopiowaniu
```text
Warunek `[[ -f "${tmp}/${ENTRYPOINT_REL}" ]]` zwraca fałsz, wywołana zostaje funkcja `die()`, wyświetla się komunikat `"Entrypoint not found after copy: ${ENTRYPOINT_REL}"`, `trap` usuwa katalog tymczasowy, instalacja zostaje przerwana.
```





























