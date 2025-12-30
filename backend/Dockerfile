FROM python:3.12-slim

# Install system dependencies + locales (CRITICAL for Python 3.12)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Configure UTF-8 locale (CRITICAL)
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
