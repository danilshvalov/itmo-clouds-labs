# Лабораторная работа №2

## Обязательное задание

### Введение

В данной лабораторной работе необходимо написать два Dockefile: плохой, который соответствует плохим практикам, и хороший, в котором плохие практики были исправлены. Для демонстрации работы контейнеров используются приложения из первой лабораторной работы (скрипты на Python, реализующие бэкенд и фронтенд).

### Плохие практики при написании Dockerfile

При написании Dockerfile выделяют следующие плохие практики:

1. Использовать базовые образы с тегом `latest`. Базовые образы время от времени обновляются. Зачастую обновления могут содержать обратно несовместимые изменение. Неявное обновление на новую версию базового образа может привести в лучшем случае к проблемам при сборке образа, а в худшем — ошибки в работе, которых ранее не было.
2. Использовать базовый образ, который содержит большое количество ненужного ПО. Если есть образ, который более точно подходит под заданные требования, то следует использовать специализированный образ вместо общего. Например, для приложения на Python следует выбрать образ `python`, а не `ubuntu`. Наличие лишнего ПО увеличивает размер образа, а также повышает шанс наличия уязвимостей.
3. Устанавливать пакеты, которые не требуется для работы контейнера. Таковыми могут быть различные утилиты, которые используются в повседневной жизни (например, текстовые редакторы, ssh и прочее). Установка лишних пакетов приводит к увеличению сложности Dockerfile, количества зависимостей, размера и времени сборки образа.
4. Использовать образ для решения нескольких задач. В одном контейнере следует запускать один процесс. Если необходимо запускать несколько процессов, то вероятнее всего необходимо их разделить на разные образы (например, бэкенд и фронтенд). Такой подход позволяет упростить горизонтальное масштабирование и переиспользование образов.
5. Запускать процессы от рута. Процессы, если такое возможно, следует запускать от имени пользователя, отличного от рута. Запуск процессов из-под рута может повлечь за собой возможные проблемы с безопасностью.

Далее приведен пример плохого Dockerfile:

```dockerfile
FROM ubuntu:latest

WORKDIR /app
COPY ./ /app

RUN apt-get update && apt-get -y install python3 ssh vim

CMD ["/app/start.sh"]
```

В нем используется неподходящий базовый образ `ubuntu`, хотя хватило бы и образа `python`. Также используется тег `latest`, вместо конкретной версии. Кроме этого, в образ устанавливаются лишние пакеты (`vim` и `ssh`), которые не требуются для работы приложения в контейнере. И самое главное: в контейнере с помощью скрипта `start.sh` запускаются два процесса (бэкенд и фронтенд), несмотря на то, что это два отдельных приложения, которые стоит запускать в разных контейнерах (исходный код скрипта находится [здесь](dockerfile/bad/start.sh)). В добавок ко всему, все процессы запускаются из-под рута.

Исправив эти недостатки, получим следующий Dockerfile:

```dockerfile
FROM python:3.12.6

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY ./ /home/appuser

CMD ["python3", "server.py"]
```

В нем используется наиболее подходящий базовый образ, указана конкретная версия, не устанавливаются лишние пакеты, контейнер используется только для одного приложения (в данном случае для фронтенда), а также процесс запускается пользователем, отличным от рута.

### Плохие практики при работе с контейнерами

При работе с контейнерами выделяют следующие плохие практики:

1. Открывать ненужные порты (например, с помощью флага `-P`). Каждый открытый порт является потенциальной дырой в безопасности. Поэтому стоит оставлять только те порты, которые используются приложениями.
2. Хранить важные данные в контейнере. В любой момент времени контейнер может быть остановлен и удален. В таком случае все данные, хранимые в контейнере, будут безвозвратно удалены. Чтобы такого не произошло, важные данные, которые должны сохраниться в случае удаления контейнера, необходимо хранить томах хранения данных (volumes).
3. Запускать контейнеры от рута (например, с помощью флага `--user=root`). Запуск контейнеров из-под рута может повлечь за собой возможные проблемы с безопасностью.

## Задание со звездочкой

### Плохие практики при написании docker-compose

При написании docker-compose выделяют следующие плохие практики:

1. Не прописывать зависимости между зависимыми контейнерами. Если один контейнер зависит от другого и должен быть запущен после другого (например, сервис и база данных), то необходимо выражать зависимость с помощью `depends_on`.

### Раздельные сети для контейнеров

Для того, чтобы контейнеры не видели друг друга в сети, необходимо для каждого контейнера задать собственную изолированную сеть. Для этого необходимо сделать следующее:

1. В разделе `networks` 