import json5

def count_code_snippets(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = json5.load(file)
    except ValueError as e:
        print(f"Error decoding JSON from file {file_name}: {e}")
        return 0
    return len(content)

files = ['bobcadAdvPostingCustomFiles.code-snippets', 'bobcadLuaVBscript.code-snippets', 'bobcadSpecific.code-snippets']

total_snippets = sum(count_code_snippets(file) for file in files)

print(f'Total number of code snippets: {total_snippets}')
