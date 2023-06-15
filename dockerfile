FROM python:3.10

ENV MICRO_SERVICE=/home/app/microservice

RUN mkdir -p $MICRO_SERVICE
COPY . /$MICRO_SERVICE
RUN pip install -r $MICRO_SERVICE/requirements.txt
WORKDIR $MICRO_SERVICE/VMAP_VAST

ENTRYPOINT [ "python3", "STUB.py" ]