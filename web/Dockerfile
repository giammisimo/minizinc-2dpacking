FROM ubuntu:latest
RUN apt update && apt install -y python3 python3-pip

COPY ./src/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# Install only watchdog for file monitoring
RUN pip install --no-cache-dir --break-system-packages watchdog

WORKDIR /app

# Create a non-root user and set up directories with proper permissions
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    mkdir -p /app/static/cache && \
    mkdir -p /home/appuser/.config/matplotlib && \
    chown -R appuser:appuser /app && \
    chmod -R 777 /app/static/cache && \
    chown -R appuser:appuser /home/appuser

USER appuser

# Set matplotlib config directory
ENV MPLCONFIGDIR=/home/appuser/.config/matplotlib

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--debug"]
