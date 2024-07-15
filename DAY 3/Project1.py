import bs4
import pandas as pd
import os
from tqdm import tqdm
root_path = r"C:\Users\user\Downloads\project1"
folders = os.listdir(root_path)
df = []

for folder in folders:
    
    folder_path = os.path.join(root_path, folder, 'found')
    if not os.path.exists(folder_path):
        continue

    html_files = os.listdir(folder_path)

    for file in tqdm(html_files):
        file_name = os.path.join(folder_path, file)
        dict_entry = {'filename': file}

        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                soup = bs4.BeautifulSoup(f.read(), 'html.parser')

                div = soup.find('div', class_='cont_outer')
                if div:
                    table = div.find('table', class_='cont_DIV_UN')
                    if table:
                        div2 = table.find('div', id='midd_part_UN')
                        td = table.find_all('td', class_='border1')
                        marks_list = []
                        for i in td:
                            if 'SGPA' in i.text or 'CGPA' in i.text:
                                marks_str = i.text
                                try:
                                    marks_list.append(float(marks_str[6:10]))
                                except ValueError as e:
                                    pass

                        if len(marks_list) == 2:
                            dict_entry['sgpa'] = marks_list[0]
                            dict_entry['cgpa'] = marks_list[1]
                        elif len(marks_list) == 1:
                            dict_entry['sgpa'] = marks_list[0]

        except FileNotFoundError as e:
            print(f"File not found: {file_name}")
            continue
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            continue

        df.append(dict_entry)

dataframe = pd.DataFrame(df)
dataframe.to_csv("data.csv", index=False)

print("Completed!")
