# Берем нужный базовый образ
FROM python:3.8.10-slim
# Копируем все файлы из текущей директории в /app контейнера
COPY ./ /app
# Устанавливаем все зависимости
RUN apt-get update
RUN apt-get -y install gcc
#RUN apt-get add make automake gcc g++ subversion python3-dev
RUN pip install -r /app/requirements.txt --no-cache-dir
# Устанавливаем приложение
RUN pip install -e /app
# Говорим контейнеру какой порт слушай
EXPOSE 8080
# Запуск нашего приложения при старте контейнера
CMD web_server

# В качестве альтернативы distutils можно просто указать что выполнить
#CMD python /app/app/ratings.py