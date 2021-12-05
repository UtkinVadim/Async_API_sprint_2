FROM python:3.9.7-slim
WORKDIR /functional

ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG USER=fastapi_tests
RUN addgroup --system ${USER} && \
    adduser --system --no-create-home --ingroup ${USER} ${USER} && \
    chown -R ${USER}:${USER} /functional
USER $USER

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENTRYPOINT ["/bin/sh", "-c", "python utils/wait_for_redis.py && python utils/wait_for_es.py && pytest src --pastebin=all"]
