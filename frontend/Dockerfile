FROM python:3.11-slim

WORKDIR /app

COPY frontend /app/frontend

RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -r /app/frontend/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "frontend/🏠_Home_page.py", "--server.address=0.0.0.0", "--server.port=8501"]