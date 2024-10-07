import sys
import os

"""
This module processes XML files provided as command line arguments. 
It applies preprocessing to the text within these files and then creates an inverted index. 
The inverted index counts the occurrences of terms and identifies the documents in which these terms exist.
"""
# Add the lab_01 directory to the system path
lab_01_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lab_01'))
print(lab_01_path)
sys.path.append(lab_01_path)

import preprocessing


# Import the preprocessing module