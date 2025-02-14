FROM ubuntu:latest
RUN apt update && apt install -y python3 python3-pip

COPY ./src/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# Install only watchdog for file monitoring
RUN pip install --no-cache-dir --break-system-packages watchdog

WORKDIR /app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    mkdir -p /app/static/cache && \
    chown -R appuser:appuser /app

USER appuser

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--debug"]
