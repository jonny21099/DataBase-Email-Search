import query as q
import re

#GLOBALS 
keywords = ["subj", "body", "date", "from", "to", "cc", "bcc", "output"] #reserved keywords


def term(condition): #function to match terms in subj/body
	match = re.match("((subj|body)\s*:)?\s*([0-9a-zA-Z_-]+)", condition) #regex to match format of subj/body : term, or a single term. With possibility of % for partial matching
	
	#partial = re.split("(?=%)", match.groups()[2]) <----started partial matching but could not finish
	#print("partial: %s" %partial)
	
	if match.groups()[2] == None:
		return
	if match.groups()[1] == "subj": #if keyword is subj, return term and s-term
		return ["term", "s-%s" %(match.groups()[2])]
	elif match.groups()[1] == "body":  #elif keyword is body, return term and b-term
		return ["term", "b-%s" %(match.groups()[2])]
	elif match.groups()[1] == None: #elif no keyword, return term ,s-term, and b-term. Use '|' to check for OR in query.py
		return ["term", "s-%s" %(match.groups()[2]), "|"],["term", "b-%s" %(match.groups()[2]), "|"]

def dates(condition): #function to match date
	match = re.match("(date)\s*(<=|<|>|>=|:)\s*(\d{4}/\d{2}/\d{2})$", condition) #regex to match format date '<=' or'<' or '>' or '>=' or ':' xxxx/xx/xx
	return [match.groups()[0], match.groups()[2], match.groups()[1]] #return in format [date, xxxx/xx/xx, '<=' or'<' or '>' or '>=' or ':']

def email(condition): #function to match emails in from/to/cc/bcc
	match = re.match("(from|to|cc|bcc)\s*:\s*([0-9a-zA-Z_.-]+@[0-9a-zA-Z_.-]+)",condition) #regex to match format from/to/cc/bcc : alphanum@alphanum, allowing periods in the email
	
	if match.groups()[1] in keywords: #if email is a keyword, return
		return
	if match.groups()[0] == "from": #if keyword is from, return email and from-email
		return ["email", "from-%s" %(match.groups()[1])]
	elif match.groups()[0] == "to": #if keyword is to, return email and to-email
		return ["email", "to-%s" %(match.groups()[1])]
	elif match.groups()[0] == "cc": #if keyword is cc, return email and ccemail
		return ["email", "cc-%s" %(match.groups()[1])]
	elif match.groups()[0] == "bcc": #if keyword is bcc, return email and bcc-email
		return ["email", "bcc-%s" %(match.groups()[1])]

def main():
	output = "brief" #output mode
	while True: #while loop until quit
		conditions = [] #list to pass to query.py
		outputChange = False #checks if output mode haas changed in the iteration
		query = input("\nEnter a query: ").lower() #asks for user input
		if query == "" or query == "quit": #if input is blank or "quit", terminate
			print("Please enter something.")
			return
		condition = re.split("(?<=\w)\s+(?=\w)",query) #regex to split up multiple conditions
		for each in condition: #for each section of a condition
			keyword = re.split("\s*?=<=|<|>|>=|=|:", each) #regex to split keyword and term/email/date
			if keyword[0] in keywords[:2]: #if condition is subj or body then call term() and append to conditions
				#print("SUBJ/BODY")
				conditions.append(term(each))
			elif keyword[0] == keywords[2]: #if condition is date then call date() and append to conditions
				#print("DATE")
				conditions.append(dates(each))
			elif keyword[0] in keywords[3:7]: #if condition is from, to, cc, or bcc call email() and append to conditions
				#print("EMAIL")
				conditions.append(email(each))
			elif keyword[0] == keywords[7]: #if input is output=x
				#print("OUTPUT")
				if output == "brief" and keyword[1] == "full": #if output is brief and x is full, change output mode to full
					output = "full"
					outputChange = True #outputChange to true
				elif output == "full" and keyword[1] == "brief":#if output is full and x is brief, change output mode to brief
					output = "brief"
					outputChange = True #outputChange to true
				break
			else: #anything else is considered a term to search in body and subj
				#print("random term")
				for each2 in term(each): #for each list term() returns (return a list for body and one for subject)
					conditions.append(each2) #append to conditions
		if not outputChange: #if output mode has not changed in current iteration
			q.query(conditions,output) #call query in query.py
main()

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	