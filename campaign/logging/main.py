from base.webserver import *
from lib.helper import get_timestamp
from lib.ua import UserAgent
import logging

class Campaign(Base):
  @route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
  @route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
  def index(self, path):
    query = '?{}'.format(request.query_string.decode('utf-8')) if request.query_string else ''
    remote_addr = request.headers.getlist('X-FORWARDED-FOR')[0] if request.headers.getlist('X-FORWARDED-FOR') else request.remote_addr
    print("[{}] Origin: {}".format(get_timestamp(), remote_addr))
    user_agent_str = request.headers.get('User-Agent')
    if user_agent_str:
      ua = UserAgent(user_agent_str)
      print(str(ua))
    print('')

    print("{} /{}{} {}".format(request.method, path, query, request.environ.get('SERVER_PROTOCOL')))
    for header, value in request.headers.items():
        print(f"{header}: {value}")

    body = request.get_data(as_text=True)
    if body:
      print('')
      print(request.get_data(as_text=True))
    print('')
    return "Request received!\n", 200

Campaign.register(server, route_base='/')
