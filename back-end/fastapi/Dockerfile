# 1. 使用輕量化的 Python 基礎映像檔
FROM python:3.10-slim

# 2. 設定容器內的工作目錄
WORKDIR /app

# 3. 將在地需求檔案複製到容器中
COPY requirements.txt .

# 4. 安裝依賴套件
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 5. 將應用程式程式碼複製到容器中
COPY . .

# 6. 執行 FastAPI 伺服器
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]