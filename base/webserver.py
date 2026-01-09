from flask import Flask, render_template, request, send_file
from flask_classful import FlaskView, route
from ua_parser import parse
import logging
from lib.helper import print_message as print
from lib.ua import UserAgent
from flask.views import MethodView
from urllib.parse import urljoin
import mimetypes

server = Flask(__name__)
logging.getLogger('werkzeug').disabled = True

class Base(FlaskView):
  def get_remote_addr(self):
    remote_addr = request.headers.getlist('X-FORWARDED-FOR')[0] if request.headers.getlist('X-FORWARDED-FOR') else request.remote_addr
    return remote_addr

  @route('/')
  def index(self):
    return 'OK\n'

  @route('/ping')
  def pingback(self):
    return 'OK\n'

def get_pingback_url():
  return urljoin(server.config['pingback'], 'ping')

def init(args):
  server.config['lhost'] = args.lhost
  server.config['lport'] = args.lport
  server.config['pingback'] = args.pingback
  server.config['ssl_context'] = args.ssl_context

def start(args):
  print(f'Running server on http://{args.lhost}:{args.lport}/')
  server.run(debug=True, use_reloader=False, host=args.lhost, port=args.lport)
