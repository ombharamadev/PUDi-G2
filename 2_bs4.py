

from bs4 import BeautifulSoup
import pandas as pd
file_name = "sample/21010305041_1800265903.html"

file = open(file_name,"r")

file_data = file.read()

soup = BeautifulSoup(file_data)

div_1 = soup.find("div",{"class":"cont_outer"})

table = div_1.find("table",{"class":"cont_DIV_UN"})

div_2 = table.find("div",{"id":"midd_part_UN"})

table_2 = div_2.find("table")

td_all = table_2.findAll("td",{"class":"border1"})

sgpa = td_all[-6:-5][0]
sgpa = sgpa.text
sgpa = sgpa.replace("SGPA","")

cgpa = td_all[-4:-3][0]
cgpa = cgpa.text
cgpa = cgpa.replace("CGPA","")

new_js = [{
    "file_name":file_name,
    "sgpa":sgpa,
    "cgpa":cgpa
}]

df = pd.DataFrame(new_js)
df.to_csv("out.csv")
