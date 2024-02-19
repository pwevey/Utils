import json

# Load the data from the JSON file
with open('postVariablesEDM.json', 'r') as f:
    data = json.load(f)

# Modify the 'jobTypes' values
for postVariable in data['postVariables']:
    if isinstance(postVariable['jobTypes'], str):
        postVariable['jobTypes'] = [postVariable['jobTypes']]

# Write the modified data back to the JSON file
with open('postVariablesEDM.json', 'w') as f:
    json.dump(data, f, indent=4)