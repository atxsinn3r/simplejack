import os
import subprocess
from base.webserver import *
from base.webserver import init as base_init
from lib.config import *

exe_pingback_src_dir = Path(os.path.join(SRC_PATH, 'exe_pingback'))
build_script = Path(os.path.join(exe_pingback_src_dir, 'build.sh'))
exe_path = Path(os.path.join(exe_pingback_src_dir, 'build', 'EXEPINGBACK'))

class Campaign(Base):
  @route('/download')
  def download(self):
    return send_file(exe_path, as_attachment=True, download_name='hello_world')

def generate_exe(url):
  result = subprocess.run([build_script, url], check=True, cwd=exe_pingback_src_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  if not os.path.exists(exe_path):
    raise RuntimeError('EXE not found')

def init(args):
  base_init(args)
  pingback_url = get_pingback_url()
  try:
    print(f'Please wait. Generating EXE with pingback: {pingback_url}')
    generate_exe(pingback_url)
  except Exception as e:
    print(f'Failed to run build script: {e}')
    return
  print('Use endpoint /download to download the executable.')
  print(f'Pingback URL: {pingback_url}')

Campaign.register(server, route_base='/')
