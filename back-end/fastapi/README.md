# 本地開發環境設定
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
## 運行server
```
uvicorn main:app --reload
```