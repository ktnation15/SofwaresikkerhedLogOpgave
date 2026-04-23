# Softwaresikkerhed - Logging & Monitoring Opgave

En Python-applikation der demonstrerer **logging** og **Prometheus metrics** til monitoring og overvågning af systemaktivitet.

## 🎯 Formål

Projektet viser hvordan man:
- Logger aktivitet på forskellige niveauer (INFO, WARNING, ERROR, CRITICAL)
- Samler metrics med Prometheus til overvågning
- Logger i JSON format for struktureret datahåndtering
- Håndterer login-forsøg med advarsel ved fejlslagne attempts
- Måler task-performance og gennemførselstid
- Håndterer fejl og kritiske situationer
- Monitorer ressourceforbrug (CPU) med multiple advarselniveauer

## 📋 Funktionalitet

Applikationen simulerer en web-service som:
- **Tæller requests** med en Prometheus Counter
- **Overvåger CPU-forbrug** med en Prometheus Gauge (10-90%)
- **Logger aktivitet** til `app.log` baseret på CPU-niveau:
  - ✅ **INFO**: Normal aktivitet
  - ⚠️ **WARNING**: CPU over 70%
  - 🔴 **ERROR**: Høj CPU (>80%)
  - 🔴 **CRITICAL**: Kritisk CPU (>95%)
- **JSON Logging** - Alle events logges også i JSON format til `stdout`
- **JSONL Fil Logging** - Alle events gemmes også i `logs.jsonl` (én JSON pr. linje)
- **Login System** - Tester login-systemet med både validering af admin og gæst-brugere
- **Task Timing** - Måler hvor lang tid hver task tager at gennemføre
- **Håndterer fejl** og logger dem for fejlfinding

### 🔑 Nye Funktioner

**`log_json(level, message, extra=None)`** - Logger beskeder i JSON format
```python
log_json("INFO", "System started")
log_json("ERROR", "High CPU", {"cpu": 85})
```

**`write_log(level, message, extra=None)`** - Gemmer beskeder i `logs.jsonl`
```python
write_log("INFO", "System started")
write_log("WARNING", "CPU is high", {"cpu": 87})
write_log("ERROR", "Something failed")
```

**`login(user)`** - Logger login-forsøg med forskellige advarsler
```python
login("admin")    # INFO log
login("guest")    # WARNING log for fejlet attempt
```

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

### Se JSON logs

JSON logs udskrives på konsollen (stdout) i realtid når programmet kører

### Se JSONL fil logs

JSONL logs gemmes i `logs.jsonl`:
```bash
tail -f logs.jsonl
```

## 📁 Projektstruktur

```
Sofwaresikkerhed/
├── app.py              # Hovedapplikation
├── app.log             # Logfil (genereres ved kørsel)
├── logs.jsonl          # JSONL logfil (genereres ved kørsel)
├── logging_project/    # Projektmappe
└── README.md           # Denne fil
```

## 📊 Prometheus Metrics

Applikationen eksponerer følgende metrics:

- `app_requests_total` - Antal requests behandlet (Counter)
- `fake_cpu_usage_percent` - Simuleret CPU-forbrug (Gauge)

## 📈 Output Eksempler

**Normal Log (app.log):**
```
2026-04-23 14:32:45 [INFO] Application started
2026-04-23 14:32:46 [INFO] Admin login successful: admin
2026-04-23 14:32:46 [WARNING] Failed login attempt: guest
2026-04-23 14:32:46 [INFO] Task completed in 2.15 seconds
2026-04-23 14:32:51 [WARNING] CPU is getting high
```

**JSON Output (stdout):**
```json
{"time": "Wed Apr 23 14:32:45 2026", "level": "INFO", "message": "System started", "extra": null}
{"time": "Wed Apr 23 14:32:46 2026", "level": "INFO", "message": "Admin login successful", "extra": {"user": "admin"}}
{"time": "Wed Apr 23 14:32:46 2026", "level": "WARNING", "message": "Failed login attempt", "extra": {"user": "guest"}}
```

**JSONL Output (logs.jsonl):**
```json
{"time":"Thu Apr 23 11:31:26","level":"INFO","message":"System started","extra":null}
{"time":"Thu Apr 23 11:31:38","level":"WARNING","message":"CPU is high","extra":{"cpu":87}}
{"time":"Thu Apr 23 11:31:39","level":"ERROR","message":"Something failed","extra":null}
```

## 🛑 Stop applikationen

Tryk `Ctrl+C` for at stoppe programmet.

---

**Udviklet af**: Klaus Therkildsen  
**Dato**: April 2026
