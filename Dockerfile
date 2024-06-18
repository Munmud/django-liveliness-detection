FROM python:3.11
LABEL maintainer="munmud"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y ffmpeg libglib2.0-0 libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# RUN apk add --update --no-cache postgresql-client
# RUN apk add --update --no-cache --virtual .tmp-build-deps \
#     gcc libc-dev linux-headers postgresql-dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN pip install scikit-learn==1.5.0 pandas==2.2.2

COPY ./app /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000


# RUN apk add --no-cache build-base python3-dev g++
# RUN pip install scikit-learn
# RUN pip install numpy networkx geopy

RUN adduser --disabled-password --no-create-home app

RUN mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]
