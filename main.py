import csv
import requests
import urllib.request
from bs4 import BeautifulSoup

from urllib.request import urlopen

url = "https://en.wikipedia.org/wiki/List_of_chief_executive_officers"
# page = requests.get(url)
html = urlopen(url) 

soup = BeautifulSoup(html, 'html.parser')

rows = soup.find("table").find_all("tr")

biden_donor_codes = ["C00703975","C00744946","C00431916","C00746651","C00213652","C00143701","C00197996"]
all_ceos = []
detailed_ceos = {}
all_donors = []
matches = []

for row in rows:
    cells = row.find_all("td")
    current_person = {}
    if len(cells)>=1:
        rn = cells[1].get_text()
        current_person["company"] = cells[0].get_text()
        if rn and (not rn.isspace()):
            all_ceos.append(rn.upper().lstrip().rstrip())
            current_person["name"] = rn.upper().lstrip().rstrip()
            detailed_ceos[current_person["name"]] = current_person
            # print(rn.upper())

with open('CEO_LIST_2020_FINAL.txt','r') as f:
    count = 0
    for line in f:
        current_person = {}
        count = count + 1
        for character in line:
            if character.isdigit():
                index = line
                count = 0
                break
        if count == 2:
            current_person["company"] = line.upper().lstrip().rstrip()
        if count == 4:
            # print(line)
            if line and (not line.isspace()):
                all_ceos.append(line.upper().lstrip().rstrip())
                current_person["name"] = line.upper().lstrip().rstrip()
                detailed_ceos[current_person["name"]] = current_person
            # for x in range(6):
            #     if "|" in line:
            #         line = line.split("|")[1]
            # line_list = line.split("|")
            # print(line_list[7])


# with open('itcont_2020_20000616_20190425.txt', newline='') as csvfile:
# ...     reader = csv.DictReader(csvfile)
# ...     for row in reader:

import os
for filename in os.listdir('indiv20/by_date'):
    with open("indiv20/by_date/"+filename,'r') as f:
        for line in f:
            if line[:9] in biden_donor_codes:
                line_list = line.split("|")
                name = line_list[7]
                if ", " in name:
                    new_name = name.split(", ")[1]+" "+name.split(", ")[0]
                    if new_name not in all_donors:
                        all_donors.append(new_name)
                        if new_name in all_ceos and new_name in detailed_ceos:
                            # print("* "+new_name)
                            matches.append(detailed_ceos[new_name])
                
for match in matches:
    print(match["name"]+" ("+match["company"]+")")