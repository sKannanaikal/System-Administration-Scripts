#!/usr/bin/python3

'''
Author: Sean Kannanaikal
Date: 10/18/2021
'''

#Importing necessary modules
import os
import subprocess
import time


#constants for color values
COLORGREEN = '\33[92m'
COLORRED = '\33[91m'
COLOREND = '\33[0m'

#set which will hold all links in the home directory
LINKS = set()

'''
method that will print a welcome message to the tool
'''
def welcome():
	print('\t\t************************************')
	print('\t\t**********'+ COLORGREEN + 'Shortcut Creator'+ COLOREND +'**********')
	print('\t\t************************************\n')

'''
method will clear the terminal
'''
def clearTerminal():
	#running linux command clear
	os.system('clear')

'''
helper method that will end up taking in a src and dest
with those two parameters will end up creating the link
'''
def createLink(src, dest):
	#identifying the actual name of the file
	tokens = src.split('/')
	fname = tokens[len(tokens) - 1]

	#creating the link through a system call
	os.system(f'ln -s {src} {dest}/{fname} 2>/dev/null')

'''
helper method that will end up taking in a src paramter
and then remove the linked file
'''
def deleteLink(src):
	#making system call to remove the file
	os.system(f'rm {src}')

'''
this is a method which will deal with obtaining the source path of a file
after a user types in a file.  It will go ahead and verify that the file exists
and then  return the source if the user agrees
'''
def obtainSource(filetype):
	#welcome message and obtaing source which is parsed to obtain the file name
	welcome()
	source = input("Enter a source: ")
	tokens = source.split('/')
	fname = tokens[len(tokens) -1]

	#this if/elif chain is to determine wheter the check is happening to find a file or find a linkerfile
	if filetype == '-f':
		pipedResults = subprocess.run(["find", "/", "-type" ,filetype, "-name", fname], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
	elif filetype == '-l':
		pipedResults = subprocess.run(["find", "/home/student", "-type" ,"l","-maxdepth", "1", "-name", fname], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

	#once the command is run verify that the output wasn't empty if it was then the file was not found and can stop
	if pipedResults.stdout.decode('utf-8') == '':
		print('Unable to find ' + COLORRED + f'{fname}' + COLOREND + '.')
		return NULL

	#otherwise the output must be dcoded and notify that the file was found
	source = pipedResults.stdout.decode('utf-8').split('\n')[0]
	print('Found ' + COLORGREEN + f'{source}' + COLOREND + '.')

	#verify that the user wants to go ahead and return source and null if the user agrees or disagrees respectively
	userinput = input('Are you sure you want to continue?' + COLORGREEN + '[y/Y]' + COLOREND + '.')
	if userinput.lower() == 'y':
		return source
	elif userinput.lower() != 'y':
		return NULL


def main():
	#clearing the terminal and determining the user's home directory
	clearTerminal()
	destination = os.environ['HOME']
	global LINKS

	#core program loop
	while True:

		#welcome message along with instructions
		welcome()

		print('Enter Selection:')
		print('\t 1 - Create a shortcut in your home directory.')
		print('\t 2 - Remove a shortcut from your home directory.')
		print('\t 3 - Run shortcut report.\n')
		print('Please enter a ' + COLORGREEN + 'number (1-3)' + COLOREND ' or' + COLORGREEN + '"quit"' + COLOREND +' to quit the program.')
		
		#clearing the LINKS set and adding the new entries constantly updating after each command to ensure the linker file records are up to date
		LINKS.clear()
		fileListings = os.listdir()
		for file in fileListings:
			if(os.path.islink(file)):
				LINKS.add(file)
		choice = input("Enter an Option: ")
		
		#clearing ther terminal
		clearTerminal()

		#stop the loop if they enter 'quit'
		if(choice.lower() == 'quit'):
			break

		#if they choose 1 then go ahead and create the link after obtaing source
		elif(choice == '1'):
			#obtain source
			source = obtainSource("-f")
			
			#create the link as long as a file was returned
			if source != NULL:
				createLink(source, destination)

		#if they choose 2 then go ahead and delete the linker file after obtaining the source
		elif(choice == '2'):
			#obtain source
			source = obtainSource("-l")
			
			#delete the linker as long as a file was returned
			if source != NULL:
				deleteLink(source)

		#if they choose 3 provide them with a summary report of all the shortcuts
		elif(choice == '3'):
			#identifying current working directory, the number of links, and a title line for the list of links and paths
			print("Your current directory is " + COLORGREEN + "{}\n".format(os.getcwd()) + COLOREND + '')
			print("The number of links is " + COLORGREEN + "{}\n".format(str(len(LINKS))) + COLOREND + '')
			print(COLORGREEN + "Symbolic Link" + COLOREND + '\t\t\t\t' + COLORGREEN + "Target Path" + COLOREND + ' ')

			#looping through each linkfile in the LINKS set and then identifying the target path and printing each linkfile and targetpath
			for linkfile in LINKS:
				targetpath = os.readlink(linkfile)
				print(f'{linkfile}\t\t\t\t{targetpath}')

			#message to indicate completion
			print("To return to the Main Menu, press Enter.")
			#constantly loop until they hit enter
			while True:
				option = input()
				if option == '':
					break

		time.sleep(3)

#calling main method
if __name__ == '__main__':
	main()
