import sys
import time
import re
import nltk
import gzip
from nltk.corpus import stopwords
import Stemmer

def space_only(line):
    pattern = r"^[\s\n]+$"
    return bool(re.match(pattern, line))

def lower_case(text_input):
     return text_input.lower()

def remove_alphanumeric(text_input):
    """
    Remove all alphanumeric characters from the given text input.

    Args:
        text_input (str): The input string from which alphanumeric characters are to be removed.

    Returns:
        str: The resulting string after removing all alphanumeric characters.
    """
    token_pattern = r"[^\w\s]"
    return  re.sub(token_pattern,"", text_input)


def remove_stop_words(iterable_of_text_words, iterable_of_stop_words):
    """
    Remove stop words from a given iterable of text words.

    Args:
        iterable_of_text_words (iterable): An iterable containing words from which stop words need to be removed.
        iterable_of_stop_words (iterable): An iterable containing stop words that need to be removed from the text words.

    Returns:
        str: A list of text_words with the stop words removed from the original list.
    """
    return [word for word in iterable_of_text_words if word not in iterable_of_stop_words]

def my_porter_stemmer(iterable_of_text_words, my_porter_stemmer_function):
    """
    Applies a given Porter stemmer function to each word in an iterable of text words.

    Args:
        iterable_of_text_words (iterable): An iterable containing words to be stemmed.
        my_porter_stemmer_function (function): A function that takes a word as input and returns its stemmed form.

    Returns:
        list: A list of stemmed words.
    """
    return [my_porter_stemmer_function(word) for word in iterable_of_text_words]

def my_preprocessor(text_line, stop_words, porter_stemmer):
    """
    Preprocesses a given text line by applying several text processing steps.

    Args:
        text_line (str): The input text line to be processed.
        stop_words (set): A set of stop words to be removed from the text.
        porter_stemmer (PorterStemmer): An stem method (function) from an instance of PorterStemmer for stemming words.

    Returns:
        str: The processed text line after converting to lowercase, removing alphanumeric characters,
             removing stop words, and applying Porter stemming.
    """

    if space_only(text_line):
        return ""
    else:
        processed_text = " ".join(my_porter_stemmer(remove_stop_words(remove_alphanumeric(lower_case(text_line)).split(), stop_words), porter_stemmer))
        if space_only(processed_text):
            return ""
        else:
            return processed_text



def main():
    if len(sys.argv) < 2:
        sys.exit("Must enter one or more text files to be preprocessed")
    pattern = r"^.*\.txt\.gz$"
    #
    for file in sys.argv[1:]:
        if not re.search(pattern, file):
            sys.exit("Please only enter alphanumeric.txt files as command line arguments")

    file_names = sys.argv[1:]

    stop_words = set(stopwords.words('english'))

    #Instantiate an instance from a porterstemmer class
    stemmer = Stemmer.Stemmer('english')
    #Define my porterstemmer function
    porter_stemmer_function = stemmer.stemWord

    for file in file_names:
        cleaned_file_string = ""
        line_count = 0
        with gzip.open(file, 'rt') as active_file:
            previous_line = None
            for line in active_file:
                cleaned_file_string += my_preprocessor(line, stop_words, porter_stemmer_function) + "\n"
                line_count += 1
                if line_count % 1000000==0:
                    print(cleaned_file_string, end="")
                    cleaned_file_string = ""
       
        # Print any remaining lines after the loop ends
        if cleaned_file_string:
            print(cleaned_file_string, end="")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time-start_time
    print(f"Execution time: {elapsed_time:.2f}s")