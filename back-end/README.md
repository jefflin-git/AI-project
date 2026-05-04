# 本地開發環境設定
## 進入fastapi資料夾
```
cd back-end/fastapi
```
## 建立python venv環境
### 建立venv
```
python -m venv ./.venv
```
### 啟動venv環境
```
.\.venv\Scripts\Activate.ps1
```
## 安裝依賴
```
pip install -r requirements.txt
```
## 設定GCP key
- 在back-end/fastapi/repositories/gcp_key/下貼上從GCP下載的金鑰json檔案
- 在back-end/fastapi/common.py中修改BUCKET_NAME為你的bucket name
- 在back-end/fastapi/common.py中修改GOOGLE_APPLICATION_CREDENTIALS為你的金鑰json檔案路徑
- 在back-end/fastapi/common.py中修改GEMINI_API_KEY為你的Gemini API Key
## 運行server
```
uvicorn main:app --reload
```