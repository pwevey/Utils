import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://bobcad.com/components/webhelp/PostProcessorHelpSystemFiles/Topics/postblockreferenceintroduction.html"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <h3> tags
    h3_tags = soup.find_all("h3")

    # Create a list to store block information
    blocks = []

    # Extract information from each <h3> tag
    for h3_tag in h3_tags:
        block_name = h3_tag.text.strip()

        # Use regular expression to extract the number from the block name
        match = re.search(r'\b\d+\b', block_name)
        block_number = int(match.group()) if match else None

        # Create a dictionary for the block
        block_info = {
            "number": block_number,
            "name": block_name,
            "description": "",
        }

        # Find the following <p> and <ul> elements
        next_elements = h3_tag.find_all_next()

        for element in next_elements:
            if element.name == "p":
                if "Job Type:" in element.text:
                    # Extract job types from the following <ul>
                    ul_element = element.find_next("ul")
                    if ul_element:
                        job_types = [li.text.strip() for li in ul_element.find_all("li")]
                        if job_types:
                            block_info["jobTypes"] = job_types
                    break
                else:
                    # Add text to the description until the next <h3> tag
                    block_info["description"] += element.text.strip() + "\n"
            elif element.name == "h3":
                # Stop when the next <h3> tag is encountered
                break

        # Add the block dictionary to the list
        blocks.append(block_info)

    # Create a dictionary for the final JSON structure
    json_data = {"blocks": blocks}

    # Write the JSON data to a file
    with open("postBlocks.json", "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=2)

    print("JSON file created successfully.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
