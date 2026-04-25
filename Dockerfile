# 使用轻量级的 Python 3.11 镜像
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 设置工作目录
WORKDIR /app

# 安装系统依赖（如果有些包需要编译）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    make \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目全量代码
COPY . .

# 默认提供系统测试指令作为容器启动检查
CMD ["make", "test"]
