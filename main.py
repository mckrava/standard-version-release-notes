import json
import os
import re


TAG_NAME = os.getenv("INPUT_TAG_NAME")
TAG_NAME_PREFIX = os.getenv("INPUT_TAG_NAME_PREFIX")
TAG_NAME_REF_VIEW = os.getenv("INPUT_TAG_NAME_REF_VIEW")
PATH_TO_CHANGELOG = os.getenv("INPUT_CHANGELOG")

if TAG_NAME_REF_VIEW == "true":
    TAG_NAME = TAG_NAME.split("refs/tags/")[1]

# We need remove prefix because changelog contains version headers without prefix
if TAG_NAME_PREFIX != '':
    TAG_NAME = TAG_NAME.replace(TAG_NAME_PREFIX, '', 1)


def get_changelog_lines():
    """
    Read relevant files of changelog for specified tag.

    :return: The desired lines
    :rtype: list(str)
    """
    with open(PATH_TO_CHANGELOG, "r") as read_file:
        all_lines = read_file.readlines()
        changelog_lines = []
        read_line = False
        
        for line in all_lines:
            if line.find(f"## {TAG_NAME}") != -1 or line.find(f"## [{TAG_NAME}]") != -1 or line.find(f"### {TAG_NAME}") != -1 or line.find(f"### [{TAG_NAME}]") != -1:
                read_line = True
                continue
            if read_line:
                if re.search(r'^###?\s\[?\d.\d.\d', line):
                    break
                else:
                    changelog_lines.append(line)
        return changelog_lines


def main():
    notes = get_changelog_lines()
    notes_dict = json.dumps({"notes": notes})
    print(f"::set-output name=notes::{notes_dict}")


if __name__ == "__main__":
    main()
