# Берем нужный базовый образ
FROM python:3.8-alpine
# Копируем все файлы из текущей директории в /app контейнера
COPY ./ /app
# Устанавливаем все зависимости
RUN pip download scipy==1.3
RUN echo -e '[DEFAULT]\n\
library_dirs = /usr/lib/openblas/lib\n\
include_dirs = /usr/lib/openblas/lib\n\n\
[atlas]\n\
atlas_libs = openblas\n\
libraries = openblas\n\n\
[openblas]\n\
libraries = openblas\n\
library_dirs = /usr/lib/openblas/lib\n\
include_dirs = /usr/lib/openblas/lib'  >> site.cfg
RUN apk update && pip install -r /app/requirements.txt --no-cache-dir
# Устанавливаем приложение
RUN pip install -e /app
# Говорим контейнеру какой порт слушай
EXPOSE 8080
# Запуск нашего приложения при старте контейнера
CMD web_server

# В качестве альтернативы distutils можно просто указать что выполнить
#CMD python /app/app/ratings.py