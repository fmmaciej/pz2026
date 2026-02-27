#!/usr/bin/env bash

QUICK=false
PATH_AUDIT_DIR="./audits"

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

mkdir -p $PATH_AUDIT_DIR
path=$PATH_AUDIT_DIR/audit_$(hostname)_$(date +%Y)-$(date +%m)-$(date +%d)_$(date +%H)$(date +%M)$(date +%S).txt
touch $path

echo "METADANE AUDYTU" >> $path
echo "Użytkownik: $(whoami)" >> $path
echo "Data: $(date)" >> $path
echo "Nazwa hosta: $(hostname)" >> $path
if [[ -n "$SSH_CLIENT" ]]; then
    echo "Połączenie: SSH" >> $path
    echo "Adres IP: $(echo $SSH_CLIENT | awk '{print $1}')" >> $path
else
    echo "Połączenie: LOCAL" >> $path
fi

echo "" >> $path
echo "INFORMACJE O SYSTEMIE" >> $path
echo "Wersja systemu: $(cat /etc/os-release)" >> $path
echo "Kernel i architektura: $(uname -a)" >> $path
echo "Uptime: $(uptime -p)" >> $path
echo "Obciążenie systemu: $(uptime)" >> $path

echo "" >> $path
echo "ZASOBY" >> $path
echo "Użycie dysku:" >> $path
df -h >> $path
echo "Pamięć:" >> $path
free -h >> $path

if [[ $QUICK == false ]]; then
    echo "Top 5 największych katalogów w \$HOME:" >> $path
    du -sh "$HOME"/* 2>/dev/null | sort -h | tail -n 5 >> $path
fi

exit