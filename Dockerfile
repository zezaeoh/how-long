FROM python:3.8 as dev

LABEL maintainer="jaegeon <zezaeoh@gmail.com>"

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        locales rdate \
    && localedef -f UTF-8 -i ko_KR ko_KR.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG="ko_KR.UTF-8" LANGUAGE="ko_KR.UTF-8" LC_ALL="ko_KR.UTF-8" PYTHONUNBUFFERED="0" FITCLIP_ENV="development"

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN pip install uwsgi

ENTRYPOINT ["/app/bin/docker-entrypoint"]

FROM python:3.8-slim as prod

LABEL maintainer="jaegeon <zezaeoh@gmail.com>"

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        locales rdate libxml2 libmariadb3 \
    && localedef -f UTF-8 -i ko_KR ko_KR.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG="ko_KR.UTF-8" LANGUAGE="ko_KR.UTF-8" LC_ALL="ko_KR.UTF-8" PYTHONUNBUFFERED="0" \
    UWSGI_PORT="8000" UWSGI_THREAD_NUM="2" UWSGI_PROCESS_NUM="2" UWSGI_LISTEN_NUM="1024" \
    FITCLIP_ENV="production"
WORKDIR /app

COPY --from=dev /usr/local/bin /usr/local/bin
COPY --from=dev /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

COPY . .

ENTRYPOINT ["/app/bin/docker-entrypoint"]
