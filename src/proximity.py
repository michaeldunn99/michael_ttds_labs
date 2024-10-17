import numpy as np
def proximity(list_0, list_1):
    min_proximity = np.infty
    positions = []
    min_prox_list_0_pos = np.infty
    min_prox_list_1_pos = np.infty
    list_0_counter = 0
    list_1_counter = 0
    i = 1
    previous_list_add = 1000
    merged_list = []

    #Edge case: Starting
    if list_0[list_0_counter] <= list_1[list_1_counter]:
        merged_list.append(list_0[list_0_counter])
        list_0_counter +=1
        previous_list_add = 0
    else:
        merged_list.append(list_1[list_1_counter])
        list_1_counter +=1
        previous_list_add = 1

    #Remainder of the list
    while i < (len(list_0) + len(list_1)):
        #If we have already added all of list 0 then add the next one from list 1 and check proximity
        #Then add the rest of list 0 to the list and we are finished
        if list_0_counter == len(list_0):
            current_list_add = 1
            merged_list.append(list_1[list_1_counter])
            list_1_counter +=1
            if current_list_add + previous_list_add == 1:
                current_proximity = np.abs(merged_list[i]- merged_list[i-1])
                if current_proximity < min_proximity:
                    min_proximity = current_proximity
                    if current_list_add == 1:
                        min_prox_list_1_pos = merged_list[i]
                        min_prox_list_0_pos = merged_list[i-1]
                        
                    else:
                        min_prox_list_0_pos = merged_list[i]
                        min_prox_list_1_pos = merged_list[i-1]
                    positions = [(min_prox_list_0_pos, min_prox_list_1_pos)]
             
                elif current_proximity == min_proximity:
                    if current_list_add == 1:
                        positions.append((merged_list[i-1],merged_list[i]))
                    else:
                        positions.append((merged_list[i],merged_list[i-1]))
            if list_1_counter < len(list_1):
                merged_list.append(list_1[list_1_counter:])
            i = len(list_0) + len(list_1)

        #Else if we have already added all of list 1 then add the next one from list 0 and check proximity
        #Then add the rest of list 0 to the list and we are finished
        elif list_1_counter == len(list_1):
            current_list_add = 0
            merged_list.append(list_0[list_0_counter])
            list_0_counter += 1
            if current_list_add + previous_list_add == 1:
                current_proximity = np.abs(merged_list[i] - merged_list[i-1])
                if current_proximity < min_proximity:
                    min_proximity = current_proximity
                    if current_list_add == 1:
                        min_prox_list_1_pos = merged_list[i]
                        min_prox_list_0_pos = merged_list[i-1]
                    else:
                        min_prox_list_0_pos = merged_list[i]
                        min_prox_list_1_pos = merged_list[i-1]
                    positions = [(min_prox_list_0_pos, min_prox_list_1_pos)]
                elif current_proximity == min_proximity:
                    if current_list_add == 1:
                        positions.append((merged_list[i-1],merged_list[i]))
                    else:
                        positions.append((merged_list[i],merged_list[i-1]))
            if list_0_counter < len(list_0):
                merged_list.append(list_0[list_0_counter:])
            i = len(list_0) + len(list_1)
            break
            
            
        elif list_0[list_0_counter] <= list_1[list_1_counter]:
            current_list_add = 0
            merged_list.append(list_0[list_0_counter])
            list_0_counter +=1
            if current_list_add + previous_list_add == 1:
                current_proximity = np.abs(merged_list[i]- merged_list[i-1])
                if current_proximity < min_proximity:
                    min_proximity = current_proximity
                    if current_list_add == 1:
                        min_prox_list_1_pos = merged_list[i]
                        min_prox_list_0_pos = merged_list[i-1]
                    else:
                        min_prox_list_0_pos = merged_list[i]
                        min_prox_list_1_pos = merged_list[i-1]
                    positions = [(min_prox_list_0_pos, min_prox_list_1_pos)]
                elif current_proximity == min_proximity:
                    if current_list_add == 1:
                        positions.append((merged_list[i-1],merged_list[i]))
                    else:
                        positions.append((merged_list[i],merged_list[i-1]))
            previous_list_add = current_list_add
        else:
            current_list_add = 1
            merged_list.append(list_1[list_1_counter])
            list_1_counter +=1
            if current_list_add + previous_list_add == 1:
                current_proximity = np.abs(merged_list[i]- merged_list[i-1])
                if current_proximity < min_proximity:
                    min_proximity = current_proximity
                    if current_list_add == 1:
                        min_prox_list_1_pos = merged_list[i]
                        min_prox_list_0_pos = merged_list[i-1]
                    else:
                        min_prox_list_0_pos = merged_list[i]
                        min_prox_list_1_pos = merged_list[i-1]
                    positions = [(min_prox_list_0_pos, min_prox_list_1_pos)]
                elif current_proximity == min_proximity:
                    if current_list_add == 1:
                        positions.append((merged_list[i-1],merged_list[i]))
                    else:
                        positions.append((merged_list[i],merged_list[i-1]))
            previous_list_add = current_list_add
        i+=1

        #If the previous item to be added is from a different list to the current one then consider
        #if we have a new minimum proximity
    return min_proximity, positions

if __name__ == "__main__":
        list_0 = [1, 9, 29]
        list_1 = [5, 15, 45]

        list_2 = [1,4,7,123,653]
        list_3 = [6,27,29,100,1000]
        print(proximity(list_0, list_1))
        print(proximity(list_2, list_3))