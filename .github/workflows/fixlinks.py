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
            for element in elements:
                href = element["href"]
                if href.startswith("/assets") or href.startswith("/etc"):
                    updated_href = static_prefix + href
                    element["href"] = updated_href
                    updated_links.append(f"Original: {href}\nUpdated: {updated_href}\n")

        css_elements = soup.find_all("link", rel="stylesheet", href=True)
        for css_element in css_elements:
            href = css_element["href"]
            if href.startswith("/assets") or href.startswith("/etc"):
                updated_href = static_prefix + href
                css_element["href"] = updated_href
                updated_links.append(f"Original: {href}\nUpdated: {updated_href}\n")

        font_elements = soup.find_all("style")
        for font_element in font_elements:
            if "@font-face" in font_element.string:
                updated_string = font_element.string.replace("/assets", static_prefix)
                font_element.string = updated_string
                updated_links.append("Updated font URLs\n")

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
