FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk xauth ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
ENV DISPLAY=:0
ENTRYPOINT ["python"]
CMD ["/app/bin/gramified_gui.py"]
