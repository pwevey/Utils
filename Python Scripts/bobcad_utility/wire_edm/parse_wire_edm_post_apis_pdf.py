import re
import json
from pdfminer.high_level import extract_text

# Does not fully work but does give you some APIs and Defs. Manually modify after

def extract_text_from_pdf(file_path):
    text = extract_text(file_path)
    lines = text.split('\n')
    api_data = []
    api_name = None

    for line in lines:
        # Find the API name using a regular expression
        match = re.search(r'EDM\w+\(\)', line)
        if match:
            api_name = match.group(0)

        if 'Description:' in line and api_name is not None:
            # Extract the description
            parts = line.split('Description:')
            if len(parts) > 1:
                description = parts[1].strip()
                api_data.append({'BobCAD API': api_name, 'description': description})
                # Reset the API name for the next match
                api_name = None

    return api_data

# Extract text from the PDF file
api_data = extract_text_from_pdf('Wire_EDM_Scripting_Function_Reference.pdf')

# Write the extracted data to a JSON file
with open('postWireEDMAPIs.json', 'w') as f:
    json.dump(api_data, f, indent=4)