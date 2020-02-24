import re

#This function writes to terms.txt file
def prepTerms(inFile):
	termsFile = open("terms.txt", "w+") #Creates terms.txt with w+ (writing and reading) rights
	with open(inFile, 'r') as file: #Opens inFile (xml file passed as argument)
		for line in file: #for loop for each line
			if line.startswith("<mail>"): #Only take lines starting with <mail>
				if line.split("<subj>")[1].split("</subj>")[0] != "": #checks if <subj> content is non-empty
					for term in re.split("[^A-Za-z0-9\-_]+", re.sub("&.*?;", " ", line.split("<subj>")[1].split("</subj>")[0])): #splits by all chars except [A-Za-z0-9_-], substitutes all instances of &xxx; with space char, splits by <subj> and </subj> to get contents
						if len(term) > 2: #only write to file if the term length is greater than 2
							termsFile.write("s-%s:%s\n" %(term.lower(), line.split("<row>")[1].split("</row>")[0])) #write the term and row id
				if line.split("<body>")[1].split("</body>") != "": #checks if <body> content is non-empty
					for term in re.split("[^A-Za-z0-9\-_]+", re.sub("&.*?;", " ", line.split("<body>")[1].split("</body>")[0])): #splits the same as above for <subj>
						if len(term) > 2: #only write term length > 2
							termsFile.write("b-%s:%s\n" %(term.lower(), line.split("<row>")[1].split("</row>")[0])) #write the term and row id

#This functions write to emails.txt file
def prepEmails(inFile):
	emailsFile = open("emails.txt", "w+") #same as above but for emails.txt
	with open(inFile, 'r') as file: #same as above
		for line in file: #same as above
			if line.startswith("<mail>"): #same as above
				emailsFile.write("from-%s:%s\n" %(line.split("<from>")[1].split("</from>")[0],line.split("<row>")[1].split("</row>")[0])) #write <from> contents into file. No condition since will always have from email
				if line.split("<to>")[1].split("</to>")[0] != "": #checks if <to> content is non-empty
					for email in line.split("<to>")[1].split("</to>")[0].split(","): #for loop to print all emails in <to> split by ','
						emailsFile.write("to-%s:%s\n" %(email,line.split("<row>")[1].split("</row>")[0])) #writes <to> contents and row id to file
				if line.split("<cc>")[1].split("</cc>")[0] != "": #checks if <cc> content is non-empty
					for email in line.split("<cc>")[1].split("</cc>")[0].split(","): #for loop to print all emails in <cc> split by ','
						emailsFile.write("cc-%s:%s\n" %(email,line.split("<row>")[1].split("</row>")[0])) #writes <cc> contents and row id to file
				if line.split("<bcc>")[1].split("</bcc>")[0] != "": #checks if <bcc> content is non-empty
					for email in line.split("<bcc>")[1].split("</bcc>")[0].split(","): #for loop to print all emails in <bcc> split by ','
						emailsFile.write("bcc-%s:%s\n" %(email,line.split("<row>")[1].split("</row>")[0])) #writes <bcc> contents and row id to file
						
def prepDates(inFile):
	datesFile = open("dates.txt", "w+") #same as above but for dates.txt
	with open(inFile, 'r') as file: #same as above
		for line in file: #same as above
			if line.startswith("<mail>"): #same as above
				datesFile.write("%s:%s\n" %(line.split("<date>")[1].split("</date>")[0],line.split("<row>")[1].split("</row>")[0])) #writes <date> content and row id
		
def prepRecs(inFile):
	recsFile = open("recs.txt", "w+") #same as above but for recs.txt
	with open(inFile, 'r') as file: #same as above
		for line in file: #same as above
			if line.startswith("<mail>"): #same as above
				recsFile.write("%s:%s" %(line.split("<row>")[1].split("</row>")[0], line)) #writes row id and full line
		
		
		
		
		
		
		
		
		
		
		