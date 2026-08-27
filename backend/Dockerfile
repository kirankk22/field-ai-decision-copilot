FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY llm ./llm

COPY data/knowledge_base ./data/knowledge_base

COPY start.sh ./start.sh

RUN chmod +x ./start.sh \
    && mkdir -p ./data/vectorstore

EXPOSE 8000

CMD ["./start.sh"]
