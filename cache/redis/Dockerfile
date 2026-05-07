# 使用官方輕量版作為基底
FROM redis:7.2-alpine

# 設定工作目錄
WORKDIR /usr/local/etc/redis

# 將本地的 redis.conf 複製到映像檔內部
COPY redis.conf .

# 建立資料存放目錄並確保權限正確
RUN mkdir -p /data && chown redis:redis /data

# 暴露埠位
EXPOSE 6379

# 啟動時讀取設定檔
# 注意：這裡不寫死密碼，改由啟動命令接收環境變數
CMD ["redis-server", "redis.conf"]