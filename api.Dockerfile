FROM api_2025:1.0
RUN pip install fastapi
RUN pip install uvicorn[standart]

COPY ./src /app/src
COPY ./main.py /app/main.py
COPY ./data /app/data

CMD ["python", "main.py"]