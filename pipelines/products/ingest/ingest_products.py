
import json
import requests
import boto3
from datetime import datetime, timezone
from botocore.config import Config

# Configuracion de la API
API_URL = "https://dummyjson.com/products?limit=0"

# Configuracion de Floci y S3
S3_ENDPOINT = "http://localhost:4566"
BUCKET = "ucv-data-platform"
DOMAIN = "products"

def main():
    print("Iniciando ingesta de productos...")

    # Consultar API
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    data = response.json()
    products = data["products"]

    print(f"Productos descargados: {len(products)}")

    # Crear cliente S3
    s3 = boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
        config=Config(s3={"addressing_style": "path"})
    )

    # Generar archivo JSON
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    key = f"{DOMAIN}/bronze/products_{timestamp}.json"

    body = json.dumps(data, ensure_ascii=False).encode("utf-8")

    # Subir a S3
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=body,
        ContentType="application/json"
    )

    print(f"Archivo guardado en s3://{BUCKET}/{key}")
    print("Ingesta completada correctamente.")

if __name__ == "__main__":
    main()
