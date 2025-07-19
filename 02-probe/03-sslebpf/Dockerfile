FROM alpine:3

RUN apk add --no-cache \
    bcc-tools \
    py3-pip \
    py3-bcc \
    py3-netifaces

ADD sslebpf.py /root/

CMD ["python3", "/root/sslebpf.py"]