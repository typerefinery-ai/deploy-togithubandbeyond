import os
import sys
import re
from bs4 import BeautifulSoup

def update_html_files(folder_path, static_prefix, pattern):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".html"):
                file_path = os.path.join(root, file_name)
                updated_links = update_html_file(file_path, static_prefix, pattern)
                print(f"File: {file_path}")
                print("Updated Links:")
                print("\n".join(updated_links))
                print()

def update_html_file(file_path, static_prefix, pattern):
    updated_links = []

    with open(file_path, "r+") as file:
        content = file.read()
        soup = BeautifulSoup(content, "html.parser")

        for element in soup.find_all(True):
            for attribute, value in element.attrs.items():
                if isinstance(value, str) and re.search(pattern, value):
                    updated_value = static_prefix + value
                    element[attribute] = updated_value
                    updated_links.append(f"Tag: {element.name}\nAttribute: {attribute}\nOriginal: {value}\nUpdated: {updated_value}\n")

        file.seek(0)
        file.write(str(soup))
        file.truncate()

    return updated_links

# Usage example
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py folder_path static_prefix pattern")
        sys.exit(1)

    folder_path = sys.argv[1]
    static_prefix = sys.argv[2]
    pattern = sys.argv[3]
    update_html_files(folder_path, static_prefix, pattern)
