FROM python:slim-bullseye
RUN adduser --system --no-create-home app
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
USER app
EXPOSE 8765
CMD ["python", "-u", "server.py"]