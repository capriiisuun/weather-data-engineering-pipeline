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

key = f"weather_analytics/date={today}/weather_gold.json"
response = s3.get_object(Bucket="gold", Key=key)
df = pd.DataFrame(json.loads(response["Body"].read()))

df.to_csv("weather_gold.csv", index=False, encoding="utf-8-sig")
print("Fichier weather_gold.csv cree !")
print(df[["city", "temperature", "humidity", "weather", "weather_score", "rank"]].to_string(index=False))