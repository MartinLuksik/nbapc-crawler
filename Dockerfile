FROM markadams/chromium-xvfb

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install selenium bs4 numpy pandas requests boto3 azure-storage-blob

ADD wc /wc
ADD chromedriver chromedriver

WORKDIR wc

CMD ["python3", "__main__.py", "boxscores", "2018-19", "wasb"]
