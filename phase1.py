import prepDF as df
import sys
import os

def main():
	print("The file name is: %s" %(sys.argv[1]))
	if sys.argv[1][-4:] != ".xml": #checks that the argument is an xml file
		print("File name does not have .xml extension.")
		return
	inFile = sys.argv[1] #input file is the argument

	#calls preparation files to create output files
	df.prepTerms(inFile)
	df.prepEmails(inFile)
	df.prepDates(inFile)
	df.prepRecs(inFile)
	
	print("Done outputting")
	input("Press Enter to Terminate")
	os.system("cls")
	
main()