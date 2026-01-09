from base.webserver import *
from base.webserver import init as base_init
import qrcode
import io
from PIL import Image

class Campaign(Base):
  @route('/qr_code')
  def get_qr_code(self):
    qr_code = io.BytesIO(server.config.get('qr_code'))
    return send_file(qr_code, mimetype='image/png', download_name='qr.png', as_attachment=False)

def init(args):
  base_init(args)
  pingback_url = get_pingback_url()
  print(f'Generating QR code with pingback: {pingback_url}')
  img = qrcode.make(pingback_url)
  buf = io.BytesIO()
  img.save(buf, format='PNG')
  buf.seek(0)
  server.config['qr_code'] = buf.getvalue()

Campaign.register(server, route_base='/')
