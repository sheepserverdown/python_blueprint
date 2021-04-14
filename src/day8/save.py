import csv

def save_to_file(name, parsed_list):
  file = open(f"{name}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["place","title","time","pay","date"])
  [writer.writerow(inputList) for inputList in parsed_list]
  return