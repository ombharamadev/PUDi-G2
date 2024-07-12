import bs4
import pandas as pd
import os

root_path = 'Project 1/DATA'
folders = os.listdir(root_path)
df = []

for folder in folders:
    print(len(os.listdir(os.path.join(root_path, folder, 'found'))))

    htmlFiles = os.listdir(os.path.join(root_path, folder, 'found'))

    for file in htmlFiles:
        #print(i)
        #print(os.path.join(root_path, i, 'found', j))
        file_name = os.path.join(root_path, folder, 'found', file)

        print("Filename:-{}\n".format(file))
        print("------------")

        dict = {}
        dict['filename'] = file

        soup = bs4.BeautifulSoup(open(file_name), 'html.parser')

        try:
            div = soup.find('div', class_ = 'cont_outer')

            table = div.find('table', class_ = 'cont_DIV_UN')

            div2 = table.find('div', id = 'midd_part_UN')

            td = table.find_all('td', class_ = 'border1')

        except AttributeError as e:
            print(e)
            pass

        marks_list = []
        for i in td:
            
            if 'SGPA' in i.text or 'CGPA' in i.text:
                #print('Index = {}\n'.format(i.index))
                #print(i.text)
                marks_str = i.text
                try:
                    #print(float(marks_str[6:10]))
                    marks_list.append(float(marks_str[6:10]))
                except ValueError as e:
                    #print(e)
                    pass
                
                #print('---------------------\n')
            
        #print(marks_list)

        if len(marks_list)  == 2:
            dict['sgpa'] = marks_list[0]
            dict['cgpa'] = marks_list[1]
        elif len(marks_list) == 1:
            dict['sgpa'] = marks_list[0]
        else:
            continue
        df.append(dict)

dataframe = pd.DataFrame(df)

dataframe.to_csv("data.csv")

print("Completed!")