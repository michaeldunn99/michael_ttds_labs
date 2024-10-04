import sys
import time
import re
import nltk
import gzip
import concurrent.futures
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from io import StringIO

# Download the necessary NLTK data
# nltk.download('stopwords')
# nltk.download('punkt_tab')

def space_only(line):
    pattern = r"^[\s\n]+$"
    return bool(re.match(pattern, line))

def lower_case(text_input):
    return text_input.lower()

def remove_alphanumeric(text_input):
    token_pattern = r"[^\w\s]"
    return re.sub(token_pattern, "", text_input)

def remove_stop_words(iterable_of_text_words, iterable_of_stop_words):
    return [word for word in iterable_of_text_words if word not in iterable_of_stop_words]

def my_porter_stemmer(iterable_of_text_words, my_porter_stemmer_function):
    return [my_porter_stemmer_function(word) for word in iterable_of_text_words]

def my_preprocessor(text_line, stop_words, porter_stemmer):
    if space_only(text_line):
        return ""
    else:
        processed_text = " ".join(my_porter_stemmer(remove_stop_words(remove_alphanumeric(lower_case(text_line)).split(), stop_words), porter_stemmer))
        if space_only(processed_text):
            return ""
        else:
            return processed_text

def process_file(file, stop_words, porter_stemmer_function):
    cleaned_file_string = StringIO()
    line_count = 0
    with gzip.open(file, 'rt') as active_file:
        for line in active_file:
            cleaned_file_string.write(my_preprocessor(line, stop_words, porter_stemmer_function) + "\n")
            line_count += 1
            if line_count % 100000 == 0:
                print(cleaned_file_string.getvalue(), end="")
                cleaned_file_string = StringIO()
    if cleaned_file_string.getvalue():
        print(cleaned_file_string.getvalue(), end="")

def main():
    if len(sys.argv) < 2:
        sys.exit("Must enter one or more text files to be preprocessed")
    pattern = re.compile(r"^.*\.txt\.gz$")
    for file in sys.argv[1:]:
        if not pattern.search(file):
            sys.exit("Please only enter alphanumeric.txt files as command line arguments")

    file_names = sys.argv[1:]
    stop_words = set(stopwords.words('english'))
    porter = PorterStemmer()
    porter_stemmer_function = porter.stem

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_file, file, stop_words, porter_stemmer_function) for file in file_names]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f}s")
