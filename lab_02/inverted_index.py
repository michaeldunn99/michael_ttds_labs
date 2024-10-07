import sys
import os
import xml.etree.ElementTree as ET
import re

"""
This module processes XML files provided as command line arguments. 
It applies preprocessing to the text within these files and then creates an inverted index. 
The inverted index counts the occurrences of terms and identifies the documents in which these terms exist.
"""
# Add the lab_01 directory to the system path
lab_01_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lab_01'))
print(lab_01_path)
sys.path.append(lab_01_path)

#import preprecessing module from lab_02
import preprocessing

def check_command_line_arguments(command_line_arguments: list, file_type: str):
    """
    Checks the command line arguments to ensure that at least one file is provided 
    and that all files match the specified file type.

    Args:
        command_line_arguments (list): List of command line arguments.
        file_type (str): The expected file type (e.g., "xml", "txt").

    Raises:
        SystemExit: If no files are provided or if any file does not match the specified file type.
    """
    if len(command_line_arguments) < 2:
        sys.exit("Must enter one or more text files to be preprocessed")
    
    pattern = rf"^.*\.{file_type}$"
    
    for file in command_line_arguments[1:]:
        if not re.search(pattern, file):
            sys.exit("Please only enter alphanumeric files with the specified extension as command line arguments")


def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return tree, root

def main():
    check_command_line_arguments(sys.argv, "xml")
    my_root = parse_xml(sys.argv[1])

    for doc in my_root[1].findall('DOC'):
        doc_id = doc.find('DOCNO').text.strip()
        
        if doc.find('Headline'):
            processed_headline = preprocessing.my_preprocessor(doc.find('Headline').text.strip())
            doc.find('Headline').text = processed_headline
            print(doc.find('Headline').text)
        current_text = doc.find('TEXT').text
        processed_text = preprocessing.my_preprocessor(current_text.strip())
        doc.find('TEXT').text = processed_text
        print(doc.find('TEXT').text)
main()
