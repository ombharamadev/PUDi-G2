import os
from bs4 import BeautifulSoup
import pandas as pd

file_path = r"C:\Users\Haransh Singh\Desktop\python\project1\p1data"

folders = os.listdir(file_path)
data = []

for folder in folders:
    data_files_path = os.path.join(file_path, folder,'found')
    
    if not os.path.exists(data_files_path):
        print(f"Path {data_files_path} does not exist.")
        continue

    data_files = os.listdir(data_files_path)

for file in data_files:
    file_name = os.path.join(file_path, folder,'found', file)
    print(f"Processing file: {file}")

    record = {'filename': file}
    
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        div = soup.find('div', class_='cont_outer')
        table = div.find('table', class_='cont_DIV_UN')
        div2 = table.find('div', id='midd_part_UN')
        td_elements = table.find_all('td', class_='border1')

        marks_list = []
        for td in td_elements:
            if 'SGPA' in td.text or 'CGPA' in td.text:
             
                marks_str = td.text
                try:
                    marks_list.append(float(marks_str[6:10]))
                except ValueError as e:
                    pass

        if len(marks_list) == 2:
            record['sgpa'] = marks_list[0]
            record['cgpa'] = marks_list[1]
        elif len(marks_list) == 1:
            record['sgpa'] = marks_list[0]
        else:
            pass
        data.append(record)
    
    except Exception as e:
        print("Error processing file ")
        

dataframe = pd.DataFrame(data)
output_file = "output.csv"
dataframe.to_csv(output_file)
print("Completed")
