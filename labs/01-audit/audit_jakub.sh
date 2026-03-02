#!/usr/bin/env bash

NOT_QUICK=true

CONFIG_PATH="$HOME/.config/audit_jakub"
CONFIG_NAME="audit.conf"
FULL_CONFIG_PATH="$CONFIG_PATH/$CONFIG_NAME"

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in 
            -o | --out)
                [[ -z "$2"]] && echo "Brak podanej ścieżki dla: $1"; exit 1

                PATH_AUDIT_DIR="$2"

                case "$3" in
                    -s | --setdefault)
                        sed -i "s|^PATH_AUDIT_DIR=.*|PATH_AUDIT_DIR=\"$2\"|" "$FULL_CONFIG_PATH"
                        shift 3
                        ;;
                    *)
                        shift 2
                esac
                ;;
            -q | --quick)
                NOT_QUICK=false
                shift
                ;;
            *)
            echo "Nieznany argument: $1"
            exit 1
            ;;
        esac
    done
}

load_config() {
    if [[ ! -f "$FULL_CONFIG_PATH" ]]; then
        mkdir -p "$CONFIG_PATH"
        echo "PATH_AUDIT_DIR=\"./audits\"" > "$FULL_CONFIG_PATH"

        source "$FULL_CONFIG_PATH"
    else
        source "$FULL_CONFIG_PATH"
    fi
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
    load_config
    parse_args "$@"
    [[ -d "$PATH_AUDIT_DIR" ]] || mkdir -p "$PATH_AUDIT_DIR"
    create_file
}

main "$@"