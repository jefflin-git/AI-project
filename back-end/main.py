import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.client import client_manager
from application.services.geo import GeoService
from infrastructure.repositories.geo_from_bigquery import GeoRepository
from application.services.brand import BrandService
from infrastructure.repositories.brand_from_bigquery import BrandRepository
from application.services.prediction import PredictionService
from infrastructure.repositories.gcs import GCSRepository
from infrastructure.repositories.prediction_from_file import PredictionRepository
from domain.services.generative_ai import GenerativeAIService
from infrastructure.services.gemini import GeminiService
from log import Logger
from common.constants import BUCKET_NAME, PREDICTION_MODEL_PKL_FILE_NAME, SHAP_DATABASE_FILE_NAME, PREDICTION_TABLE_FILE_NAME, REPORT_TABLE_FILE_NAME

logger = Logger(__name__)

DATA_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "infrastructure", "repositories", "datas"))
MODEL_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "infrastructure", "repositories", "models"))

prediction_model_path = os.path.abspath(os.path.join(MODEL_FOLDER, f"{PREDICTION_MODEL_PKL_FILE_NAME}"))
shap_database_path = os.path.abspath(os.path.join(MODEL_FOLDER, f"{SHAP_DATABASE_FILE_NAME}"))
prediction_table_path = os.path.abspath(os.path.join(DATA_FOLDER, f"{PREDICTION_TABLE_FILE_NAME}"))
report_table_path = os.path.abspath(os.path.join(DATA_FOLDER, f"{REPORT_TABLE_FILE_NAME}"))

gcs_repository = None
geo_repository = None
geo_service = None
brand_repository = None
brand_service = None
gemini_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時初始化所有基礎設施連線
    global gcs_repository, geo_repository, geo_service, brand_repository, brand_service, gemini_service
    client_manager.init_clients()
    gcs_repository = GCSRepository()
    # 啟動時執行：建立資料和模型資料夾
    if not os.path.exists(DATA_FOLDER):
        logger.debug("建立資料資料夾")
        os.makedirs(DATA_FOLDER)
    if not os.path.exists(MODEL_FOLDER):
        logger.debug("建立模型資料夾")
        os.makedirs(MODEL_FOLDER)
    # 啟動時執行：下載資料表檔案
    if not os.path.exists(prediction_table_path):
        logger.debug(f"下載 {PREDICTION_TABLE_FILE_NAME} 到 {prediction_table_path}")
        gcs_repository.download_file(BUCKET_NAME, PREDICTION_TABLE_FILE_NAME, prediction_table_path)
    if not os.path.exists(report_table_path):
        logger.debug(f"下載 {REPORT_TABLE_FILE_NAME} 到 {report_table_path}")
        gcs_repository.download_file(BUCKET_NAME, REPORT_TABLE_FILE_NAME, report_table_path)
    # 啟動時執行：下載並載入模型
    if not os.path.exists(prediction_model_path):
        logger.debug(f"下載 {PREDICTION_MODEL_PKL_FILE_NAME} 到 {prediction_model_path}")
        gcs_repository.download_file(BUCKET_NAME, PREDICTION_MODEL_PKL_FILE_NAME, prediction_model_path)
    if not os.path.exists(shap_database_path):
        logger.debug(f"下載 {SHAP_DATABASE_FILE_NAME} 到 {shap_database_path}")
        gcs_repository.download_file(BUCKET_NAME, SHAP_DATABASE_FILE_NAME, shap_database_path)
    # 初始化 repository 和 service
    gemini_service = GeminiService()
    geo_repository = GeoRepository()
    geo_service = GeoService(geo_repository)
    brand_repository = BrandRepository()
    brand_service = BrandService(brand_repository)
    yield
    # 關閉時執行
    client_manager.close_clients()
    # 關閉時執行（選填）
    if os.path.exists(prediction_table_path):
        os.remove(prediction_table_path)
    if os.path.exists(report_table_path):
        os.remove(report_table_path)
    if os.path.exists(prediction_model_path):
        os.remove(prediction_model_path)
    if os.path.exists(shap_database_path):
        os.remove(shap_database_path)
    logger.info("應用程式正在關閉...")

app = FastAPI(lifespan=lifespan)
uri_prefix = "/api"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get(uri_prefix + "/cities")
async def get_city_list():
    return geo_service.get_city_list()

@app.get(uri_prefix + "/districts/{city}")
async def get_district_list(city: str):
    return geo_service.get_district_list(city)

@app.get(uri_prefix + "/neighborhoods/{city}/{district}")
async def get_neighborhood_list(city: str, district: str):
    return geo_service.get_neighborhood_list(city, district)

@app.get(uri_prefix + "/brands")
async def get_brand_list():
    return brand_service.get_brand_list()

@app.get(uri_prefix + "/geo-check/{city}/{district}/{neighborhood}")
async def check_valid_geo(city: str, district: str, neighborhood: str):
    return {"is_valid": geo_service.check_valid_geo(city, district, neighborhood)}

@app.get(uri_prefix + "/run-prediction/{city}/{district}/{neighborhood}/{brand}")
async def run_prediction(city: str, district: str, neighborhood: str, brand: str):
    brand_type = 1 if brand == "便利商店" else 0
    prediction = PredictionService(PredictionRepository(), GenerativeAIService(gemini_service)).run_prediction(city, district, neighborhood, brand_type)
    return {
        "operation": {
            "score": prediction.operation.score,
            "report": prediction.operation.report,
        },
        "totalPopulation": {
            "neighborhood": prediction.total_population.neighborhood,
            "district": prediction.total_population.district,
        },
        "medianIncome": {
            "neighborhood": prediction.median_income.neighborhood,
            "district": prediction.median_income.district,
        },
        "competitorCount": prediction.competitor_count,
        "aiInsight": prediction.ai_insight,
        "radar": {
            "labels": prediction.radar.labels,
            "values": prediction.radar.values,
        },
        "isSuccess": prediction.is_success
    }

