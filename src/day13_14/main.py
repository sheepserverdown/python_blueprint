import requests
from flask import Flask, render_template, request, redirect, send_file, make_response
from bs4 import BeautifulSoup
import csv

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

db = {}

url = [
    "https://stackoverflow.com/jobs?r=true&q=python",
    "https://weworkremotely.com/remote-jobs/search?term=python",
    "https://remoteok.io/remote-dev+python-jobs"
]

app = Flask("GraduateScrapper")


def parseStruct(title, company, url):
    data = {
        "title": title,
        "company": company,
        "url": url
    }
    return data


def parseStack(soup):
    results = soup.find("div", {"class": "listResults"}).find_all("div", {"class": "js-result"})
    answer = []
    for job in results:
        title = job.find("a", {"class": "s-link"})["title"]
        company = job.find("h3").find("span").get_text().replace("\r", "").replace("\n", "").strip()
        url = "https://stackoverflow.com" + job.find("a", {"class": "s-link"})["href"]
        answer.append(parseStruct(title, company, url))
    return answer


def parseWework(soup):
    results = soup.find("section", {"class": "jobs"}).find_all("li")[:-1]
    answer = []
    for job in results:
        title = job.find("span", {"class": "title"}).get_text()
        company = job.find("span", {"class": "company"}).get_text()
        url = "https://weworkremotely.com" + job.find("a")["href"]
        answer.append(parseStruct(title, company, url))
    return answer


def parseRemoteOk(soup):
    results = soup.find("table", {"id": "jobsboard"}).find_all("tr", {"class": "job"})
    answer = []
    for job in results:
        title = job.find("h2").get_text()
        company = job.find("a", {"class": "companyLink"}).find("h3").get_text()
        url = "https://remoteok.io" + job.find("a", {"class": "preventLink"})["href"]
        answer.append(parseStruct(title, company, url))
    return answer


def searchRequest(url, search):
    data = []
    for target in url:
        request = requests.get(target.replace("python", search), headers=headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        if "stackoverflow" in target:
            result = parseStack(soup)
        elif "weworkremotely" in target:
            result = parseWework(soup)
        elif "remoteok" in target:
            result = parseRemoteOk(soup)
        data += result
    return data


def save_to_file(name, parsed_list):
    file = open(f"{name}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["Title", "company", "Link"])
    [writer.writerow([data['title'], data['company'], data['url']]) for data in parsed_list]
    return


@app.route("/")
def home():
    return render_template("main.html")


@app.route("/search")
def search():
    search = request.args.get('term').lower()
    inputData = db.get(search)

    if (inputData):
        parsingData = inputData
    else:
        if search is None:
            redirect('/')
        else:
            # 1,2,3 세 페이지가 다 다르다
            parsingData = searchRequest(url, search)
            db[search] = parsingData

    return render_template("search.html",
                           length=len(parsingData),
                           search=search,
                           parsingData=parsingData)


@app.route("/export")
def saveFile():
    try:
        search = request.args.get('term').lower()
        data = db.get(search)
        save_to_file(search, data)
        return send_file(
            f"{search}.csv",
            mimetype='text/csv',
            attachment_filename='result.csv',
            as_attachment=True
        )
    except Exception:
        return redirect("/")


app.run(host="0.0.0.0")