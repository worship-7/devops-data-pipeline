import time
import pandas as pd
import boto3
from config import S3_BUCKET, AWS_REGION

def run():
    # sample data (pretend this is coming from API)
    df = pd.DataFrame({
        "id": [1, 2, 3, 4],
        "name": ["A", "B", None, "D"],
        "amount": [10.5, 20.0, 15.2, None]
    })

    # save to CSV
    file_name = f"data_{int(time.time())}.csv"
    df.to_csv(file_name, index=False)

    # upload to S3
    s3 = boto3.client("s3", region_name=AWS_REGION)
    s3.upload_file(file_name, S3_BUCKET, f"raw/{file_name}")

    print(f"✅ Ingest complete: {file_name} uploaded to S3 bucket {S3_BUCKET}/raw/")

if __name__ == "__main__":
    run()