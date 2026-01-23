from base.webserver import *
from werkzeug.utils import secure_filename

class Campaign(Base):
  def __init__(self):
    super().__init__('exfil')

  @route('/upload', methods=['POST'])
  def index(self):
    if 'file' in request.files:
      f = request.files['file']
      fname = secure_filename(f.filename)
      f.save(os.path.join(self.root_dir, fname))
      print(f'self.get_remote_addr() : Saved file as {fname}')
    return 'OK\n'

Campaign.register(server, route_base='/')