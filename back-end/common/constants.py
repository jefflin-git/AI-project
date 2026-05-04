import os

BUCKET_NAME = os.getenv("BUCKET_NAME") # docker
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # docker

# BUCKET_NAME = "<your-bucket-name>" # local
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "gcp_key", "<your-service-account-key>.json")) # local
# GEMINI_API_KEY = "<your-gemini-api-key>" # local

PREDICTION_TABLE_FILE_NAME = "prediction_data.csv"
REPORT_TABLE_FILE_NAME = "final_expert_report.csv"
PREDICTION_MODEL_PKL_FILE_NAME = "Store_Intelligence_Model_v4.pkl"
PREDICTION_MODEL_ONNX_FILE_NAME = "store_prediction_model.onnx"
SHAP_DATABASE_FILE_NAME = "SHAP_XGB_Full_Database.pkl"

HEADERS = {
    "Content-Type": "application/json"
}