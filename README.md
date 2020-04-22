# nbapc-crawler
This repository consists of a dockerized python program, which crawls data from nba.com.

[![Build status](https://dev.azure.com/martinluksik/nbapc/_apis/build/status/nbapc-crawler%20-%20Build%20Docker%20Image)](https://dev.azure.com/martinluksik/nbapc/_build/latest?definitionId=2)


# Docker build

Provide s3 credentials to setup aws cli during the build time.
```bash
docker build -t <repo:tag> --build-arg key=<aws-key> --build-arg secret=<aws-secret> --build-arg region=<aws-region> .
```

# Run application

```bash
# Save data to local file system
docker run -t -e table=boxscores -e season=2008-09 -e filesystem=local -v <path>:/wc/data <repo:tag>

# Save to Azure Storage Account
docker run -t -e table=boxscores -e season=2008-09 -e filesystem=wasb -e wasbaccountname=<SAname> -e containername=<containername> -e wasbaccountkey=<SAkey> <repo:tag>

# Save to S3
docker run -t -e table=boxscores -e season=2019-20 -e filesystem=s3 -e s3bucket=nbapc <repo:tag>
```
