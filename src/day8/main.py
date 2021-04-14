import os
from save import save_to_file
from request import parsing_url, parsing_job_info
os.system("clear")
alba_url = "http://www.alba.co.kr"

# url 캐오기
target_url_list = parsing_url(alba_url)



count = 0
for i in target_url_list:
  print(f"Progressing... {count+1}/{len(target_url_list)}")
  parsed_data = parsing_job_info(list(i.values())[0])
  file_name = list(i)[0]
  if('/' in file_name):
    file_name = file_name.replace('/',' ')
  save_to_file(file_name, parsed_data)
  count += 1
print("complete")

