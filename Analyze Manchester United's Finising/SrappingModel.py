from os import stat
from bs4 import BeautifulSoup
import requests
import csv

# source data
url = 'https://fbref.com/en/comps/9/2022-2023/2022-2023-Premier-League-Stats#all_league_summary'
result = requests.get(url)
doc = BeautifulSoup(result.text, 'html.parser')

collect = []
collect_value = []
column_titles = []
# Collecting Data

# extract data by specify table
def extract_value(data, table_id):
    table = data.find('table', {'id': table_id})
    if table:
        header = table.thead.find_all('th')
        column_titles.extend([th.text.strip() for th in header])
        for row in table.tbody.find_all('tr'):
            # Find the squad name from the table header (th) element
            squad_name = row.find('th', {'data-stat': 'player'}).text.strip()
            # Find all data for each column
            columns = row.find_all('td')
            if len(columns) >= 6:  # Make sure there are at least 6 columns
                  value = [column.text.strip() for column in columns]
                  collect_value.append(value)
                  collect.append((squad_name,value))  # Append a tuple containing squad name and value
    

table_id = 'stats_squads_shooting_for'
extract_value(doc, table_id)
print(collect)
final_list = column_titles[3:23]

with open('club_stats.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(final_list)  # Write header row
    for row_data in collect:
       total_dic = len(row_data[1])
       values = [row_data[0]] + list(row_data[1])[:total_dic] # Convert set to comma-separated string
       writer.writerow(values)