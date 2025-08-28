import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")
S3_BUCKET  = os.getenv("S3_BUCKET")

MONGODB_URI        = os.getenv("MONGODB_URI", "")
MONGODB_DB         = os.getenv("MONGODB_DB", "pipeline_db")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "clean_data")