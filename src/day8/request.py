import requests
from bs4 import BeautifulSoup

def parsing_url(alba_url):
  response = requests.get(alba_url)
  soup = BeautifulSoup(response.text, 'html.parser')
  results = soup.find("div", {"id":"MainSuperBrand"})
  find_ul = results.find("ul", {"class":"goodsBox"})
  find_li_list = find_ul.find_all("li")
  target_url_list = []
  for li in find_li_list:
    find_anchor = li.find("a", {"class":"goodsBox-info"})["href"]
    company = li.find("a").find("span", {"class":"company"}).string
    target_url_list.append({f"{company}":f"{find_anchor}"})
  return target_url_list

def get_maxPage(url):
  response = requests.get(url)
  soup2 = BeautifulSoup(response.text, 'html.parser')
  try:
    total_page_text = soup2.find("p", {"class":"jobCount"}).find("strong").get_text()
    total_page = int(int(total_page_text) / 50 + 1)
  except Exception:
    total_page = 1
  return total_page

def parsing_job_info(parsed_url):
  except_target = "http://www.alba.co.kr/job/"
  parsed_data = []
  # 페이지 별로 데이터 긁어오기
  maxPage = get_maxPage(parsed_url)
  print(f"All of Page : {maxPage}")
  for current_page in range(maxPage):
    if(except_target in parsed_url) :
      target = f"{except_target}brand/pspfnd/?page=1&pagesize=50"
    else: # "http://www.alba.co.kr/job"으로 시작
      target = f"{parsed_url}job/brand/?page={current_page+1}&pagesize=50"
    response = requests.get(target)
    soup3 = BeautifulSoup(response.text, 'html.parser')

    # tbody의 table 긁어오기 (실질적인 내용)
    table = soup3.find("div", {"id": "NormalInfo"}).find("table").find("tbody").find_all("tr")[::2]
    print(f"current page : {current_page+1}")
    try:
      for td in table:
        local = td.find("td", {"class":"local"}).get_text()
        local = local.replace(u'\xa0', u' ')
        title = td.find("td", {"class":"title"}).find("span", {"class":"company"}).get_text()
        data = td.find("td", {"class":"data"}).find("span").get_text()
        pay = td.find("td", {"class":"pay"}).find("span", {"class":"payIcon"}).string + td.find("td", {"class":"pay"}).find("span", {"class":"number"}).get_text()
        try:
          regDate = td.find("td", {"class":"regDate"}).find("strong").get_text()
        except Exception:
          regDate = td.find("td", {"class":"regDate"}).get_text()
        temp = [local, title, data, pay, regDate]
    except Exception:
      temp = ['','','','','']
    parsed_data.append(temp)
  return parsed_data