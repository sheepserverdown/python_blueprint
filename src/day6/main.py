import os
from babel.numbers import format_currency
from function import parsing_country_code, parsing_exchange_rate, parsing_tag, print_list
from check import input_check, number_to_code

os.system("clear")

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""
tr = parsing_country_code()
result_list = parsing_tag(tr)
print_list(result_list)

first = 0
second = 0

print("Where are you from? Choose a country by number.")
first = input_check(result_list)
first_code = number_to_code(result_list, first)

print("Now choose another country.")
second = input_check(result_list)
second_code = number_to_code(result_list, second)

print(f"How many {result_list[first-1][2]} do you want to convert to {result_list[second-1][2]}?")
target = input_check(result_list, True)

try:
  rate = parsing_exchange_rate(first_code, second_code, target)
  print(format_currency(target, first_code, locale="ko_KR") + " is " + format_currency(float(target) * rate, second_code, locale="ko_KR"))
except Exception:
  print("No Information about CURRENCY_CODE")
