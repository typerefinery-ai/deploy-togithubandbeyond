import os
import sys
from bs4 import BeautifulSoup

def update_html_files(folder_path, static_prefix):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".html"):
                file_path = os.path.join(root, file_name)
                updated_links = update_html_file(file_path, static_prefix)
                print(f"File: {file_path}")
                print("Updated Links:")
                print("\n".join(updated_links))
                print()

def update_html_file(file_path, static_prefix):
    updated_links = []

    with open(file_path, "r+") as file:
        content = file.read()
        soup = BeautifulSoup(content, "html.parser")

        tags = ["a", "link", "script", "img"]
        for tag in tags:
            elements = soup.find_all(tag, href=True)
            elements += soup.find_all(tag, src=True)
            for element in elements:
                if "href" in element.attrs:
                    attr_name = "href"
                    attr_value = element["href"]
                else:
                    attr_name = "src"
                    attr_value = element["src"]

                if attr_value.startswith("/assets") or attr_value.startswith("/etc"):
                    updated_attr_value = static_prefix + attr_value
                    element[attr_name] = updated_attr_value
                    updated_links.append(f"Original: {attr_value}\nUpdated: {updated_attr_value}\n")

                if tag == "img" and "srcset" in element.attrs:
                    srcset_values = element["srcset"].split(",")
                    updated_srcset_values = []
                    for value in srcset_values:
                        if value.strip().startswith("/assets") or value.strip().startswith("/etc"):
                            updated_value = static_prefix + value.strip()
                            updated_srcset_values.append(updated_value)
                            updated_links.append(f"Original (srcset): {value.strip()}\nUpdated: {updated_value}\n")
                        else:
                            updated_srcset_values.append(value.strip())
                    element["srcset"] = ", ".join(updated_srcset_values)

        file.seek(0)
        file.write(str(soup))
        file.truncate()

    return updated_links

# Usage example
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py folder_path static_prefix")
        sys.exit(1)

    folder_path = sys.argv[1]
    static_prefix = sys.argv[2]
    update_html_files(folder_path, static_prefix)
