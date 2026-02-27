# Ćwiczenie: system-audit — raport z audytu w pliku z datą

## Cel

Napisać skrypt `audit.sh`, który:

1. tworzy katalog na raporty,
2. generuje plik raportu z aktualną datą w nazwie,
3. zbiera podstawowe informacje o użytkowniku, połączeniu i systemie,
4. dopisuje je w czytelnym formacie do pliku,
5. na końcu pokazuje podsumowanie i ścieżkę do raportu.

## Wymagania minimalne

Raport ma zawierać (w tej kolejności):

### A. Metadane audytu

- kto robi audyt (`whoami`, ewentualnie też `id`)
- kiedy (`date -Iseconds` albo `date`)
- nazwa hosta (`hostname`)
- z jakiego IP jest połączony (jeśli jest SSH)
- podpowiedź: zmienne `SSH_CLIENT`, `SSH_CONNECTION`
- jeśli nie ma SSH -> wpisz "LOCAL"

### B. Informacje o systemie

- wersja systemu (np. `/etc/os-release`)
- kernel i architektura (`uname -a`)
- uptime (`uptime -p` albo `cat /proc/uptime`)
- obciążenie (load average) (`uptime`)

### C. Zasoby

- użycie dysku (`df -h`)
- pamięć (`free -h`)
- top 5 największych katalogów w `$HOME` (albo w `/var/log` dla odważnych)
- podpowiedź: `du -sh "$HOME"/* 2>/dev/null | sort -h | tail -n 5`

## Dodatkowe

### Opcje skryptu

- `./audit.sh` -> normalny raport
- `./audit.sh --quick` -> bez ciężkich rzeczy (`du`)
- `./audit.sh --out /path/to/dir` -> własny katalog raportów

## Konwencja plików

- katalog raportów: `./audits/`
- nazwa pliku: `audit_<hostname>_YYYY-MM-DD_HHMMSS.txt`

## Przykład

`audits/audit_pz2026_2026-02-18_214530.txt`
