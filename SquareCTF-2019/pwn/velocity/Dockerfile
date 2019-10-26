FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y && apt-get install -y socat

RUN useradd -ms /bin/sh wwhv
WORKDIR /home/wwhv

COPY ./flag.txt ./
COPY ./worldwide_highest_velocity ./
COPY ./run.sh ./

RUN chown -R root:wwhv /home/wwhv && \
    chmod 550 /home/wwhv && \
    chmod 550 /home/wwhv/worldwide_highest_velocity && \
    chmod 550 /home/wwhv/run.sh && \
    chmod 440 /home/wwhv/flag.txt

EXPOSE 6129

CMD ["socat", "-T60", "TCP-LISTEN:6129,reuseaddr,fork,su=wwhv", "EXEC:/home/wwhv/run.sh,stderr"]
