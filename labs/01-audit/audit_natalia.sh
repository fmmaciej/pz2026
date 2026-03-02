#!/usr/bin/env bash

QUICK=false
PATH_AUDIT_DIR="./audits"

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --quick)
                QUICK=true
                shift
                ;;
            --out)
                PATH_AUDIT_DIR="$2"
                shift 2
                ;;
        esac
    done
}

create_file() {
    mkdir -p $PATH_AUDIT_DIR
    path=$PATH_AUDIT_DIR/audit_$(hostname)_$(get_date).txt

    extract_data_to_file
}

get_date() {
    echo $(date +%Y)-$(date +%m)-$(date +%d)_$(date +%H)$(date +%M)$(date +%S)
}

extract_data_to_file() {
    {
        echo "METADANE AUDYTU" 
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
        echo "Wersja systemu: $(cat /etc/os-release)" 
        echo "Kernel i architektura: $(uname -a)" 
        echo "Uptime: $(uptime -p)" 
        echo "Obciążenie systemu: $(uptime)" 

        echo "" 
        echo "ZASOBY" 
        echo "Użycie dysku:" 
        df -h 
        echo "Pamięć:" 
        free -h 

        if [[ $QUICK == false ]]; then
            echo "Top 5 największych katalogów w \$HOME:" 
            du -sh "$HOME"/* 2>/dev/null | sort -h | tail -n 5 
        fi
    } > $path;
}

main() {
    parse_args
    create_file    
}

main