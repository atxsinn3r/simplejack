import json
import os
from lib.campaign import Campaign
from pathlib import Path
from datetime import datetime
from lib.config import *
import uuid

def get_campaign_info():
  campaigns = []
  files = list(CAMPAIGN_PATH.rglob('config.json'))
  for f in files:
    try:
      with open(f, 'r', encoding='utf-8') as config:
        data = json.load(config)
        campaign = Campaign()
        campaign.key = str(f).split('/')[-2]
        campaign.name = data['name']
        campaign.description = data['description']
        campaigns.append(campaign)
    except json.JSONDecodeError as e:
      pass
  return campaigns

def get_timestamp():
  return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_uuid():
  unique_id = uuid.uuid4()
  return (str(unique_id))

def print_message(msg):
  print(f' * [{get_timestamp()}] {msg}')
