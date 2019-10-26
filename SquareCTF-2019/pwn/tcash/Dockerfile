FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y && apt-get install -y socat

RUN useradd -ms /bin/sh tcash
WORKDIR /home/tcash

COPY ./flag.txt ./
COPY ./tcash ./
COPY ./run.sh ./

RUN chown -R root:tcash /home/tcash && \
    chmod 550 /home/tcash &&\
    chmod 550 /home/tcash/tcash && \
    chmod 550 /home/tcash/run.sh && \
    chmod 440 /home/tcash/flag.txt

EXPOSE 7852

CMD ["socat", "-T60", "TCP-LISTEN:7852,reuseaddr,fork,su=tcash", "EXEC:/home/tcash/run.sh,stderr"]
