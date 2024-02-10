import os
import requests
from bs4 import BeautifulSoup
import json

url = "https://bobcad.com/components/webhelp/PostProcessorHelpSystemFiles/Topics/Post%20Variables%20and%20API%20Reference.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

post_variables = []

# Iterate through each table tag
for table in soup.find_all('table'):
    post_variable = {}
    
    # Extract post variable name from the anchor tag in the first td of the first tr
    post_variable_name = table.select_one('tr:first-child td:first-child a[name]')
    if post_variable_name:
        post_variable['postVariableName'] = post_variable_name['name']
    
    # Extract jobTypes and description from other tr tags
    job_types = []
    description = None
    for tr in table.find_all('tr')[1:]:
        tds = tr.find_all('td')
        if tds:
            job_type = tds[0].get_text(strip=True)
            job_types.append(job_type)
    
    post_variable['jobTypes'] = job_types

    description_row = table.find_all('tr')[1]
    if description_row:
        tds = description_row.find_all('td')
        if len(tds) >= 2:
            # Description found in the second td
            description = tds[1].get_text(strip=True)
            post_variable['description'] = description
    
    post_variables.append(post_variable)

# Create a folder named "data" if it doesn't exist
data_folder = 'data'
os.makedirs(data_folder, exist_ok=True)

# Write to JSON file inside the "data" folder
output_json_path = os.path.join(data_folder, 'postVariables.json')
with open(output_json_path, 'w') as json_file:
    json.dump({"postVariables": post_variables}, json_file, indent=2)

print(f"Scraping and JSON creation completed. Check '{output_json_path}' file.")
