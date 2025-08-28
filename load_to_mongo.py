import io
import boto3
import pandas as pd
from pymongo import MongoClient
from config import S3_BUCKET, AWS_REGION, MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION

def _get_latest_processed_key(s3):
    # List all objects inside processed/
    resp = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix="processed/")
    contents = resp.get("Contents", [])
    if not contents:
        raise SystemExit("No processed files found in S3. Run transform.py first.")
    latest = max(contents, key=lambda x: x["LastModified"])
    return latest["Key"]

def run():
    if not MONGODB_URI:
        print("MONGODB_URI not set in .env. Skipping Mongo load.")
        return

    # connect to S3
    s3 = boto3.client("s3", region_name=AWS_REGION)

    # get latest processed file
    key = _get_latest_processed_key(s3)
    print(f"Loading from s3://{S3_BUCKET}/{key}")

    # download CSV into a DataFrame
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))

    # connect to MongoDB
    client = MongoClient(MONGODB_URI)
    coll = client[MONGODB_DB][MONGODB_COLLECTION]

    # insert
    if not df.empty:
        coll.insert_many(df.to_dict(orient="records"))
        print(f"Inserted {len(df)} documents into {MONGODB_DB}.{MONGODB_COLLECTION}")
    else:
        print("DataFrame is empty. Nothing to insert.")

if __name__ == "__main__":
    run()