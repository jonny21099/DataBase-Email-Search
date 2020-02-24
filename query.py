from bsddb3 import db
import re



def RowID(result): #returns a list with all the row IDs that matches the query.
    if(result[0] == "term"):
        DB_File = "te.idx"
    elif(result[0] == "email"):
        DB_File = "em.idx"
    elif(result[0] == "date"):
        DB_File = "da.idx"
    elif(result[0] == "rec"):
        DB_File = "re.idx"
    else:
        print("Somethings wrong with the first part of the elements in the list")
        return  
    database = db.DB()
    database.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
    database.open(DB_File,None,db.DB_BTREE,db.DB_CREATE)   
    curs = database.cursor()    
    list = []
    if (len(result)==3):    #this check checks whether or not it contains an operator at the end.
        if (result[2] == "<"):  #If it contains < I perform my code to find all dates <
            find = curs.set_range(result[1].encode("utf-8"))
            find = curs.prev()
            if (errorCheck(find) == 1): return
            row = str(find[1].decode("utf-8"))
            list.append(row)
            while(find != None):
                find = curs.prev() 
                if (find != None):
                    row = str(find[1].decode("utf-8"))
                    list.append(row)
                else:
                    return(list)
                    
        elif (result[2] == ">"):    #if it contains > I perform my code to find all dates >
            find = curs.set_range(result[1].encode("utf-8"))
            if (errorCheck(find) == 1): return #this is for putting a hugge number
            value = str(find[0].decode("utf-8"))
            if (value > result[1]): 
                #just do everything greater than value
                row = str(find[1].decode("utf-8"))
                list.append(row)
                while(find != None):
                    find = curs.next()
                    if (find != None):
                        row = str(find[1].decode("utf-8"))
                        list.append(row)
                    else:
                        return(list)
            elif (value == result[1]):
                temp = curs.next_dup()
                while (temp != None):
                    find = temp
                    temp = curs.next_dup()
                find = curs.next()
                row = str(find[1].decode("utf-8"))
                list.append(row)
                while(find != None):
                    find = curs.next()
                    if (find != None):
                        row = str(find[1].decode("utf-8"))
                        list.append(row)
                    else:
                        return(list)
                    
                
                #gotta go to the last duplicate item
        
        elif (result[2] == "<="):
            find = curs.set_range(result[1].encode("utf-8"))
            if (errorCheck(find) == 1): 
                find = curs.prev()
                while(find != None):
                    row = str(find[1].decode("utf-8"))
                    list.append(row)
                    find = curs.prev() 
                return(list)
            value = str(find[0].decode("utf-8"))
            temp = curs.prev()
            if (value > result[1] and temp != None):
                find = temp
            elif (value > result[1] and temp == None):
                return
            curs.next()
            temp2 = curs.next_dup()
            while (temp2 != None):
                if (value == result[1]):
                    find = temp2
                    temp2 = curs.next_dup()
            row = str(find[1].decode("utf-8"))
            list.append(row)
            while(find != None):
                find = curs.prev() 
                if (find != None):
                    row = str(find[1].decode("utf-8"))
                    list.append(row)
                else:
                    return(list)
            
            
        elif (result[2] == ">="):
            find = curs.set_range(result[1].encode("utf-8"))
            if (errorCheck(find) == 1): return
            row = str(find[1].decode("utf-8"))
            list.append(row)
            while(find != None):
                find = curs.next() 
                if (find != None):
                    row = str(find[1].decode("utf-8"))
                    list.append(row)
                else:
                    return(list)
        
            
    if (len(result) == 2 or result[2] == ":" or result[2] == "|"):  #If it doesnt contains one of the <,>,<=,>= operator come here
        find = curs.set(result[1].encode("utf-8"))
        if (errorCheck(find) == 1): return
        row = str(find[1].decode("utf-8"))
        list.append(row)
        while(find != None):
            find = curs.next_dup()
            if (find != None):
                row = str(find[1].decode("utf-8"))
                list.append(row)            
            else:
                return(list) 
                
                
def errorCheck(find):
    if (find == None):
        return 1
        
        
def query(conditions, output):
    result = conditions  #this is what kevin passes me
    Data_index = 0          #this is the index for my database        
    LengthDI = len(result) #this is the length of the things inside result
    check = RowID(result[Data_index])
    final_list = []
    final = check
    if (check == None and result[0][-1] != "|" ):
        print("Nothing was found.")
        return
    while (Data_index < LengthDI):  #in this while loop I perform and or checks with rowIDs
        if (result[Data_index][-1] == "|"):
            temp = RowID(result[Data_index])
            if (temp == None):
                temp = []
            Data_index += 1
            temp2 = RowID(result[Data_index])
            if (temp2 == None):
                temp2 = []
            final_list.append(set(temp)|set(temp2))
            final = final_list[0]
            for each in final_list:
                final = set(final) & each
            if not final:
                print("Nothing was found")
                return
            Data_index += 1
        
        else:    
            temp = RowID(result[Data_index])
            if (temp == None):
                print("Nothing was found.")
                return
            final = set(temp) & set(final) 
            if not final:
                print("Nothing was found")
                return
            Data_index += 1
    database = db.DB()
    DB_File = "re.idx"
    database.open(DB_File,None,db.DB_HASH,db.DB_CREATE)
    curs = database.cursor()
    #Here is the output
    if (output == "brief"):
        for each in final:
            output = curs.set(each.encode("utf-8"))
            print("Row ID: %s\n\tSubject: %s" %(str(output[0].decode("utf-8")), output[1].decode("utf-8").split("<subj>")[1].split("</subj>")[0]))
    elif (output == "full"):
        for each in final:
            output = curs.set(each.encode("utf-8"))
            record = str(output[1].decode("utf-8")).split("><")
            print("Row ID: %s" %(str(output[0].decode("utf-8"))))
            for i in range(len(record)):
                print("\t%s" %(str(record[i])))

























