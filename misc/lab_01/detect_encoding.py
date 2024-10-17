import chardet

def detect_encoding(file_path, sample_size=1024):
    with open(file_path, 'rb') as file:
        raw_data = file.read(sample_size)
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']
        print(f"Detected encoding: {encoding} with confidence {confidence}")

# Path to the file
file_path = "wiki.txt"

# Detect and print the file encoding
detect_encoding(file_path)