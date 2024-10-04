def main():
    with open("pg10.txt", "r") as file:
        for lines in file:
            print(lines.lower())
        
    
    #Note that if we loop through 'file' it will loop through each of they lines
    #This is the most Pythonic way

if __name__ == "__main__":
    main()
