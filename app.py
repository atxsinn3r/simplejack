#!/usr/bin/env python

import sys
import argparse
import importlib
from lib.helper import get_campaign_info

def start_campaign(campaign_choice, args):
  campaign = importlib.import_module(f"campaign.{campaign_choice}.main")
  for fn in ("init", "start"):
    if not hasattr(campaign, fn):
      raise AttributeError(f"{campaign_choice} is missing {fn}()")
  campaign.init(args)
  campaign.start(args)

def main(args):
  campaign_names = [campaign.key for campaign in get_campaign_info()]
  if len(campaign_names) == 0:
    print('No campaign ready')
    sys.exit(0)

  parser = argparse.ArgumentParser(description='A browser attack tool')
  parser.add_argument('-c', '--campaign', type=str, choices=campaign_names, help='Choose a campaign')
  parser.add_argument('--lhost', type=str, default='0.0.0.0', help='Optional: Web server host binding')
  parser.add_argument('--lport', type=str, default='8181', help='Optional: Web server port')
  parser.add_argument('--pingback', type=str, default='http://127.0.0.1:8181/', help='Optional: Server the campaign can ping back to')
  parser.add_argument('--ssl_context', type=str, choices=['None', 'adhoc', 'custom'], help='Optional: SSL context')
  args = parser.parse_args()
  campaign_choice = args.campaign
  start_campaign(campaign_choice, args)

if __name__ == '__main__':
  main(sys.argv)
