#!/usr/bin/env python

import urllib, json
import requests
import boto3
import os
import subprocess

required = ['AWS_USERNAME', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION']
for e in required:
    if not os.environ[e]:
        raise

url_suffix = "aws.amazon.com"
region_name = None
if os.environ["AWS_REGION"] == "cn-north-1":
    region_name = os.environ["AWS_REGION"]
    url_suffix = "amazonaws.cn"


client = boto3.client('sts', region_name=region_name)
# sts = boto.connect_sts()

# policy will be an intersection of the user's existing permissions
# and these
policy = """{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*"
        }
    ]
}"""
token = client.get_federation_token(Name=os.environ['AWS_USERNAME'],
                                    Policy=policy)

session_json = json.dumps({'sessionId': token["Credentials"]["AccessKeyId"],
                           'sessionKey': token["Credentials"]["SecretAccessKey"],
                           'sessionToken': token["Credentials"]["SessionToken"]})

r = requests.get('https://signin.' + url_suffix + '/federation?Action=getSigninToken&SessionType=json&Session=' +
                 urllib.quote(session_json))

sign_in_token = r.json()['SigninToken']

destination = urllib.quote('https://console.' + url_suffix)
url = ("https://signin.%s/federation?"
       "Action=login&Issuer=%s"
       "&Destination=%s"
       "&SigninToken=%s") % (url_suffix, "twadev", destination, sign_in_token)

print url
# subprocess.call(["xdg-open", url])
