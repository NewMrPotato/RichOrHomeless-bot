FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install poetry && \
    if [ -f pyproject.toml ]; then poetry export -f requirements.txt --without-hashes -o /tmp/requirements.txt || true; fi && \
    pip install -r /tmp/requirements.txt || pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "bot.__main__"]