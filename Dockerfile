# syntax=docker/dockerfile:1.2

#
# BUILDER STAGE
#

FROM python:3.10 as builder
WORKDIR /assassin

# install poetry
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry==1.2.2

# install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry --no-interaction --no-ansi install

# run checks
COPY . ./
RUN poetry --no-interaction --no-ansi install \
    && poetry --no-interaction --no-ansi run ./scripts/check  

# build wheel
RUN poetry build

#
# OUTPUT STAGE
#

FROM python:3.10

# upgrade pip and install wheel from builder stage
RUN --mount=from=builder,target=mnt/dist,source=assassin/dist \
    pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir mnt/dist/assassin-*-py3-none-any.whl

# setup healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s \
  CMD curl -f http://localhost/ || exit 1

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:80", "assassin:create_app()" ]
