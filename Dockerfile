FROM python:3.12.8-slim-bullseye as builder

COPY uv.lock pyproject.toml ./

RUN python -m pip install uv==0.5.7 && \
	uv export --no-hashes --format requirements-txt > requirements.txt

FROM python:3.12.8-slim-bullseye as prod

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder requirements.txt /app

RUN apt update -y && \
	apt install -y python3-dev \
	gcc \
	musl-dev && \
	rm -rf /var/lib/apt/lists/* && \
	pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src
COPY ./scripts/run_app.sh /app/
COPY ./alembic.ini /app/
RUN chmod +x /app/run_app.sh

CMD . /app/run_app.sh
