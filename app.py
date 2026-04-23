import logging
import time
import random
from prometheus_client import start_http_server, Counter, Gauge

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

# Starter Prometheus server på port 8000 (HTTP endpoint) hvor metrics kan tilgås. Dette gør det muligt for Prometheus at scrape metrics fra denne applikation.
start_http_server(8000)

print("Program kører...")
print("Prometheus metrics på: http://localhost:8000")

# Uendelig loop = programmet kører konstant og simulerer aktivitet ved at opdatere metrics og logge beskeder. Dette er en simpel simulation af en applikation der håndterer requests og har CPU-aktivitet.
while True:
    try:
        # Simuler aktivitet
        request_counter.inc()
        # Genererer tilfældig CPU værdi mellem 10 og 90 og opdaterer Prometheus gauge metric med denne værdi.    
        fake_cpu = random.randint(10, 90)
                # Sender CPU værdi til Prometheus gauge metric, så den kan blive scraped og overvåget.
        cpu_usage.set(fake_cpu)
        # Logger normal aktivitet (INFO) med den simulerede CPU værdi. Dette vil blive skrevet i app.log filen.
        logger.info(f"Request handled - CPU: {fake_cpu}%")

        # Hvis CPU er høj → log fejl (ERROR) og hvis CPU er kritisk høj → log kritisk (CRITICAL). Disse beskeder vil også blive skrevet i app.log filen.
        if fake_cpu > 80:
            logger.error("High CPU usage detected")
        # Hvis CPU er ekstrem → kritisk fejl 
        if fake_cpu > 95:
            logger.critical("CRITICAL CPU overload!")
        # Pause i 5 sekunder før næste loop iteration, så vi ikke spammer logs og metrics for hurtigt. Dette simulerer en vis tid mellem requests.
        time.sleep(5)
    # Hvis der sker en uventet fejl i loopet, fanges den og logges som en fejl (ERROR) i app.log filen. Dette sikrer at eventuelle problemer bliver registreret for senere fejlfinding.
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")