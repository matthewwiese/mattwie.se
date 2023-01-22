FROM python:slim-bullseye
RUN adduser --system --no-create-home app
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
USER app
CMD ["python", "server.py"]
EXPOSE 8765