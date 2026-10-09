import boto3
import json
import pandas as pd
from datetime import datetime

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    region_name="us-east-1"
)

today = datetime.now().strftime("%Y-%m-%d")
errors = []

print("=" * 50)
print("   TESTS DE QUALITE DES DONNEES")
print("=" * 50)

# TEST 1 - Bronze
print("\nTEST 1 : Bronze Layer")
CITIES = ["Marrakech", "Tanger", "Dakhla", "Essaouira"]
for city in CITIES:
    prefix = f"weather_raw/city={city}/date={today}/"
    objects = s3.list_objects_v2(Bucket="bronze", Prefix=prefix)
    if objects.get("KeyCount", 0) > 0:
        print(f"  [OK] {city} - fichier present")
    else:
        print(f"  [ERREUR] {city} - fichier MANQUANT")
        errors.append(f"Bronze: fichier manquant pour {city}")

# TEST 2 - Silver
print("\nTEST 2 : Silver Layer")
try:
    key = f"weather_clean/date={today}/weather_silver.json"
    response = s3.get_object(Bucket="silver", Key=key)
    df = pd.DataFrame(json.loads(response["Body"].read()))

    required_cols = ["city", "temperature", "humidity", "weather", "event_timestamp", "ingestion_timestamp"]
    for col in required_cols:
        if col in df.columns:
            print(f"  [OK] Colonne '{col}' presente")
        else:
            print(f"  [ERREUR] Colonne '{col}' MANQUANTE")
            errors.append(f"Silver: colonne manquante {col}")

    if df["temperature"].between(-10, 50).all():
        print(f"  [OK] Temperatures valides ({df['temperature'].min():.1f}C - {df['temperature'].max():.1f}C)")
    else:
        print(f"  [ERREUR] Temperatures invalides !")
        errors.append("Silver: temperatures invalides")

    if df["humidity"].between(0, 100).all():
        print(f"  [OK] Humidite valide ({df['humidity'].min()}% - {df['humidity'].max()}%)")
    else:
        print(f"  [ERREUR] Humidite invalide !")
        errors.append("Silver: humidite invalide")

    if df.isnull().sum().sum() == 0:
        print(f"  [OK] Aucune valeur nulle")
    else:
        print(f"  [ATTENTION] Valeurs nulles detectees !")

except Exception as e:
    print(f"  [ERREUR] Silver : {e}")
    errors.append(f"Silver: {e}")

# TEST 3 - Gold
print("\nTEST 3 : Gold Layer")
try:
    key = f"weather_analytics/date={today}/weather_gold.json"
    response = s3.get_object(Bucket="gold", Key=key)
    df_gold = pd.DataFrame(json.loads(response["Body"].read()))

    if "weather_score" in df_gold.columns:
        print(f"  [OK] Score meteo present (min: {df_gold['weather_score'].min()}, max: {df_gold['weather_score'].max()})")
    else:
        print(f"  [ERREUR] Score meteo MANQUANT")
        errors.append("Gold: score meteo manquant")

    if "rank" in df_gold.columns:
        print(f"  [OK] Classement present")
    else:
        print(f"  [ERREUR] Classement MANQUANT")

    best = df_gold[df_gold["best_city"] == True]
    if len(best) == 1:
        print(f"  [OK] Meilleure ville : {best['city'].values[0]}")
    else:
        print(f"  [ERREUR] Meilleure ville non identifiee !")
        errors.append("Gold: meilleure ville manquante")

except Exception as e:
    print(f"  [ERREUR] Gold : {e}")
    errors.append(f"Gold: {e}")

# RESUME
print("\n" + "=" * 50)
if not errors:
    print("TOUS LES TESTS SONT PASSES !")
else:
    print(f"{len(errors)} ERREUR(S) DETECTEE(S) :")
    for e in errors:
        print(f"  - {e}")
print("=" * 50)