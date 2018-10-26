#get the file that needs to be added
#define a function to split and extract from a line
def splitter(line,split_char="",index_pos=0):
    '''
    This function accepts a line of text and the character that must be used to split, and the index position of the required word in the list
    It returns a list which is the resultant split
    '''
    return line.split(split_char)[int(index_pos)]

def between_html(line):
    '''
    This function removes the html tag at the beginning and end of a line and returns what is between
    '''
    length = len(line)
    for char in range(0,length-2):
        if line[char:char+1] == ">":
            start_char = char + 1
    answer = line[start_char:]
    answer = answer[:-6]
    return answer
 
 #get the name of the match from the user
game_name = input("Enter the match name in the format pir-chi_abs_18-19   ")
path_compu_data = "C:\\Users\\Derek\\Dropbox\\Orlando Pirates\\Data analysis\\Master_Data\\" + game_name + ".txt"
path_master_data = "C:\\Users\\Derek\\Dropbox\\Orlando Pirates\\Data analysis\\Master_Data\\master_data.csv"

#open the computicket file and read each line into a list variable
compu_data = open(path_compu_data,"r")
compu_data.seek(0)
compu_data_list = compu_data.readlines()
compu_data.close()
list_len = len(compu_data_list) #This is the number of lines in the file
#find the heading part which gives the game details and read this into variables
#line_no will be used to go through the file. It will also relate to the index in the list variable
#So line_no =1 will be index 0 etc
line_no = 1
while line_no <= list_len - 5:
    #go line by line looking for one that starts with <H4 ALIGN="center">Title:
    line = compu_data_list[line_no]
    if '<H4 ALIGN="center">Title:' in line:
        #this is the line with the title etc
        event_title = splitter(line,"<BR>",0)
        event_title = event_title[25:]
        print(event_title)
        event_venue = splitter(line,"<BR>",1)
        event_venue = event_venue[6:]
        print(event_venue)
        event_date_time = splitter(line,"<BR>",2)
        event_date_time = event_date_time[12:28]
        event_date = splitter(event_date_time," ",0)
        #change date format
        event_date = event_date[-2:] + "/" + event_date[3:5] + "/" + event_date[0:2]
        event_time = splitter(event_date_time," ",1)
        print(event_date)
        print(event_time)
        break
    line_no = line_no + 1

#find customer details
#open the cls file and start capturing valid customers
#first check if this game already exists
dup_count = 0
for line_check in open(path_master_data):
    game_check = splitter(line_check,",",0)
    if game_check == game_name :  # note this is game name not event title
        dup_count = dup_count + 1
if dup_count > 0:
    print(str(dup_count) + " entries already found for this match, aborting")
    #master_data_file.close()   This may be needed
else:
    #write new data in the file, appending
    master_data_file = open(path_master_data,"a")
    #stop_checking = False    for testing
    while line_no <= list_len - 5: #this starts where we found the title info and goes to the end of the file
        line = compu_data_list[line_no]
        #check if this is the start of a customer
        if 'ROWSPAN="2"' in line:
            #extract the details and write into the master file
            #this is what the data looks like
            #<TD ALIGN="center" ROWSPAN="2"><A HREF="/report/reports_performances.BasketLineDetails?p_basket_line=197541430&p_performance=7054272">L4CU0L2C</A></TD>
            #<TD>20/09/18 14:34</TD>
            #<TD>client services jhbg 10 khetha</TD>
            #<TD>PRINT</TD>
            #<TD>Level 2 Block 227</TD>
            #<TD>Level 2 Block 227</TD>
            #<TD>N:16</TD>
            #<TD>Full</TD>
            #<TD ALIGN="right">1</TD>
            #<TD ALIGN="right">         170.00</TD>
            #</TR>
            #<TR ALIGN="left">
            #<TD COLSPAN="9">Customer Details: .   Sample, 0113408208,</TD>
            #</TR>
            #<TR ALIGN="left">

            #go to the next line to get the date and time of purchase
            line_no=line_no + 1
            purchase_date = splitter(compu_data_list[line_no]," ",0)
            purchase_date = purchase_date[4:12]
            #change date format
            purchase_date = purchase_date[-2:] + "/" + purchase_date[3:5] + "/" + purchase_date[0:2]
            purchase_time = splitter(compu_data_list[line_no]," ",1)
            purchase_time = purchase_time[0:5]
            #go to the next line to get the purchase place
            line_no = line_no + 1
            purchase_place = between_html(compu_data_list[line_no])
            #go to the next line to get STATUS
            line_no = line_no + 1
            status = between_html(compu_data_list[line_no])
            #go to the next line to get area
            line_no = line_no + 1
            area = between_html(compu_data_list[line_no])
            #go to the next line to get section
            line_no = line_no + 1
            section = between_html(compu_data_list[line_no])
            #go to the next line to get seats
            line_no = line_no + 1
            seats = between_html(compu_data_list[line_no])
            #go to the next line to get discount code
            line_no = line_no + 1
            discount_code = between_html(compu_data_list[line_no])
            #go to the next line to get number
            line_no = line_no + 1
            number = between_html(compu_data_list[line_no])
            #go to the next line to get amount
            line_no = line_no + 1
            amount = between_html(compu_data_list[line_no])
            #remove spaces and comma from amount
            new_amount = ""
            for char in amount:
                if char != " " and char != ",":
                    new_amount = new_amount + char
            amount = new_amount
            #go to the third next line to get customer details
            line_no = line_no + 3
            customer_details = between_html(compu_data_list[line_no])
            if customer_details[0:3] == "Res":
                #This is a reservation note line
                customer_name = customer_details
                customer_number = ""
                customer_field2 = ""
            else:
                customer_name = splitter(customer_details,",",0)
                customer_name = customer_name[18:]
                customer_number = splitter(customer_details,",",1)
                #make customer number a string
                customer_number = "'" + str(customer_number[1:])
                customer_field2 = splitter(customer_details,",",2)
            #Now write all this to the file
            data_string = game_name + "," + event_title + "," + event_venue + "," + event_date + ","
            data_string = data_string + event_time + "," + purchase_date + "," + purchase_time + "," + purchase_place + ","
            data_string = data_string + status + "," + area + "," + section + "," + seats + "," + discount_code + ","
            data_string = data_string + number + "," + amount + "," + customer_name + "," + customer_number + "," + customer_field2 + "\n"
            master_data_file.write(data_string)
            #stop_checking = True  for testing

            
        line_no = line_no + 1
        #if stop_checking:
        #   line_no = 1000000
    master_data_file.close()
    print ("Finished!")