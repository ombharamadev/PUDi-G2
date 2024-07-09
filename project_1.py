import os
from bs4 import BeautifulSoup
import pandas as pd

file_path_1 = r"D:\cei_assignments\project_1_files\project1\bpharma\found"
file_path_2 = r"D:\cei_assignments\project_1_files\project1\btech\found"

data = {'File Name': [], 'CGPA': [], 'SGPA': []}

def extract_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Extract CGPA
    cgpa_td = soup.find(string="CGPA\xa0")
    if cgpa_td:
        parent_td = cgpa_td.find_parent('td')
        next_td = parent_td.find_next('td') 
        value = next_td.get_text(strip=True) 
        data['CGPA'].append(value)
    
    else:
        data['CGPA'].append("N/A")

    # Extract SGPA
    sgpa_td = soup.find(string="SGPA\xa0")
    if sgpa_td:
        parent_td = sgpa_td.find_parent('td')
        next_td = parent_td.find_next('td') 
        value = next_td.get_text(strip=True) 
        data['SGPA'].append(value)
    
    else:
        data['SGPA'].append("N/A")

    # Extracting file name
    file_name = os.path.basename(file_path)
    data['File Name'].append(file_name)

def process_directory(directory_path):
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.html'):
            file_path = os.path.join(directory_path, file_name)
            try:
                extract_data(file_path)
                print(f"Data extracted from {file_path}")
            except Exception as e:
                print(f"Error occurred while processing {file_path}: {e}")

            

process_directory(file_path_1)
process_directory(file_path_2)

df = pd.DataFrame(data)
df.to_csv('day3\\extracted_data.csv', index=False)
print("Data extracted to extracted_data.csv successfully")
    

    

