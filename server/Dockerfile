FROM python:slim-bullseye
RUN pip install --upgrade pip
RUN adduser -D app
USER myuser
WORKDIR /home/app
COPY --chown=app:app requirements.txt requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt
ENV PATH="/home/app/.local/bin:${PATH}"
COPY --chown=app:app . .
EXPOSE 8765
CMD ["python", "server.py"]
