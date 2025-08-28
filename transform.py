import io
import boto3
import pandas as pd
from config import S3_BUCKET, AWS_REGION

def _get_latest_raw_key(s3):
    # List all objects inside raw/
    resp = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix="raw/")
    contents = resp.get("Contents", [])
    if not contents:
        raise SystemExit("No raw files found in S3.")
    # Find the latest uploaded file by LastModified
    latest = max(contents, key=lambda x: x["LastModified"])
    return latest["Key"]

def run():
    s3 = boto3.client("s3", region_name=AWS_REGION)

    # Get latest raw file
    raw_key = _get_latest_raw_key(s3)
    print(f"Using latest raw file: {raw_key}")

    # Download CSV
    obj = s3.get_object(Bucket=S3_BUCKET, Key=raw_key)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))

    # Clean data (remove rows with missing values)
    df_clean = df.dropna()

    # Save back to processed folder
    out_key = raw_key.replace("raw/", "processed/").replace(".csv", "_clean.csv")
    s3.put_object(Bucket=S3_BUCKET, Key=out_key, Body=df_clean.to_csv(index=False).encode())
    print(f"Saved cleaned data to: s3://{S3_BUCKET}/{out_key}")

if __name__ == "__main__":
    run()