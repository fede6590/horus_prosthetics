FROM python:3.11-slim-bookworm
 
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

WORKDIR /app

COPY requirements.txt .
COPY app.py .
COPY image_processing.py .
COPY pose_landmarker_lite.task .
 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
