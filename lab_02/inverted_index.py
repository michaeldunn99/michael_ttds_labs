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


#Making this object oriented would be better (classes and methods)

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
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at path {file_path} does not exist.")
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root


def preprocess_xml(file_path, remove_stop_words, apply_stemming):
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
        
        headline_element = doc.find('HEADLINE')
        if headline_element is not None:
            processed_headline = preprocessing.my_preprocessor(headline_element.text.strip(), remove_stop_words, apply_stemming)
            headline_element.text = processed_headline
        
        text_element = doc.find('TEXT')
        if text_element is not None:
            current_text = text_element.text.strip()
            processed_text = preprocessing.my_preprocessor(current_text, remove_stop_words, apply_stemming)
            text_element.text = processed_text
    return my_root

def generate_inverted_index(file_path, remove_stop_words, apply_stemming):
    root = preprocess_xml(file_path, remove_stop_words, apply_stemming)
    word_inverted_index = defaultdict(lambda: {"frequency": 0, "document_set": set(), "position_dict": defaultdict(lambda:set())})
    for doc in root.findall('DOC'):
        headline_length = 0
        doc_id = doc.find('DOCNO').text.strip()
        headline_element = doc.find('HEADLINE')
        if headline_element is not None:
            headline_enumerable = enumerate(headline_element.text.split())
            headline_list = list(headline_enumerable)
            #print(headline_list)
            headline_length = headline_list[-1][0] + 1 if headline_list else 0
            for i, word in headline_list:
                word_inverted_index[word]["frequency"] += 1
                word_inverted_index[word]["document_set"].add(doc_id)
                word_inverted_index[word]["position_dict"][doc_id].add(i)
                word_inverted_index["_total_document_set"]["document_set"].add(doc_id)
        text_element = doc.find('TEXT')
        if text_element is not None:
            text_enumerable = enumerate(text_element.text.split())
            for i, word in text_enumerable:
                word_inverted_index[word]["frequency"] += 1
                word_inverted_index[word]["document_set"].add(doc_id)
                word_inverted_index[word]["position_dict"][doc_id].add(i + headline_length)
                word_inverted_index["_total_document_set"]["document_set"].add(doc_id)
    return word_inverted_index

def write_index_to_file(inverted_index, file_path):
    with open(file_path, 'w') as output_file:
        for word in inverted_index:
            output_file.write(f"{word}:\n")
            output_file.write(f"\tFrequency: {inverted_index[word]['frequency']}\n")
            for doc_id in inverted_index[word]["position_dict"]:
                if word != "_total_document_set":
                    output_file.write(f"\tDoc_ID: {doc_id} Position(s): {inverted_index[word]['position_dict'][doc_id]}\n")
            output_file.write("\n")

def main():
    check_command_line_arguments(sys.argv, "xml")

    #Save the processed xml_tree in memory
    #processed_tree_root = preprocess_xml()

    remove_stop_words = input("Do you want to remove stop words? (Y/N): ")
    if remove_stop_words == "Y":
        remove_stop_words = True
    elif remove_stop_words == "N":
        remove_stop_words = False
    else:
        sys.exit(-1)
    
    apply_stemming = input("Do you want to apply_stemming? (Y/N): ")
    if apply_stemming == "Y":
        apply_stemming = True
    elif apply_stemming == "N":
        apply_stemming = False
    else:
        sys.exit(-1)

    #Generate a word index
    word_index = generate_inverted_index(sys.argv[1], remove_stop_words, apply_stemming)

    #Output result to text file
    input_file_name = sys.argv[1]
    pattern = r'([^/]+)\.xml$'
    match = re.search(pattern, input_file_name)
    if match:
        output_file_name = match.group(1) + ".txt"
    else:
        sys.exit("Invalid input file format. Expected a .xml file.")
    print(output_file_name)
    #Need to work out how to set the output name correctly
    write_index_to_file(word_index, output_file_name)


#Now we want to loop through each 
if __name__ == "__main__":
    main()
