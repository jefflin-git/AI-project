import os

BUCKET_NAME = os.getenv("BUCKET_NAME")
TRAIN_TABLE_FILE_NAME = "train_data_v1.1.csv"
VALIDATION_TABLE_FILE_NAME = "test_data_v1.1.csv"
PREDICTION_TABLE_FILE_NAME = "prediction_data.csv"
REPORT_TABLE_FILE_NAME = "final_expert_report.csv"
PREDICTION_MODEL_FILE_NAME = "Store_Intelligence_Model_v4.pkl"
SHAP_DATABASE_FILE_NAME = "SHAP_XGB_Full_Database.pkl"