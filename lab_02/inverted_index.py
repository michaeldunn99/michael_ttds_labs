import sys
import os
import xml.etree.ElementTree as ET
import re
from collections import defaultdict

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
    return root


def preprocess_xml(file_path):
    """
    Preprocesses an XML file by parsing it, extracting document elements, and applying a preprocessing function
    to the text within 'Headline' and 'TEXT' elements.
    Args:
        file_path (str): The path to the XML file to be processed.
    Returns:
        ElementTree.Element: The root element of the processed XML tree.
    """
    my_root = parse_xml(file_path)

    for doc in my_root.findall('DOC'):
        doc_id = doc.find('DOCNO').text.strip()
        
        headline_element = doc.find('Headline')
        if headline_element is not None:
            processed_headline = preprocessing.my_preprocessor(headline_element.text.strip())
            headline_element.text = processed_headline
        
        text_element = doc.find('TEXT')
        if text_element is not None:
            current_text = text_element.text.strip()
            processed_text = preprocessing.my_preprocessor(current_text)
            text_element.text = processed_text
    return my_root

def generate_inverted_index(root: ET.Element):
    word_inverted_index = defaultdict(lambda: {"frequency": 0, "document_list": [], "position_dict": defaultdict(lambda:[])})
    document_inverted_index = defaultdict(dict)
    for doc in root.findall('DOC'):
        doc_id = doc.find('DOCNO').text.strip()
        headline_element = doc.find('Headline')
        if headline_element is not None:
            headline_enumerable = enumerate(headline_element.text)
            headline_length = len(headline_enumerable)
            for i, word in headline_enumerable:
                word_inverted_index[word]["frequency"] += 1

                word_inverted_index[word]["document_list"].append(doc_id)
                word_inverted_index[word]["position_dict"]["doc_id"] = i
        text_element = doc.find('Text')
        if text_element is not None:
            text_enumerable = enumerate(headline_element.text)
            for i, word in headline_enumerable:
                word_inverted_index[word]["frequency"] += 1

                word_inverted_index[word]["document_list"].append(doc_id)
                word_inverted_index[word]["position_dict"]["doc_id"] = i + headline_length




def main():
    check_command_line_arguments(sys.argv, "xml")

    #Save the processed xml_tree in memory
    processed_tree_root = preprocess_xml(sys.argv[1])

#Now we want to loop through each 
if __name__ == "__main__":
    main()
