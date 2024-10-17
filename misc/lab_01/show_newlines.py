import re

def space_only(line):
    pattern = r"^[\s\n]+$"
    return bool(re.match(pattern, line))

def line_ends_two_line_ends(line):
    pattern = r"\n+$"
    return bool(re.match(pattern, line))

def show_newlines(file_path):
    """
    Reads a text file, replaces newline characters with a visible representation, and prints the modified content.

    Args:
        file_path (str): The path to the text file to be processed.
    """
    with open(file_path, 'r') as file:
        for line in file:
            if space_only(line):
                print("Space only line")
            elif line_ends_two_line_ends(line):
                modified_line = re.sub(r'\n+', '\n', line)
                print(modified_line)
                print("This line ends in two new line characters")
            else:
                print(line, end="")
    
        #modified_content = content.replace('\n', '\\n\n')
        #print(modified_content)

if __name__ == "__main__":
    file_path = "bible_mini.txt"  # Replace with the path to your text file
    show_newlines(file_path)