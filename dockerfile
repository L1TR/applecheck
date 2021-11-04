FROM python:3

COPY src /src

RUN pip install bs4
RUN pip install requests

ENV TELEGRAM_TOKEN=""
ENV TELEGRAM_CHATID=""
ENV ZIP=""
ENV ITEMS_PICKUP_ELIGIBILITY="Z14W,Z14X"
ENV ITEMS_PICKUP_AVAILABILITY="Z14W,Z14X,MK1A3LL/A,MK193LL/A"

ENTRYPOINT [ "python", "src/runner.py" ]