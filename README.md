# Softwaresikkerhed - Logging & Monitoring Opgave

En Python-applikation der demonstrerer **logging** og **Prometheus metrics** til monitoring og overvågning af systemaktivitet.

## 🎯 Formål

Projektet viser hvordan man:
- Logger aktivitet på forskellige niveauer (INFO, ERROR, CRITICAL)
- Samler metrics med Prometheus til overvågning
- Håndterer fejl og kritiske situationer
- Monitorer ressourceforbrug (CPU)

## 📋 Funktionalitet

Applikationen simulerer en web-service som:
- **Tæller requests** med en Prometheus Counter
- **Overvåger CPU-forbrug** med en Prometheus Gauge (10-90%)
- **Logger aktivitet** til `app.log` baseret på CPU-niveau:
  - ✅ **INFO**: Normal aktivitet
  - ⚠️ **ERROR**: Høj CPU (>80%)
  - 🔴 **CRITICAL**: Kritisk CPU (>95%)
- **Håndterer fejl** og logger dem for fejlfinding

## 🚀 Start

### Installér afhængigheder

```bash
pip install prometheus-client
```

### Kør applikationen

```bash
python app.py
```

### Overvåg metrics

Prometheus metrics kan ses på:
```
http://localhost:8000
```

### Se logs

Logs bliver skrevet til `app.log`:
```bash
tail -f app.log
```

## 📁 Projektstruktur

```
Sofwaresikkerhed/
├── app.py              # Hovedapplikation
├── app.log             # Logfil (genereres ved kørsel)
├── logging_project/    # Projektmappe
└── README.md           # Denne fil
```

## 📊 Prometheus Metrics

Applikationen eksponerer følgende metrics:

- `app_requests_total` - Antal requests behandlet (Counter)
- `fake_cpu_usage_percent` - Simuleret CPU-forbrug (Gauge)

## 🛑 Stop applikationen

Tryk `Ctrl+C` for at stoppe programmet.

---

**Udviklet af**: Klaus Therkildsen  
**Dato**: April 2026
