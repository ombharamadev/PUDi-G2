import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

btech_path = "{file path}"
bpharma_path = "{file path}"

def scrape_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        div = soup.find("div", {"id": "midd_part_UN"})
        if not div:
            return file_path, None, None

        table = div.find_all("table")[-1]
        if not table:
            return file_path, None, None

        td_all = table.findAll("td", {"class": "border1"})
        if not td_all:
            return file_path, None, None

        try:
            sgpa = td_all[0].text.replace("SGPA", "").strip()
        except IndexError:
            sgpa = None

        try:
            cgpa = td_all[2].text.replace("CGPA", "").strip()
        except IndexError:
            cgpa = None

        return file_path, cgpa, sgpa


data = []

for folder_path in [btech_path, bpharma_path]:
    for root, _, files in os.walk(folder_path):
        for file in tqdm(files):
            if file.endswith('.html'):
                file_name = os.path.join(root, file)
                try:
                    file_name_, cgpa, sgpa = scrape_data(file_name)
                    if cgpa is not None and sgpa is not None:
                        data.append((file_name_, cgpa, sgpa))
                except Exception as e:
                    continue


df = pd.DataFrame(data, columns=['filename', 'cgpa', 'sgpa'])
print(df.head())

# save it in output.csv
df.to_csv("output.csv", index=True)