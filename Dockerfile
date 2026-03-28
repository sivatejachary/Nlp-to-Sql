FROM python:3.10-slim

# set working directory
WORKDIR /app

# install system deps (needed for some python libs)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy requirements first (faster build)
COPY requirements.txt .

# install python packages
RUN pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . .

# Hugging Face uses port 7860
EXPOSE 7860

# run app
CMD ["sh", "-c", "python setup_database.py && python seed_memory.py || true && uvicorn main:app --host 0.0.0.0 --port 7860"]