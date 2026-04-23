import logging
import time
import random
import json
from prometheus_client import start_http_server, Counter, Gauge

LOG_FILE = "logs.jsonl"

# ------------------------
# LOGGING SETUP
# ------------------------
# Konfigurerer logging systemet til at skrive logbeskeder til en fil "app.log" med INFO niveau og et specifikt format.
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Opretter et logger-objekt som bruges i hele programmet til at logge beskeder. Loggeren vil skrive til "app.log" filen.
logger = logging.getLogger()

# ------------------------
# JSON LOGGING FUNCTION
# ------------------------
def log_json(level, message, extra=None):
    """Logger en besked i JSON format"""
    log_entry = {
        "time": time.asctime(),
        "level": level,
        "message": message,
        "extra": extra
    }
    print(json.dumps(log_entry))


def write_log(level, message, extra=None):
    log_entry = {
        "time": time.asctime(),
        "level": level,
        "message": message,
        "extra": extra
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# ------------------------
# LOGIN FUNCTION
# ------------------------
def login(user):
    """Logger login forsøg"""
    if user == "admin":
        logger.info(f"Admin login successful: {user}")
        log_json("INFO", "Admin login successful", {"user": user})
        write_log("INFO", "Admin login successful", {"user": user})
    else:
        logger.warning(f"Failed login attempt: {user}")
        log_json("WARNING", "Failed login attempt", {"user": user})
        write_log("WARNING", "Failed login attempt", {"user": user})

# ------------------------
# PROMETHEUS METRICS
# ------------------------
# Counter = tæller der kun stiger (antal requests) 
request_counter = Counter(
    "app_requests_total",
    "Total number of requests"
)
# Gauge = værdi der kan gå op og ned (fx CPU)
cpu_usage = Gauge(
    "fake_cpu_usage_percent",
    "Fake CPU usage percent"
)

# ------------------------
# PROGRAM START
# ------------------------

# Logger at programmet starter (skrives i app.log) og på konsollen.
logger.info("Application started")
log_json("INFO", "System started")
write_log("INFO", "System started")

write_log("WARNING", "CPU is high", {"cpu": 87})
write_log("ERROR", "Something failed")

# Starter Prometheus server på port 8000 (HTTP endpoint) hvor metrics kan tilgås. Dette gør det muligt for Prometheus at scrape metrics fra denne applikation.
start_http_server(8000)

print("Program kører...")
print("Prometheus metrics på: http://localhost:8000")

# Test login funktioner
login("admin")
login("guest")

# Uendelig loop = programmet kører konstant og simulerer aktivitet ved at opdatere metrics og logge beskeder. Dette er en simpel simulation af en applikation der håndterer requests og har CPU-aktivitet.
while True:
    try:
        # Simuler arbejde med tidtagning
        start = time.time()
        
        # Simuler aktivitet
        request_counter.inc()
        # Genererer tilfældig CPU værdi mellem 10 og 90 og opdaterer Prometheus gauge metric med denne værdi.    
        fake_cpu = random.randint(10, 90)
                # Sender CPU værdi til Prometheus gauge metric, så den kan blive scraped og overvåget.
        cpu_usage.set(fake_cpu)
        # Logger normal aktivitet (INFO) med den simulerede CPU værdi. Dette vil blive skrevet i app.log filen.
        logger.info(f"Request handled - CPU: {fake_cpu}%")

        # Hvis CPU er høj → log warning, fejl (ERROR) og hvis CPU er kritisk høj → log kritisk (CRITICAL). Disse beskeder vil også blive skrevet i app.log filen.
        if fake_cpu > 70:
            logger.warning("CPU is getting high")
            log_json("WARNING", "CPU is getting high", {"cpu": fake_cpu})
            write_log("WARNING", "CPU is getting high", {"cpu": fake_cpu})
        
        if fake_cpu > 80:
            logger.error("High CPU usage detected")
            log_json("ERROR", "High CPU usage detected", {"cpu": fake_cpu})
            write_log("ERROR", "High CPU usage detected", {"cpu": fake_cpu})
        
        # Hvis CPU er ekstrem → kritisk fejl 
        if fake_cpu > 95:
            logger.critical("SYSTEM OVERLOAD")
            log_json("CRITICAL", "SYSTEM OVERLOAD", {"cpu": fake_cpu})
            write_log("CRITICAL", "SYSTEM OVERLOAD", {"cpu": fake_cpu})
        
        # Beregn tid for task
        time.sleep(random.randint(1, 3))
        end = time.time()
        
        logger.info(f"Task completed in {end - start:.2f} seconds")
        log_json("INFO", "Task completed", {"duration": f"{end - start:.2f} seconds"})
        write_log("INFO", "Task completed", {"duration": f"{end - start:.2f} seconds"})
        
        # Pause i 5 sekunder før næste loop iteration, så vi ikke spammer logs og metrics for hurtigt. Dette simulerer en vis tid mellem requests.
        time.sleep(5)
    # Hvis der sker en uventet fejl i loopet, fanges den og logges som en fejl (ERROR) i app.log filen. Dette sikrer at eventuelle problemer bliver registreret for senere fejlfinding.
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        log_json("ERROR", "Unexpected error", {"error": str(e)})
        write_log("ERROR", "Unexpected error", {"error": str(e)})