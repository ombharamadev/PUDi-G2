import os
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures
import threading

file_path_1 = r"D:\cei_assignments\project_1_files\project1\bpharma\found"
file_path_2 = r"D:\cei_assignments\project_1_files\project1\btech\found"

data = {'File Name': [], 'CGPA': [], 'SGPA': []}
processed_files_counter = 0
lock = threading.Lock()

def extract_data(file_path):
    global processed_files_counter
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'lxml')

        # Extract CGPA
        cgpa_td = soup.find(string="CGPA\xa0")
        if cgpa_td:
            parent_td = cgpa_td.find_parent('td')
            next_td = parent_td.find_next('td')
            value = next_td.get_text(strip=True)
            cgpa_value = value
        else:
            cgpa_value = "N/A"

        # Extract SGPA
        sgpa_td = soup.find(string="SGPA\xa0")
        if sgpa_td:
            parent_td = sgpa_td.find_parent('td')
            next_td = parent_td.find_next('td')
            value = next_td.get_text(strip=True)
            sgpa_value = value
        else:
            sgpa_value = "N/A"

        # Extracting file name
        file_name = os.path.basename(file_path)

        # Update the progress counter in a thread-safe manner
        with lock:
            processed_files_counter += 1
            print(f"Processed {processed_files_counter} files")

        # Append data to the lists
        return (file_name, cgpa_value, sgpa_value)
    
    except Exception as e:
        print(f"Error occurred while processing {file_path}: {e}")
        return None

def process_directory(directory_path):
    html_files = [os.path.join(directory_path, file_name) for file_name in os.listdir(directory_path) if file_name.endswith('.html')]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:


        results = list(executor.map(extract_data, html_files))
    
    for result in results:
        if result:
            data['File Name'].append(result[0])
            data['CGPA'].append(result[1])
            data['SGPA'].append(result[2])

# Process directories
process_directory(file_path_1)
process_directory(file_path_2)
 
# Save data to CSV
df = pd.DataFrame(data)
df.to_csv(r"D:\cei_assignments\project_1_files\extracted_data.csv", index=False)
print("Data extracted to extracted_data.csv successfully")
