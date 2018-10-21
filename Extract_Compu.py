path_compu_data = "C:\\Users\\Derek\\Dropbox\\Orlando Pirates\\Data analysis\\compu_data.txt"
path_csv_file = "C:\\Users\\Derek\\Dropbox\\Orlando Pirates\\Data analysis\\csv_file.csv"
message = "Dear {} thank you for buying a ticket for the derby on 27 Oct. Please visit www.orlandopiratesfc.com for match day planning info"
#open the computicket file and read each line into a list variable
compu_data = open(path_compu_data,"r")
compu_data_list = compu_data.readlines()
compu_data.close()
list_len = len(compu_data_list) #This is the number of lines in the file
print (list_len)
#find the heading part which gives the game details and read this into variables
#line_no will be used to go through the file. It will also relate to the index in the list variable
#So line_no =1 will be index 0 etc
line_no = 1
while True:
	#go line by line looking for one that starts with <H4 ALIGN="center">Title:
	line = compu_data_list[line_no]
	if line[0:25] == '<H4 ALIGN="center">Title:':
		#this is the line with the title etc
		#split on <BR> gives the title, then venue, then date time with extra characters
		title_row = line
		title_parts = title_row.split("<BR>")
		event_title = title_parts[0]
		event_title = event_title[25:]
		print(event_title)
		event_venue = title_parts[1]
		event_venue = event_venue[6:]
		print(event_venue)
		event_date_time = title_parts[2]
		event_date_time = event_date_time[12:28]
		print(event_date_time)
		break
	line_no = line_no + 1 #it wasn't this line so move to then next one
#find customer details
#open the cls file and start capturing valid customers
csv_file = open(path_csv_file,"a")
for line_number in range(line_no,list_len): #this starts where we found the title info and goes to the end of the file
	line = compu_data_list[line_number]
	#check if this has customer info
	if line[16:32] == "Customer Details":
		#extract the name and phone number and write into a cls file
		#split on commas to get te name and phone number
		split_cust = line.split(",") 
		customer_name = split_cust[0]
		customer_name = customer_name[34:]
		split_name = customer_name.split() #divide full names into separate words by white spaces
		if len(split_name) != 0:
			#only carry on if there's a name
			salutation = split_name[0]
			if salutation == ".":
				salutation = " "
			first_name = split_name[1]
			surname = split_name[-1] #the last name is the surname
			if len(first_name) > 2: #if a first name has 2 or 1 character it is probably initials
				#change to capital letter then smalls
				first_name = first_name.lower()
				first_name = first_name[0].upper() + first_name[1:]
			customer_name = salutation + " " + first_name + " " + surname
			#now get the number, second in the split
			customer_number = split_cust[1]
			customer_number = customer_number[1:]
			if int(customer_number) > 1000: #if it's smaller than 1000 it isn't a number
				number_27_format = "27" + customer_number[1:] #drops the 0 and adds 27
				#check for landlines
				if number_27_format[2:4] != "11":
					if number_27_format[2:4] != "12":
						if number_27_format[2:4] != "13":
							if number_27_format[2:4] != "21":
								#write a line to the file
								data_string = number_27_format + "," + message.format(customer_name) + "\n"
								csv_file.write(data_string)
csv_file.close()
print("Finished!")
