FROM python:3

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY exporter.py /app

ENV TAPO_EXPORTER_IP_ADDRESS ""
ENV TAPO_EXPORTER_EMAIL ""
ENV TAPO_EXPORTER_PASSWORD ""
ENV TAPO_EXPORTER_POLLING_INTERVAL_SECONDS "5"
ENV TAPO_EXPORTER_PORT "9877"

EXPOSE $TAPO_EXPORTER_PORT

CMD [ "python3", "exporter.py"]
