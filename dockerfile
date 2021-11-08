FROM python:3

COPY src /src

RUN pip install python-telegram-bot
RUN pip install requests

ENV TELEGRAM_TOKEN=""
ENV ITEMS_PICKUP_AVAILABILITY="Z14W,Z14X,MK1A3LL/A,MK1H3LL/A,Z14Z,MK193LL/A"

ENTRYPOINT [ "python", "src/main.py" ]