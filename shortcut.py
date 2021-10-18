#!/usr/bin/python3

import os

'''
This method will clear the terminal screen whenver it is used
'''

LINKS = set()

def clearTerminal():
	#running linux command clear
	os.system('clear')

def createLink(src, dest):
	os.system(f"ln -s {src} {dest}")

def deleteLink(src):
	pass


def main():
	clearTerminal()
	destination = os.environ['HOME']
	global LINKS
	while True:
		choice = input("Enter an Option: ")
		if(choice.lower() == 'quit'):
			break
		elif(choice == '1'):
			source = input("Enter a source: ")
			#todo find and verify that the file truly exists
			createLink(source, destination)
		elif(choice == '2'):
			source = input("Enter a source: ")
			os.system()
		elif(choice == '3'):
			file_listings = os.listdir()
			for file in file_listings:
				if(os.path.islink(file)):
					LINKS.add(file)

			print("Your current directory is {}".format(os.getcwd()))
			print("The number of links is {}".format(str(len(LINKS))))
			print("Symbolic Link\tTarget Path")
			for linkfile in LINKS:
				print("{}\t{}".format(linkfile, os.system(f'readlink -f {linkfile}')))
			print("To return to the Main Menu, pres Enter. Or select R/r to remove a link")
			while True:
				option = input()
				if option == '':
					break

if __name__ == '__main__':
	main()