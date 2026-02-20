# Ćwiczenie: analiza działania funkcji Bash

## Cel

Nauczyć się czytać skrypt Bash:

- rozumieć warunki
- skutki uboczne (usuwanie plików)
- znaczenie flag
- przewidywać zachowanie funkcji w różnych scenariuszach

## Repozytorium

Interesujące nas funkcje znajdziecie w pliku `install.sh` w repo [gen-license](https://github.com/fmmaciej/gen-license).

## Zakres

Analiza będzie dotyczyła funkcji `install_app()`.

Przygotujcie analizę według schematu poniżej (w podpunktach odnoszę się do przykładu, który znajdziecie poniżej):

1. **Opis wysokopoziomowy:** co funkcja robi i po co istnieje (2-4 zdania).
2. **Wejścia / zależności:** z jakich zmiennych korzysta (np. `INSTALL_DIR`, `LINK_PATH`) i jakie inne funkcje woła (np. `note`, `ensure_local_dirs`).
3. **Warunki i gałęzie:** wypisz wszystkie `if`/`else` i opisz, kiedy się wykonują.
4. **Skutki uboczne:** co zmienia w systemie plików (tworzy/usuwa/zmienia linki), jakie komendy są "niebezpieczne".
5. **Scenariusze testowe:** podaj min. 4 scenariusze (różne stany plików i katalogów) oraz przewidywany wynik (co zostanie wypisane i co zostanie usunięte/utworzone).

**Plik wynikowy:**

Analizę wrzućcie do katalogu `labs/00-reading/analiza` (jeżeli nie istnieje to proszę o utworzenie) i nazwijcie ją swoim imieniem (np. `marek.md`, `anna.md`). Plik w formacie markdown `.md` według podanego schematu i z własnymi scenariuszami testowymi.

**Wskazówka:**

W analizie `install_app()` zwróccie szczególną uwagę na to, jak tworzone są katalogi i linki, skąd bierze się źródło plików do instalacji, oraz czy są jakiekolwiek zabezpieczenia przed "nadpisaniem" istniejących elementów.

**Dodatkowe pytanie:**

Dlaczego wykorzystujemy tam `~/.local/bin`? ;)

**Do pomocy polecam:**

- manual parametrów z instrukcji warunkowych (np. `[[ -n ... ]]`) -> `man test`
- manual różnych komend (np. `man trap`) -> `man <command>`
- wyszukiwanie w manualu służy klawisz slash -> `/<fraza>`
- następna/poprzednia znaleziona fraza klawisza n i p -> `/<fraza>`, a później `n`, albo `p`

**Powodzenia!!!**

## Przykład

### Kod

```bash
uninstall_app() {
    ensure_local_dirs

                 
    if [[ -L "$LINK_PATH" || -e "$LINK_PATH" ]]; then
        note "Removing: $LINK_PATH"
        rm -f -- "$LINK_PATH"
    else
        note "No symlink found at: $LINK_PATH"
    fi

    if [[ -d "$INSTALL_DIR" ]]; then
        note "Removing: $INSTALL_DIR"
        rm -rf -- "$INSTALL_DIR"
    else
        note "No install dir found at: $INSTALL_DIR"
    fi

    note "Uninstalled."
```

### Analiza

#### 1) Co robi ta funkcja?

`uninstall_app()` usuwa elementy zainstalowanej aplikacji:

- najpierw usuwa link (np. symlink w `~/.local/bin`)
- potem usuwa katalog instalacyjny (np. w `~/.local/share/...`)
- na końcu wypisuje komunikat `"Uninstalled."`

#### 2) Zależności (funkcje i zmienne)

Wywoływane funkcje:

- `ensure_local_dirs()` - zapewne tworzy wymagane katalogi (np. ~/.local/bin, ~/.local/share)
- `note()` - funkcja logująca komunikaty (np. na stdout)

Używane zmienne:

- `LINK_PATH` - ścieżka do linku/plików wykonywalnych, które mają zostać usunięte.
- `INSTALL_DIR` - ścieżka do katalogu instalacji aplikacji.

#### 3) Analiza krok po kroku

**Krok A przygotowanie środowiska:**

- `ensure_local_dirs()`

**Krok B usuwanie linku lub pliku pod LINK_PATH:**

Warunek:

```bash
if [[ -L "$LINK_PATH" || -e "$LINK_PATH" ]]; then
```

- operator `||` jest logicznym "lub"
- `[[ ... ]]` to test wbudowany w Bash (bezpieczniejszy i wygodniejszy od `test` lub `[`)
- `-L "$LINK_PATH"`: prawda, jeśli ścieżka istnieje i jest linkiem symbolicznym
- `-e "$LINK_PATH"`: prawda, jeśli ścieżka istnieje (cokolwiek: plik, katalog, link, itp.)

Gałąź "tak":

```bash
note "Removing: $LINK_PATH"
rm -f -- "$LINK_PATH"
```

- `rm -f`:
- `-f` (force): nie pytaj, nie marudź; brak błędu, jeśli pliku nie ma (zwykle).
- `--`: koniec opcji dla `rm`. To zabezpieczenie: jeśli ścieżka zaczyna się od `-`, `rm` nie potraktuje jej jako flagi.
- `"$LINK_PATH"` w cudzysłowie: - chroni spacje i znaki specjalne w ścieżce.

Gałąź "nie":

```bash
note "No symlink found at: $LINK_PATH"
```

Uwaga: komunikat mówi "No symlink...", czyli brak linku, co jest nieco mylące. Lepszym rozwiązaniem było by ...

I tak dalej ...

#### 4) Skutki uboczne (co zmienia na dysku)

- Potencjalnie usuwa plik/link pod LINK_PATH.
- Potencjalnie usuwa cały katalog INSTALL_DIR wraz z zawartością.
- Może utworzyć katalogi bazowe przez ensure_local_dirs.

#### 5) Scenariusze testowe (przykładowe)

a. `LINK_PATH` istnieje jako symlink, `INSTALL_DIR` istnieje jako katalog

```text
Usunie link i cały katalog, wypisze `"Removing..."` dwa razy, potem `"Uninstalled."`
```

b. `LINK_PATH` nie istnieje, `INSTALL_DIR` istnieje

```text
Wypisze `"No symlink..."`, usunie katalog, potem `"Uninstalled."`
```

c. `LINK_PATH` istnieje jako zwykły plik (nie symlink), `INSTALL_DIR` nie istnieje

```text
Warunek z `-e` wejdzie, usunie plik, potem `"No install dir..."`, potem `"Uninstalled."`
```

d. Obie ścieżki nie istnieją

```text
Dwa komunikaty `"No ... found ..."`, potem `"Uninstalled."`.
```
