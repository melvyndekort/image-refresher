FROM python:3-slim AS build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY *.py /opt/venv/bin/


FROM python:3-alpine AS runtime

LABEL org.opencontainers.image.source http://github.com/melvyndekort/image-refresher

COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

CMD ["image-refresher.py"]
