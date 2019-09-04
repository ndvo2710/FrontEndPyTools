import os
import argparse
from bs4 import BeautifulSoup
from bs4.element import Tag

CWD = os.getcwd()

SCSS_HEADER = """
@import url('https://fonts.googleapis.com/css?family=Montserrat:300,700&display=swap');

body,
html {
    margin: 0;
}

body {
    height: 100%;
    font-family: 'Montserrat';
    // display: none;
}
"""

MEDIUM_MEDIA_QUERY = """
@media only screen and (min-width: 1020px) {
"""

LARGE_MEDIA_QUERY = """
@media only screen and (min-width: 1800px) {
"""



class PageBodyParser:
    def __init__(self, html_string):
        self.soup = BeautifulSoup(html_string, features="html.parser")
        self.body = self.soup.find("body")

    def parse_to_file(self):
        file_path = os.path.join(CWD, "output.scss")
        body_children_str = self.get_recursive_chidlren(self.body)
        scss_final_str = f"{SCSS_HEADER}\n{body_children_str}"
        scss_final_str = f"{scss_final_str}\n\n{MEDIUM_MEDIA_QUERY}\n{body_children_str}\n" + "}"
        scss_final_str = f"{scss_final_str}\n\n{LARGE_MEDIA_QUERY}\n{body_children_str}\n" + "}"

        with open(file_path, "w") as f:
            f.write(scss_final_str)
            f.close()

    @staticmethod
    def check_if_tag_constains_child(tag):
        return sum(1 for child in tag.children if isinstance(child, Tag)) > 0

    @staticmethod
    def fixing_tag_name(tag):
        result = []
        if 'class' in tag.attrs:
            for class_name in tag.attrs['class']:
                new_tag_name = f".{class_name}"
                if tag.name != "div":
                    new_tag_name = f"{tag.name}{new_tag_name}"
                result.append(new_tag_name)
        else:
            result.append(tag.name)
        return result

    def get_recursive_chidlren(self, root_tag):
        # result = []
        result = ""
        for tag in root_tag.children:
            if isinstance(tag, Tag):
                tag_names = self.fixing_tag_name(tag)
                if len(tag_names) > 1:
                    for tag_name in tag_names[:-1]:
                        result += "\n" + tag_name + " {\n}\n"
                    last_tag_name = tag_names[-1]
                else:
                    last_tag_name = tag_names[0]
                if self.check_if_tag_constains_child(tag):
                    tag_dict = "\n"
                    tag_dict += last_tag_name + "{\n" + self.get_recursive_chidlren(tag) + "\n}"
                    result += tag_dict
                else:
                    result += "\n" + last_tag_name + " {\n}\n"
        return result


def main():
    parser = argparse.ArgumentParser(description="scss generator parser")
    parser.add_argument("-f",
                        dest="file_path",
                        action="store",
                        type=str,
                        required=True,
                        help=
                        """
                        Required path of your index.html
                        """)
    args = parser.parse_args()

    page = open(args.file_path, "r").read()
    PageBodyParser(page).parse_to_file()


if __name__ == '__main__':
    main()