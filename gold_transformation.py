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

key = f"weather_clean/date={today}/weather_silver.json"
response = s3.get_object(Bucket="silver", Key=key)
data = json.loads(response["Body"].read())
df = pd.DataFrame(data)

print("Donnees Silver chargees !")

def calcul_score(row):
    score = 100
    if 20 <= row["temperature"] <= 30:
        score += 30
    elif 15 <= row["temperature"] < 20:
        score += 10
    else:
        score -= 10
    if row["humidity"] < 60:
        score += 20
    else:
        score -= 10
    if row["wind_speed"] < 5:
        score += 20
    elif row["wind_speed"] < 10:
        score += 10
    else:
        score -= 10
    if row["weather"] == "Clear":
        score += 30
    elif row["weather"] == "Clouds":
        score += 10
    elif row["weather"] in ["Rain", "Storm"]:
        score -= 30
    return score

df["weather_score"] = df.apply(calcul_score, axis=1)
df["rank"] = df["weather_score"].rank(ascending=False).astype(int)
df["best_city"] = df["rank"] == 1
df["date"] = today
df = df.sort_values("rank")

print("\nClassement des villes :")
print(df[["city", "temperature", "humidity", "weather", "weather_score", "rank"]].to_string(index=False))
print(f"\nMeilleure ville : {df[df['best_city']]['city'].values[0]}")

output = df.to_json(orient="records", indent=2)
gold_key = f"weather_analytics/date={today}/weather_gold.json"
s3.put_object(
    Bucket="gold",
    Key=gold_key,
    Body=output.encode("utf-8"),
    ContentType="application/json"
)

print(f"\nGold Layer cree : gold/{gold_key}")