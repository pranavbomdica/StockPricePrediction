# Use Python 3.10 as base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend codebase (including scripts)
COPY . .

# Ensure the models and data directories exist
RUN mkdir -p models data

# Copy all CSV data files into the container
COPY data/*.csv /app/data/

# Run training scripts for Linear Regression & Random Forest models
RUN python services/lr_model.py
RUN python services/rf_model.py
RUN python services/xgboost_model.py

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
