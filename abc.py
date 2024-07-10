import os
import pandas as pd
from bs4 import BeautifulSoup
btech_path = r"C:\Users\Naitik Aggarwal\Downloads\project1\btech\found"
bpharma_path = r"C:\Users\Naitik Aggarwal\Downloads\project1\bpharma\found"
data = []
def scrape_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        div_1 = soup.find("div", {"class": "cont_outer"})
        if not div_1:
            return file_path, None, None
        
        table = div_1.find("table", {"class": "cont_DIV_UN"})
        if not table:
            return file_path, None, None
        
        div_2 = table.find("div", {"id": "midd_part_UN"})
        if not div_2:
            return file_path, None, None
        
        table_2 = div_2.find("table")
        if not table_2:
            return file_path, None, None
        
        td_all = table_2.findAll("td", {"class": "border1"})
        if not td_all:
            return file_path, None, None
        
        try:
            sgpa = td_all[-6].text.replace("SGPA", "").strip()
        except IndexError:
            sgpa = None

        try:
            cgpa = td_all[-4].text.replace("CGPA", "").strip()
        except IndexError:
            cgpa = None

        print(f"File {file_path} scraped successfully.")
        return file_path, cgpa, sgpa
        
for folder_path in [btech_path, bpharma_path]:
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    data.append(scrape_data(file_path))
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")


df = pd.DataFrame(data, columns=['File name', 'cgpa', 'sgpa'])
output_csv_path = 'output.csv'
df.to_csv(output_csv_path, index=False)