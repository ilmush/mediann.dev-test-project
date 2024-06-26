FROM python:3.9-alpine3.16

COPY shop /shop
WORKDIR /shop
EXPOSE 8000

RUN apk add --no-cache postgresql-libs postgresql-dev build-base

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.4.2 \
    && poetry export --without-hashes --without dev,test -f requirements.txt -o requirements.txt

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password shop-user

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
