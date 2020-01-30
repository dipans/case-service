FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN \
 apk add --no-cache bash && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "run.py"]