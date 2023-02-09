from url import Url
from itertools import groupby

class Url_Dict:
  def __init__(self, domain, url_dict = {}):
    self.domain = domain
    self.url_dict = url_dict
    
  # take a list of urls and parse to dictionary by level
  def parse_list(self, urls):
    # turn list of urls to list of url object
    urlObjs = [Url(u, self.domain) for u in urls]

    # filter 
    urlObjs = list(filter(lambda x: x.is_valid_url, urlObjs))

    # # # sort by link level
    new_urlObjs = sorted(urlObjs, key = lambda x : x.url_level)
    self.print(new_urlObjs)
    self.organize_url_list(new_urlObjs)

  # organize links into a dictionary by level
  # e.g {aa: {aa/bb, aa/cc: {aa/cc/dd, aa/cc/ab}}}
  def print(self, urlObjs):
    for u in urlObjs:
      print(u)
  def organize_url_list(self, urlObjs):
    first_level_key = ''
    for keys, group in groupby(urlObjs, key=lambda x: (x.url_level,x.parent_url)):
      if keys[0] == 2:
        self.url_dict[keys[1]] = {k.url: None for k in list(group)}
        first_level_key = keys[1]
      if keys[0] == 3:
        self.url_dict[first_level_key][keys[1]] = {k.url: None for k in list(group)}
