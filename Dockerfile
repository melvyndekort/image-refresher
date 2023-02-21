## Build environment
FROM python:3.10-alpine AS venv

RUN python -m venv --copies /venv

COPY requirements.txt /
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install -Ur /requirements.txt

# Runtime environment
FROM python:3.10-alpine AS runtime
COPY --from=venv /venv /venv

ENTRYPOINT ["/venv/bin/python3"]

COPY image-refresher.py /app/

WORKDIR /app
CMD ["image-refresher.py"]
