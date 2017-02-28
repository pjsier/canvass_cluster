# Canvass Clustering Tool

[Link to running demo](https://ujoizgdwq9.execute-api.us-east-1.amazonaws.com/dev)

Proof of concept in applying a potential voter file API to a simple application
for creating canvassing groups out of a list of individual households. Using the
Zappa framework for deploying on AWS Lambdas and API Gateway.

## Running Locally

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python runserver.py
```

## Deploying to AWS

Make sure you have credentials for AWS configured with the AWS CLI, then change
the name of the S3 bucket in `zappa_settings.json` and run:

```
zappa deploy dev
```
