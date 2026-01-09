from ua_parser import parse
import re
from packaging.version import Version

# Checking user-agent is a way good enough for regular testing, but it isn't the best way to really
# determine what the client says it is. A better way would be running JavaScript and check for
# specific code behaviors. For example, window.scrollByLines() is rather unique to Firefox and not
# other browsers. And window.launchQueue is more unique to Chrome, Edge, and Opera.
# Code behavior detection is really more necessary for exploit kids that require precision on
# target compatibility and evasion.

class UserAgent():
  def __init__(self, ua_string):
    self.ua = parse(ua_string)
    if self.ua.user_agent:
      self.agent_family = self.ua.user_agent.family
      if self.ua.user_agent.patch:
        self.agent_version = f'{self.ua.user_agent.major}.{self.ua.user_agent.minor}.{self.ua.user_agent.patch}'
      else:
        self.agent_version = f'{self.ua.user_agent.major}.{self.ua.user_agent.minor}'
      self.agent_version = Version(self.agent_version)
    else:
      self.agent_family = ''
      self.agent_version = ''

    if self.ua.os:
      self.os_family = self.ua.os.family
      if self.ua.os.patch:
        self.os_version = f'{self.ua.os.major}.{self.ua.os.minor}.{self.ua.os.patch}'
      else:
        self.os_version = f'{self.ua.os.major}.{self.ua.os.minor}'
      self.os_version = Version(self.os_version)
    else:
      self.os_family = ''
      self.os_version = ''

    if self.ua.device:
      self.device_family = self.ua.device.family
    else:
      self.device_family = ''

  def is_browser(self, name):
    return (not (re.search(name, self.agent_family, re.IGNORECASE) == None))

  def is_os(self, name):
    return (not (re.search(name, self.os_family, re.IGNORECASE) == None))

  def compare_browser_version(self, version):
    version = Version(version)
    if self.agent_version > version:
      return 1
    elif self.agent_version < version:
      return -1
    elif self.agent_version == version:
      return 0

  def compare_os_version(self, version):
    version = Version(version)
    if self.os_version > version:
      return 1
    elif self.os_version < version:
      return -1
    elif self.os_version == version:
      return 0

  def __str__(self):
    s = []
    if self.ua.user_agent:
      s.append(f'{self.agent_family} ({self.agent_version})')
    if self.ua.os:
      s.append(f'{self.os_family} ({self.os_version})')
    return '; '.join(s)
