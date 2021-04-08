import requests
from bs4 import BeautifulSoup


def parsing_html(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  results = soup.find("table", {"class":"table"})
  tbody = results.find("tbody")
  tr = tbody.find_all("tr")
  return tr

def parsing_tag(tag):
  blank = []
  count = 0
  for text in tag:
    temp = []
    for td in tag[count]:
      if td.string is None:
        temp.append(td.string)
      else:
        temp.append(td.string.strip('\n'))
    temp = filter(None, temp)
    blank.append(list(temp))
    count += 1
  return blank

def print_list(target):
  count = 1
  for text in target:
    print(f"# {count} {target[count-1][0].title()}")
    count += 1
