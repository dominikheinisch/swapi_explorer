FROM python:3.8

ENV APP_DIR /app
WORKDIR $APP_DIR

COPY ./requirements.txt $APP_DIR/requirements.txt
RUN pip install -r requirements.txt

COPY ./ $APP_DIR/
