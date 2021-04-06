import requests
import os


def check_url_exist(url):
    try:
        response = requests.get(url)
        try:
            status = response.status_code
            if (status == 200):
                print(f"{url} is up!")
            return status
        except requests.exceptions.HTTPError:
            print(f"{url} is down!")
            return False
    except requests.exceptions.ConnectionError:
        print(f"{url} is down!")
        return False
    except requests.exceptions.RequestException:
        print(f"{url} is not a valid URL")
        return False


def check_url(url):
    output = [i.strip() for i in url]
    count = 0
    for i in output:
        if i.islower() and i.isupper() is True:
            output[count] = i.lower()

        if 'http://' not in i:
            output[count] = 'http://' + i
        count += 1

    return output


# == main ==

loop = True
loop_in = True
while (loop):
    print("Welcome to IsItDown.py!")
    print("Please write a URL or URLs you want to check. (separated by comma)")
    url = input().split(',')
    url = check_url(url)
    [check_url_exist(i) for i in url]
    while (loop_in):
        print("Do you want to start over? y/n")
        a = input()
        if (a == "y"):
            os.system('clear')
            break
        elif (a == "n"):
            loop_in = False
            break
        else:
            print("That's not valid answer")

    if (loop_in is False):
        break

print("k. Bye!")