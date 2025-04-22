
def scrap(lines: list, symbs: list, symbms: list = []):   
    new_list = []
    
    running_multi_line = False

    for line in lines:
        delete_line = False

        for symb in symbs:
            idx = line.find(symb)
            if idx >= 0:
                line = line[:idx]
                if idx == 0:
                    delete_line = True
        
        for symbm in symbms:
            idx = line.find(symbm)
 
            if running_multi_line:
                delete_line = True

            if idx >= 0:
                if running_multi_line:
                    delete_line = True
                    running_multi_line = False
                else:
                    running_multi_line = True
                    delete_line = True

        if not delete_line:
            new_list.append(line)

    
    return new_list
    
