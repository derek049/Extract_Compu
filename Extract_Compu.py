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
		len_line = len(line)
		#look for the title first
		#look for the first <BR>
		char = 24 #start towards the end of the part we know
		while True:
			test_char = line[char:char + 4]
			if test_char == "<BR>":
				#we know where <BR> is
				char_title = char
				event_title = line[25:char_title]
				print (event_title)
				break
			char = char + 1
		while True:
			#now look for the second <BR>
			char = char + 1
			test_char = line[char:char + 4]
			if test_char == "<BR>":
				#we know where 2nd <BR> is
				char_venue = char
				event_venue = line[char_title + 10:char_venue]
				print (event_venue)
				event_date_time = line[char_venue + 16:len_line - 6]
				print (event_date_time)
				break
		break
	line_no = line_no + 1
#find customer details
#open the cls file and add myself in the first line as a test
csv_file = open(path_csv_file,"a")

for line_number in range(line_no,list_len): #this starts where we found the title info and goes to the end of the file
	line = compu_data_list[line_number]
	#check if this has customer info
	if line[16:32] == "Customer Details":
		#extract the name and phone number and write into a cls file
		#look for the first comma
		char = 31 #this is the colon after details
		while True:
			if line[char]  == ",":
				customer_name = line[34:char]
				split_name = customer_name.split() #divide into separate words by white spaces
				if len(split_name) == 0:
						break
				salutation = split_name[0]
				if salutation == ".":
					salutation = " "
				first_name = split_name[1]
				surname = split_name[-1]
				if len(first_name) > 2: #if a first name has 2 or 1 character it is probably initials
					first_name = first_name.lower()
					first_name = first_name[0].upper() + first_name[1:]
				customer_name = salutation + " " + first_name + " " + surname
				char_number = char + 2
				customer_number = line[char_number:char_number + 10]
				if int(customer_number) < 1000: 
					break
				number_27_format = "27" + customer_number[1:]
				#check for landlines
				if number_27_format[2:4]== "11":
					break
				if number_27_format[2:4]== "12":
					break
				if number_27_format[2:4]== "13":
					break
				if number_27_format[2:4]== "21":
					break
				#write a line to the file
				data_string = number_27_format + "," + message.format(customer_name) + "\n"
				csv_file.write(data_string)
				break
			char = char + 1
csv_file.close()
print("Finished!")
