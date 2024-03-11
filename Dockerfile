FROM nfqlt/chromedriver:latest

ENV pop_server="outlook.office365.com"
ENV pop_port=995
ENV pop_email_address="pop_email_address"
ENV pop_email_password="pop_email_password"
ENV jrecin_address="jrecin_address"
ENV jrecin_password="jrecin_password"

LABEL maintainer="MGMCN"

USER root

COPY . /APP

WORKDIR /APP

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --break-system-packages -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT python3 main.py --pop_server $pop_server \
                           --pop_port $pop_port \
                           --pop_email_address $pop_email_address \
                           --pop_email_password $pop_email_password \
                           --jrecin_address $jrecin_address \
                           --jrecin_password $jrecin_password
