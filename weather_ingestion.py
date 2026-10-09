import requests
import boto3
import json
from datetime import datetime

API_KEY = "f0e0a3469906ad6bc80a0b2af8607509"
CITIES = ["Marrakech", "Tanger", "Dakhla", "Essaouira"]

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    region_name="us-east-1"
)

for city in CITIES:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    hour_str = now.strftime("%Hh")
    
    key = f"weather_raw/city={city}/date={date_str}/data_{hour_str}.json"
    
    s3.put_object(
        Bucket="bronze",
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json"
    )
    print(f"[OK] {city} sauvegarde dans MinIO !")

print("Ingestion terminee !")