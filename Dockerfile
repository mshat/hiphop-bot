FROM python:alpine

WORKDIR /usr/src/bot
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# зависимости для Postgres
# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./setup.py .
RUN pip install -e .

COPY . .
COPY ./hiphop_bot/env .

ENTRYPOINT ["python3", "hiphop_bot/telegram_interface/telegram_view.py"]