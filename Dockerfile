FROM markadams/chromium-xvfb

RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get clean

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

ADD wc /wc
ADD chromedriver /chromedriver

WORKDIR /wc

CMD ["python3", "-u", "__main__.py"]