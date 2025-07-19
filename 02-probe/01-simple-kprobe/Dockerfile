FROM alpine:3

RUN apk add --no-cache \
    bcc-tools \
    py3-pip \
    py3-bcc \
    py3-netifaces

ADD simple_kprobe.py /root/

CMD ["python3", "/root/simple_kprobe.py"]