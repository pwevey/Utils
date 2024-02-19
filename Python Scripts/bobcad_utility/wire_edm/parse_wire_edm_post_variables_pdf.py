from docx import Document
import json

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    post_variables = []
    current_variable_type = None
    for para in doc.paragraphs:
        line = para.text.strip()
        if line.startswith('('):
            current_variable_type = line.strip('()')  # Remove parentheses
        elif line.startswith('-'):
            # Continuation of the previous description
            post_variables[-1]['description'] += ' ' + line[1:].strip()
        elif line:
            # Split the line into the post variable name and the description
            parts = line.split(' ', 1)
            post_variable_name = parts[0]
            description = parts[1] if len(parts) > 1 else ''
            post_variables.append({
                'postVariableName': post_variable_name,
                'description': description,
                'variableType': current_variable_type
            })

    # Write the postVariables array to a JSON file
    with open('postVariables.json', 'w') as json_file:
        json.dump(post_variables, json_file, indent=2)

# Extract text from the docx file
extract_text_from_docx('Wire_EDM_Post_Variables.docx')