FROM python:3.7-slim

RUN apt-get -qq update && apt-get -qq >/dev/null install \
  gcc make autoconf libtool curl procps \
  && rm -rf /var/lib/apt/lists/* \
  && python -m pip install pipenv

RUN mkdir -p /app

ENV PYTHONPATH=/app

WORKDIR ${PYTHONPATH}

COPY . ./
RUN rm -rf ./.idea

RUN pipenv install --system --deploy

ENTRYPOINT ["python", "server.py"]
