# Kod

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

# Analiza

## 1) Co robi ta funkcja?

install_app() instaluje aplikację w sposób atomowy:

- sprawdza, czy wszystkie wymagane pliki istnieją w repozytorium,
- kopiuje je do katalogu tymczasowego,
- upewnia się, że entrypoint istnieje i jest wykonywalny,
- podmienia katalog instalacyjny na nowy,
- tworzy symlink w ~/.local/bin,
- wypisuje komunikat `"Installed."`.

## 2) Zależności (funkcje i zmienne)

Wywoływane funkcje:

- ensure_local_dirs() – tworzy wymagane katalogi
- repo_root() – zwraca ścieżkę do katalogu repozytorium
- path_exists_in_repo() – sprawdza, czy dana ścieżka istnieje w repo
- die() – kończy program
- note() – wypisuje komunikaty
- copy_item() – kopiuje element do katalogu tymczasowego
- make_executable_if_present() – daje możliwość uruchomienia pobieranego pliku

Używane zmienne:

- COPY_ITEMS – tablica elementów do skopiowania
- INSTALL_DIR – katalog instalacyjny
- ENTRYPOINT_REL – względna ścieżka do pobieranego pliku
- LINK_PATH – ścieżka symlinku w ~/.local/bin
- BIN_NAME – nazwa polecenia przy wykonywaniu


## 3) Analiza krok po kroku

### Krok A – przygotowanie środowiska\

```bash
ensure_local_dirs

local root
root="$(repo_root)"
```

Zapewnia istnienie lokalnych katalogów instalacyjnych oraz pobiera katalog repozytorium.


**Krok B – walidacja plików źródłowych**

```bash
local item
for item in "${COPY_ITEMS[@]}"; do
    path_exists_in_repo "$root" "$item" || die "COPY_ITEMS refers to missing path: $item"
done
```

- Przechodzi przez tablicę COPY_ITEMS
- Jeśli którykolwiek plik nie istnieje -> die() przerywa instalację

**Krok C – utworzenie katalogu tymczasowego**

```bash
local tmp
tmp="$(mktemp -d "${INSTALL_DIR}.tmp.XXXXXX")"
trap 'rm -rf -- "$tmp"' EXIT
```

- `mktemp -d` tworzy unikalny katalog tymczasowy (`$tmp`)
- `trap` gwarantuje jego usunięcie przy wyjściu z funkcji (nawet przy błędzie)

**Krok D – kopiowanie plików**

```bash
for item in "${COPY_ITEMS[@]}"; do
    copy_item "$root" "$item" "$tmp"
done
```

- Wszystkie pliki są kopiowane do katalogu tymczasowego (`$tmp`)

**Krok E – sprawdzenie entrypointa**

```bash
[[ -f "${tmp}/${ENTRYPOINT_REL}" ]] || die "Entrypoint not found after copy: ${ENTRYPOINT_REL}"

make_executable_if_present "${tmp}/${ENTRYPOINT_REL}"
```

- Sprawdza, czy `$ENTRYPOINT_REL` istnieje jako plik
- Jeśli nie -> instalacja zostaje przerwana

**Krok F – podmiana katalogu instalacyjnego**

```bash
if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf -- "$INSTALL_DIR"
fi

mkdir -p "$(dirname -- "$INSTALL_DIR")"
mv -- "$tmp" "$INSTALL_DIR"
trap - EXIT
```

- Jeśli katalog instalacyjny istnieje -> jest usuwany
- Tworzony jest czysty katalog nadrzędny
- Katalog tymczasowy zostaje przeniesiony w miejsce docelowe
- `trap` zostaje wyłączony (`$tmp` już nie jest tymczasowy)


**Krok G – tworzenie symlinku**

```bash
if [[ -L "$LINK_PATH" || -e "$LINK_PATH" ]]; then
    rm -f -- "$LINK_PATH"
fi

ln -s -- "${INSTALL_DIR}/${ENTRYPOINT_REL}" "$LINK_PATH"
```

- Jeśli coś istnieje pod `$LINK_PATH` -> zostaje usunięte
- Tworzony jest nowy symlink wskazujący na `$ENTRYPOINT_REL:`


**Krok H – komunikat końcowy**

```bash
note "Installed."
note "Run: $BIN_NAME --help"
```

- Informuje użytkownika o instalacji zakończonej sukcesem


## 4) Skutki uboczne (co zmienia na dysku)

- Tworzy katalog tymczasowy (usuwany po sukcesie)
- Usuwa istniejący `$INSTALL_DIR`
- Tworzy nowy katalog instalacyjny
- Usuwa istniejący plik/symlink pod `$LINK_PATH`
- Tworzy nowy symlink
- Zmienia cechy `ENTRYPOINT_REL` (nadaje możliwość wykonania)


## 5) Scenariusze testowe

a. `COPY_ITEMS` zawiera nieistniejącą ścieżkę w repozytorium

- Instalacja przerwie się błędem `"COPY_ITEMS refers to missing path: ..."`.
- Nie zostanie utworzony ani zmodyfikowany `$INSTALL_DIR`.
- `LINK_PATH` pozostanie bez zmian.


b. Po skopiowaniu plików brakuje `ENTRYPOINT_REL`

- Instalacja przerwie się błędem `"Entrypoint not found after copy: ..."`.
- `$INSTALL_DIR` nie zostanie podmieniony.
- `$LINK_PATH` nie zostanie utworzony ani zmodyfikowany.


c. `$LINK_PATH` istnieje jako katalog

- Zostanie wypisane `"Removing existing bin entry: ..."`.
- Próba `rm -f` na katalogu zaskutkuje błędem.
- `$INSTALL_DIR` pozostanie zainstalowany, ale symlink może nie zostać utworzony.