#!/usr/bin/env bash

NOT_QUICK=true
PATH_AUDIT_DIR="./audits"

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in 
            -o | --out)
                make_dir "$2"
                shift 2
                ;;
            -q | --quick)
                NOT_QUICK=false
                shift
                ;;
            *)
            echo "Unknown arg: $1"
        esac
    done
}

make_dir() {
    PATH_AUDIT_DIR="${1:-$PATH_AUDIT_DIR}"
    [[ -d "$PATH_AUDIT_DIR" ]] || mkdir -p "$PATH_AUDIT_DIR"
}

create_file() {
    PATH_FILE="$PATH_AUDIT_DIR/audit_$(hostname)_$(date +%Y-%m-%d_%H%M%S).txt"

    {
        echo "METADANE AUDYTU"
        echo ""
        echo "Użytkownik: $(whoami)"
        echo "Data: $(date)"
        echo "Nazwa hosta: $(hostname)"

        if [[ -n "$SSH_CLIENT" ]]; then
            echo "Połączenie: SSH"
            echo "Adres IP: $(echo $SSH_CLIENT | awk '{print $1}')"
        else
            echo "Połączenie: LOCAL"
        fi

        echo ""
        echo "INFORMACJE O SYSTEMIE"
        echo ""
        echo "Wersja systemu: $(cat /etc/os-release)"
        echo "Kernel i architektura: $(uname -a)"
        echo "Uptime: $(uptime -p)"
        echo "Obciążenie systemu: $(uptime)"

        if $NOT_QUICK; then
            echo ""
            echo "ZASOBY"
            echo ""
            echo "Użycie dysku: $(df -h)"
            echo "Pamięć: $(free -h)"
            echo ""
            echo "Top 5 największych katalogów w $HOME: $(du -sh "$HOME"/* 2>/dev/null | sort -h | tail -n 5)"
        fi
    } > "$PATH_FILE"
    
    echo "Audit zapisany do: $PATH_FILE"
}

main() {
    parse_args "$@"
    make_dir
    create_file
}

main "$@"