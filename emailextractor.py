#!/usr/bin/env python3

import sys
import csv
import re
import os


def collectData(file_path):
	with open(file_path) as f:
		reader = csv.DictReader(f)
		#storing data in a list so we can keep looping over it
		lines = list(reader)
	return lines

def getKeysForCSV(lines):
	line = lines[0]
	keys = line.keys()
	potentialEmailKeys = ['email', 'e-mail', 'e mail']
	potentialNameKeys = ['name', 'first name', 'fname']
	emailKey = None
	nameKey = None
	for key in keys:
		keyLower = key.lower()
		if keyLower in potentialEmailKeys and emailKey == None:
			emailKey = key
			continue
		if keyLower in potentialNameKeys and nameKey == None:
			nameKey = key
			continue

	return nameKey, emailKey

def getEmailsDict(file_path, emailsDict={}):
	lines = collectData(file_path)
	nameKey, emailKey = getKeysForCSV(lines)
	if emailKey == None:
		# TODO:
		#couldn't find an email key, time to resort to just looking for email addresses
		pass
	for line in lines:
		fName = ''
		lName = ''
		if (nameKey in line):
			name = line[nameKey]

			split = name.split(' ', 1)
			#limiting split to 1. We'll assume that everything after the first word
			#is the 'last name'
			#though, that can get messy with middle names, initials, jr, sr,
			#or whatever else might be in a name.
			#You can mostly trust the first name, at least.
			if (len(split) == 1):
				fName = split[0]
				lName = ''
			else:
				fName, lName = split
		email = line[emailKey]
		#only setting first and last names the first time we find an email.
		if email not in emailsDict:
			emailsDict[email] = [fName, lName]

	return emailsDict


def writeCSV(emailsDict, destination_file):

	column_names = ['email', 'First Name', 'Last Name']
	mode = 'w'
	with open(destination_file, mode) as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',',
					quotechar='"', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow(column_names)
		for key, value in emailsDict.items():
			filewriter.writerow([key, value[0], value[1]])


def main():
	dir = './csv/'
	#we'll stick the output on the desktop
	home = os.getenv("HOME")
	path = home + "/desktop"
	destination = path+'/emails.csv'
	#checking for cli arguments, and using the first one as the dir.
	if (len(sys.argv) > 1): dir = " ".join(sys.argv[1:])
	emailsDict = {}
	if dir[-4::] == '.csv':
		#if you drop in a file, instead of a folder, we don't need to loop over it
		file = dir
		emailsDict = getEmailsDict(file, emailsDict)
	else:
		dir = dir.replace('\\', '/') #backslashes before a quote have to be escaped.
		if (dir[-1] != '/'): dir = dir+'/'
		for file in os.listdir(dir):
			if (file[-4:] != '.csv'): continue #skipping non-csv files
			if file[0] == '.': continue #skipping .trashes and such.
			emailsDict = getEmailsDict(dir+file, emailsDict)

	writeCSV(emailsDict, destination)

	print ('Success! ' + str(len(emailsDict)) + ' unique emails stored in emails.csv')


if __name__ == '__main__':
	main()
