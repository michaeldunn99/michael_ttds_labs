import inverted_index
import sys
import os

# Add the lab_01 directory to the system path
lab_01_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lab_01'))
sys.path.append(lab_01_path)

#import preprecessing module from lab_02
import preprocessing


#Making this object oriented would be better (classes and methods)

def word_present_function(inverted_index):
    def word_present(word):
        lookup = inverted_index[word]
        if lookup["frequency"]:
            return True, lookup
        else:
            return False, lookup
    return word_present

def not_operator(word_1, word_present):
    word_1_present, word_1_dict = word_present(word_1)
    total_docs_set = word_present("_total_document_set")[1]["document_set"]
    if not word_1_present:
        doc_set_difference = total_docs_set - word_1_dict["document_set"]
        print(f"True, document this word is not in are {doc_set_difference}")
        return True, doc_set_difference
    else:
        print("False")
        return False, set()
        
def and_operator(word_1, word_2, word_present):
    word_1_present, word_1_dict = word_present(word_1)
    word_2_present, word_2_dict = word_present(word_2) 
    if word_1_present and word_2_present:
        combined_document_set = word_1_dict["document_set"] & word_2_dict["document_set"]
        print(f"True, combined set it {combined_document_set}")
        return True, combined_document_set
    else:
        print("False")
        return False, set()

def or_operator(word_1, word_2, word_present):
    word_1_present, word_1_dict = word_present(word_1)
    word_2_present, word_2_dict = word_present(word_2) 
    if word_1_present or word_2_present:
        combined_document_set = word_1_dict["document_set"] | word_2_dict["document_set"]
        print(f"True, documents with either of these words are {combined_document_set}")
        return True, combined_document_set
    else:
        print("False")
        return False, set()

def phrase_search(word_present, apply_stemming):
    word_list = input("Which phrase would you like to search?: ")
    word_list = preprocessing.remove_alphanumeric(preprocessing.lower_case(word_list)).split()
    if apply_stemming:
        word_list = preprocessing.my_porter_stemmer(word_list)
    #First loop through the word list to check each of our words are actually there
    #before we start to check if they are there consecutively (as a phrase)
    word_dicts = []
    for word in word_list:
        word_present_boolean, word_dict = word_present(word)
        if not word_present_boolean:
            print("No such phrase!")
            return False
        else:
            word_dicts.append(word_dict)
    document_set = word_dicts[0]["document_set"]

    #We are going to maintain our first word position dict for finding phrases
    #potential_matching_position_dict = word_dicts[0]["position_dict"]
    current_word_position = 0
    potential_positions_dict = {document:word_dicts[0]["position_dict"][document].copy() for document in document_set}
    for i in range(len(word_list)-1):
        docs_with_no_matches = 0
        docs_to_remove = set()
        next_word_dict = word_dicts[i+1]
        current_word_dict = word_dicts[i]
        document_set = document_set & next_word_dict["document_set"]
        potential_positions_dict = {document:potential_positions_dict[document] for document in document_set}
        #re-write potential matching dictionary to only have keys of documents in our document set
        
            #Loop through each of the documents have all the currently searched words
        for match_doc in document_set:
            #For each of the positions that the current word exists in the current docs
            for position in current_word_dict["position_dict"][match_doc]:

                #Check if the the next_word_dict has a position that is one after (i.e. the words are consecutive)
                if (position+1) not in next_word_dict["position_dict"][match_doc]:
                    #All we can say is that 
                    #Remove the position of the first word in the potential matching dict
                        if ((position - i) in potential_positions_dict[match_doc]):
                            potential_positions_dict[match_doc].remove(position - i)
            if len(potential_positions_dict[match_doc]) == 0:
                docs_to_remove.add(match_doc)
                docs_with_no_matches += 1
        
            if docs_with_no_matches == len(potential_positions_dict.keys()):
                print("No such phrase!")
                return False
        
        for doc in docs_to_remove:
            document_set.remove(doc)
            del potential_positions_dict[doc]

    if not potential_positions_dict:
        print("No such phrase!")
        return False

    sorted_docs_first_position = sorted([int(key) for key in potential_positions_dict.keys()])
        
    for match_doc in sorted_docs_first_position:
        print(f"Match in document {match_doc} at postion(s): {sorted(list(potential_positions_dict[str(match_doc)]))}")
    return True, sorted_docs_first_position

def main():
    remove_stop_words = False
    
    apply_stemming = input("Do you want to apply_stemming? (Y/N): ")
    if apply_stemming == "Y":
        apply_stemming = True
    elif apply_stemming == "N":
        apply_stemming = False
    else:
        sys.exit(-1)
    my_inverted_index = inverted_index.generate_inverted_index(sys.argv[1], remove_stop_words, apply_stemming)
    my_word_present_function = word_present_function(my_inverted_index)
    phrase_search(my_word_present_function, apply_stemming)

if __name__ == "__main__":
    main()



    