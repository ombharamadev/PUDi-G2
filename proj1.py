import os
import pandas as pd
from bs4 import BeautifulSoup

path = "C:\\Users\\Lenovo\\Downloads\\project1"

folders = os.listdir(path)
data = []

for f in folders:
    folder_path = os.path.join(path, f, 'found')
    html_files = os.listdir(folder_path)

    for file in html_files:
        file_path = os.path.join(folder_path, file)
        print(f"Processing file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        file_data = {'filename': file}

        try:
            div = soup.find('div', class_='cont_outer')
            table = div.find('table', class_='cont_DIV_UN')
            td_elements = table.find_all('td', class_='border1')
        except AttributeError:
            print(f"Skipping file due to missing elements: {file_path}")
            continue

        sgpa = cgpa = None

        for td in td_elements:
            text = td.get_text(strip=True)
            if 'SGPA' in text:
                try:
                    sgpa = float(text.split()[-1])
                except ValueError:
                    continue
            elif 'CGPA' in text:
                try:
                    cgpa = float(text.split()[-1])
                except ValueError:
                    continue

        if sgpa is not None or cgpa is not None:
            file_data['sgpa'] = sgpa
            file_data['cgpa'] = cgpa
            data.append(file_data)
df = pd.DataFrame(data)

output_file = "data.csv"
df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")
