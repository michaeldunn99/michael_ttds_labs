import inverted_index
import sys
from collections import defaultdict

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

def phrase_search(word_list, word_present):
    #First loop through the word list to check each of our words are actually there
    #before we start to check if they are there consecutively (as a phrase)
    word_dicts = []
    for word in word_list:
        word_present_boolean, word_dict = word_present(word)
        if not word_present_boolean:
            return False
        else:
            word_dicts.append(word_dict)
    matching_documents = set()
    document_set = word_dicts[0]["document_set"]

    #We are going to maintain our first word position dict for finding phrases
    potential_matching_position_dict = word_dicts[0]["position_dict"]
   
    current_word_position = 0
    for i in range(len(word_dicts)-1):
        next_word_dict = word_dicts[i+1]
        current_word_dict = word_dicts[i]
        matching_documents = matching_documents & next_word_dict["document_set"]
        #re-write potential matching dictionary to only have keys of documents in our document set
        potential_matching_position_dict = {document:potential_matching_position_dict[document] for document in document_set}
            #Loop through each of the documents have all the currently searched words
        for match_doc in document_set:
            #For each of the positions that the current word exists in the current doc
            for position in current_word_dict["position_dict"][match_doc]:

                #Check if the the next_word_dict has a position that is one after (i.e. the words are consecutive)
                if (position+1) not in next_word_dict["position_dict"][match_doc]:
                    #Remove the position of the first word in the potential matching dict
                    potential_matching_position_dict[match_doc].remove(position - current_word_position)
        current_word_position += 1




def main():
    my_inverted_index = inverted_index.generate_inverted_index(sys.argv[1])
    my_word_present = word_present_function(my_inverted_index)
    phrase_search()

if __name__ == "__main__":
    main()



    