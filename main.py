from ingest import run as ingest_run
from transform import run as transform_run
from load_to_mongo import run as load_run

if __name__ == "__main__":
    print("🚀 Pipeline started...")

    print("📥 Step 1: Ingest")
    ingest_run()

    print("🔄 Step 2: Transform")
    transform_run()

    print("📤 Step 3: Load to MongoDB")
    load_run()

    print("✅ Pipeline finished successfully.")