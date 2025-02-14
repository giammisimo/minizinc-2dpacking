FROM ubuntu:latest
RUN apt update && apt install -y python3 python3-pip

COPY ./src/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# Install only watchdog for file monitoring
RUN pip install --no-cache-dir --break-system-packages watchdog

COPY ./src /app
WORKDIR /app

# Create cache directory with correct permissions
RUN mkdir -p /app/static/cache && \
    chown -R nobody:nogroup /app/static/cache

USER nobody
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--debug"]
