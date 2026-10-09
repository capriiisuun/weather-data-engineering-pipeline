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

CITIES = ["Marrakech", "Tanger", "Dakhla", "Essaouira"]
today = datetime.now().strftime("%Y-%m-%d")
records = []

for city in CITIES:
    prefix = f"weather_raw/city={city}/date={today}/"
    
    try:
        objects = s3.list_objects_v2(Bucket="bronze", Prefix=prefix)
        
        for obj in objects.get("Contents", []):
            response = s3.get_object(Bucket="bronze", Key=obj["Key"])
            raw = json.loads(response["Body"].read())
            
            record = {
                "city": raw.get("name", city),
                "country": raw.get("sys", {}).get("country", "MA"),
                "latitude": raw.get("coord", {}).get("lat"),
                "longitude": raw.get("coord", {}).get("lon"),
                "temperature": float(raw.get("main", {}).get("temp", 0)),
                "temp_min": float(raw.get("main", {}).get("temp_min", 0)),
                "temp_max": float(raw.get("main", {}).get("temp_max", 0)),
                "feels_like": float(raw.get("main", {}).get("feels_like", 0)),
                "humidity": int(raw.get("main", {}).get("humidity", 0)),
                "pressure": int(raw.get("main", {}).get("pressure", 0)),
                "weather": raw.get("weather", [{}])[0].get("main", ""),
                "weather_description": raw.get("weather", [{}])[0].get("description", ""),
                "wind_speed": float(raw.get("wind", {}).get("speed", 0)),
                "wind_direction": int(raw.get("wind", {}).get("deg", 0)),
                "event_timestamp": datetime.fromtimestamp(raw.get("dt", 0)).isoformat(),
                "ingestion_timestamp": datetime.now().isoformat()
            }
            
            record = {k: v for k, v in record.items() if v is not None}
            records.append(record)
            print(f"[OK] {city} transforme !")
    
    except Exception as e:
        print(f"[ERREUR] {city}: {e}")

if records:
    df = pd.DataFrame(records)
    output = df.to_json(orient="records", indent=2)
    
    key = f"weather_clean/date={today}/weather_silver.json"
    s3.put_object(
        Bucket="silver",
        Key=key,
        Body=output.encode("utf-8"),
        ContentType="application/json"
    )
    print(f"Silver Layer cree : silver/{key}")
    print(df[["city", "temperature", "humidity", "weather"]].to_string(index=False))
else:
    print("Aucune donnee trouvee dans le Bronze Layer !")