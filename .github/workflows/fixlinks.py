import os
import sys
from bs4 import BeautifulSoup

def update_html_files(folder_path, static_prefix):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".html"):
                file_path = os.path.join(root, file_name)
                update_html_file(file_path, static_prefix)

def update_html_file(file_path, static_prefix):
    with open(file_path, "r+") as file:
        content = file.read()
        soup = BeautifulSoup(content, "html.parser")

        tags = ["a", "link", "script", "img"]
        for tag in tags:
            elements = soup.find_all(tag, href=True)
            for element in elements:
                href = element["href"]
                if href.startswith("/assets") or href.startswith("/etc"):
                    element["href"] = static_prefix + href

        css_elements = soup.find_all("link", rel="stylesheet", href=True)
        for css_element in css_elements:
            href = css_element["href"]
            if href.startswith("/assets") or href.startswith("/etc"):
                css_element["href"] = static_prefix + href

        font_elements = soup.find_all("style")
        for font_element in font_elements:
            if "@font-face" in font_element.string:
                font_element.string = font_element.string.replace("/assets", static_prefix)

        file.seek(0)
        file.write(str(soup))
        file.truncate()

# Usage example
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py folder_path static_prefix")
        sys.exit(1)

    folder_path = sys.argv[1]
    static_prefix = sys.argv[2]
    update_html_files(folder_path, static_prefix)
