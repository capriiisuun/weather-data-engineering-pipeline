import os
import subprocess
import sys
from datetime import datetime
import time

def run_task(name, script):
    print("\n" + "="*50)
    print(f"Tache : {name}")
    print(f"Debut : {datetime.now().strftime('%H:%M:%S')}")
    print("="*50)
    
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        encoding="utf-8",
        errors="replace"
    )
    
    if result.returncode == 0:
        print(result.stdout)
        print(f"[SUCCES] {name}")
    else:
        print(result.stderr)
        print(f"[ECHEC] {name}")
        sys.exit(1)
    
    return True

print("\n" + "="*50)
print("   DAG PIPELINE METEO - AIRFLOW SIMULATION")
print(f"   Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   Frequence : Quotidienne a 6h00")
print("="*50)

run_task("1. Ingestion Bronze", "weather_ingestion.py")
time.sleep(2)
run_task("2. Transformation Silver", "silver_transformation.py")
time.sleep(2)
run_task("3. Enrichissement Gold", "gold_transformation.py")
time.sleep(2)
run_task("4. Tests Qualite", "quality_checks.py")

print("\n" + "="*50)
print("PIPELINE COMPLET EXECUTE AVEC SUCCES !")
print(f"Fin : {datetime.now().strftime('%H:%M:%S')}")
print("="*50)