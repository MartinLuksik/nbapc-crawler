FROM markadams/chromium-xvfb

ARG key
ARG secret
ARG region

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apt-get update \
    && apt-get install -y python3-pip \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apt-get clean

ADD wc /wc
ADD chromedriver /chromedriver

WORKDIR /wc

## configure aws cli
RUN aws configure set aws_access_key_id $key \
  && aws configure set aws_secret_access_key $secret \
  && aws configure set default.region $region

CMD ["python3", "-u", "__main__.py"]