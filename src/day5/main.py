import os
from soup import parsing_html, parsing_tag, print_list

os.system("clear")

print("Hello! Please choose selct a country by number:")

url = "https://www.iban.com/currency-codes"

tr =  parsing_html(url)
result_list = parsing_tag(tr)
print_list(result_list)

while(True):
  user_input = input("#: ")
  try:
    user_input = int(user_input)
    if(len(result_list) < int(user_input) or int(user_input) == 0):
      print("Choose a number from the list")
    else:
      break
  except Exception:
    print("That wasn't a number")

print(f"You chose {result_list[user_input-1][0].title()}")

try:
  text = result_list[user_input-1][3]
  print(f"The currency code is {text}")
except Exception:
  print("The currency code is None")