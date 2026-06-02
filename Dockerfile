FROM python:3-slim
WORKDIR /app

COPY ./ .
RUN pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["uvicorn", "api:app", "--host=0.0.0.0"]
