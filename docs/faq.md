# FAQ

## Git pyta o hasło do GitHuba

Prawdopodobnie używasz remote po HTTPS. Ustaw SSH remote:

```bash
git remote set-url origin git@github.com:fmmaciej/pz2026.git
```

## Nie działa python / lint w VSCode Remote

Upewnij się, że jesteś w oknie Remote (VPS) i wybierz interpreter:

`F1 -> Python: Select Interpreter`.
