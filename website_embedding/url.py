import re
import requests
from urllib.parse import urlsplit, urljoin

class Url:
  def __init__(self, url, domain=''):
    self.url = url
    self.domain = domain
    self.parse_url()

  def __repr__(self):
    return 'Url:{}, valid_link: {}, level: {}'.format(self.url, self.is_valid_url, self.url_level)

  def __getitem__(self, key):
    return self.__dict__[key]

  def __lt__(self, other):
    return self.url_level < other.url_level

  def parse_url(self):
    result = urlsplit(self.url)  # e.g SplitResult(scheme='https', netloc='openai.com', path='/blog/chatgpt-plus/', query='', fragment='2')
    
    # check if the link is valid
    self.is_valid_url = self.is_valid(result)
    if self.is_valid_url:
      # get level of link. E.g https:/aa/bb has url_level = 2
      self.url_level = self.get_url_level(result)
      self.parent_url = self.get_parent()
   
  def is_valid(self, parse_result):
    if re.search('^\/$', self.url.strip()) or re.search(r'mailto', self.url) or re.search(r'#', self.url): 
      return False
    if parse_result.query: #return link with query e.g aa/bb?x=1
      return False 
    if len(parse_result.netloc) == 0 and len(parse_result.scheme) == 0: # e.g /abc/
      http_link = urljoin('https://'+self.domain, self.url)

      # after join link, validate if the link exists
      if not self.is_link(http_link):
        # print("status is 404 ", http_link)
        return False
      else:
        self.url = http_link
    if parse_result.netloc != self.domain:
      return False

    return True
  
  def is_link(self, url):
    # check if link is valid
    status = requests.get(url).status_code
    return status >= 200 and status < 300

  def get_url_level(self, parse_result):
    if parse_result.path == '/':
      return 1
    else:
      components = parse_result.path[1:-1].split('/') 
      # e.g bb/cc is after the domain aa/ so its level is 3

      return len(components) + 1 
  
  # if the link is aa/bb then its parent is aa, if link is aa/bb/cc then its parent is aa/bb
  def get_parent(self):
    if self.url_level == 1:
      # if self.url is the main website, its parent is itself
      return self.url  
    else:
      url_no_end_clash = self.url[:-1]
      return self.url[0: url_no_end_clash.rfind('/') + 1] # rfind get to the last clash '/'

