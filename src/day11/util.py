from bs4 import BeautifulSoup


def extract_checked_url(queryString):
    queryString = queryString.decode('utf-8').split('&')
    targetReddits = []
    [targetReddits.append(info.split('=')[0]) for info in queryString]
    return targetReddits


def convert_to_Int(votes):
    # k는 *100이다. 온점(.) 빼고 k 빼고 100 곱하기
    return int((votes.replace(".", "")).replace("k", "")) * 100


def parsing_data(response, subreddit):
    parse_result = []

    # 추출할 내용 : 제목, 주소, vote, 서브레딧
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find_all("div", {"class": "Post"})
    result.pop(1)

    for content in result:
        # 제목 얻기
        title = content.find("h3", {"class": "_eYtD2XCVieq6emjKBH3m"}).get_text()

        # 주소 얻기
        url = content.find("a", {"class": "_2INHSNB8V5eaWp4P0rY_mE"})["href"]
        url = f"https://www.reddit.com{url}"

        # vote 얻기
        votes = content.find("div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"}).get_text()

        # vote to Number
        votesNum = convert_to_Int(votes)

        # 서브 레딧
        reddit = f"r/{subreddit}"

        parse_result.append(
            {"title": title,
             "url": url,
             "votes": votes,
             "votesNum": votesNum,
             "reddit": reddit}
        )

    return parse_result