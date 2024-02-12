import os
import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://bobcad.com/components/webhelp/PostProcessorHelpSystemFiles/Topics/Post%20Variables%20and%20API%20Reference.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

post_variables = []

# Iterate through each table tag
for table in soup.find_all('table'):
    # Extract post variable names from the anchor tags in the first td of the first tr
    anchor_names = [a['name'] for a in table.select('tr:first-child td:first-child a[name]')]

    for anchor_name in anchor_names:
        post_variable = {}

        # Check if postVariableName starts with "LATHE" or "MILL"
        if anchor_name and anchor_name.upper().startswith(('LATHE', 'MILL')):
            post_variable['postVariableName'] = None
        else:
            post_variable['postVariableName'] = anchor_name if anchor_name else None


        # Extract jobTypes and description from other tr tags
        job_types = []
        description = None
        api_calls = []

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
                
                # Remove \u00a0 from descriptions
                description = description.replace('\u00a0', '')
                
                post_variable['description'] = description.replace('\u00e2\u0080\u0093', '')

                # Manually set postVariableName if description matches the specified text
                if description == "Signals the output of the stock definition":
                    post_variable['postVariableName'] = "output_stock_definition"
                    

                if "API:" in description or "TCPAPI" in description or re.search(r'\bAPI\b', description):
                    # Extract API calls from the description
                    api_pattern = re.compile(r'\b((MILL|LATHE|TURN|Get)\w*\([^)]*\))', re.IGNORECASE)

                    api_calls = [
                        api for api_tuple in set(api_pattern.findall(description))
                        if not any(char.isdigit() for char in api_tuple)
                        for api in api_tuple
                    ]
                    
                    # print(api_calls)

                    # Remove single-word entries
                    api_calls = [api for api in api_calls if not api.lower() in ["get", "lathe", "mill"]]

                    # Remove instances of '\u00e2\u0080\u009c' and '\u00e2\u0080\u009d' from each API call
                    api_calls = [api.replace('\u00e2\u0080\u009c', '').replace('\u00e2\u0080\u009d', '') for api in api_calls]            

        # print(api_calls)

        post_variable['bobcadAPIs'] = api_calls
        post_variables.append(post_variable)

# Create a folder named "data" if it doesn't exist
data_folder = 'data'
os.makedirs(data_folder, exist_ok=True)

# Write to JSON file inside the "data" folder
output_json_path = os.path.join(data_folder, 'postVariables.json')
with open(output_json_path, 'w') as json_file:
    json.dump({"postVariables": post_variables}, json_file, indent=2)

print(f"Scraping and JSON creation completed. Check '{output_json_path}' file.")
