import os

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID") # docker
BUCKET_NAME = os.getenv("BUCKET_NAME") # docker
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # docker
REDIS_HOST = os.getenv("REDIS_HOST") # docker
REDIS_PORT = os.getenv("REDIS_PORT") # docker
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") # docker

# GCP_PROJECT_ID = "your-gcp-project-id" # local
# BUCKET_NAME = "<your-bucket-name>" # local
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "gcp_key", "<your-service-account-key>.json")) # local
# GEMINI_API_KEY = "<your-gemini-api-key>" # local
# REDIS_HOST = "localhost" # local
# REDIS_PORT = 6379 # local
# REDIS_PASSWORD = "<your_strong_password>" # local

PREDICTION_TABLE_FILE_NAME = "prediction_data.csv"
REPORT_TABLE_FILE_NAME = "final_expert_report.csv"
PREDICTION_MODEL_PKL_FILE_NAME = "Store_Intelligence_Model_v4.pkl"
PREDICTION_MODEL_ONNX_FILE_NAME = "store_prediction_model.onnx"
SHAP_DATABASE_FILE_NAME = "SHAP_XGB_Full_Database.pkl"

HEADERS = {
    "Content-Type": "application/json"
}