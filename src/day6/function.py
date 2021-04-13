import requests
from bs4 import BeautifulSoup

def parsing_country_code():
  url = "https://www.iban.com/currency-codes"
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  results = soup.find("table", {"class":"table"})
  tbody = results.find("tbody")
  tr = tbody.find_all("tr")
  return tr

def parsing_exchange_rate(first_code, second_code, target):
  url = f"https://transferwise.com/gb/currency-converter/{first_code}-to-{second_code}-rate?amount={target}"

  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  results = soup.find("span", {"class":"text-success"})
  return float(results.string)

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
    print(f"#{count} {target[count-1][0].title()}")
    count += 1