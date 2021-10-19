#!/usr/bin/python3

import os
import subprocess
'''
This method will clear the terminal screen whenver it is used
'''

LINKS = set()

def clearTerminal():
	#running linux command clear
	os.system('clear')

def createLink(src, dest):
	tokens = src.split('/')
	fname = tokens[len(tokens) - 1]
	os.system(f'ln -s {src} {dest}/{fname} 2>/dev/null')

def deleteLink(src):
	os.system(f'rm {src}')


def main():
	clearTerminal()
	destination = os.environ['HOME']
	global LINKS
	while True:
		LINKS.clear()
		fileListings = os.listdir()
		for file in fileListings:
			if(os.path.islink(file)):
				LINKS.add(file)
		choice = input("Enter an Option: ")
		if(choice.lower() == 'quit'):
			break
		elif(choice == '1'):
			source = input("Enter a source: ")
			tokens = source.split('/')
			fname = tokens[len(tokens) -1]
			pipedResults = subprocess.run(["find", "/", "-type" ,"f", "-name", fname], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
			if pipedResults.stdout.decode('utf-8') == '':
				continue
			print(pipedResults)
			source = pipedResults.stdout.decode('utf-8').split('\n')[0]
			print(source)
			createLink(source, destination)
		elif(choice == '2'):
			source = input("Enter a source: ")
			tokens = source.split('/')
			fname = tokens[len(tokens) -1]
			pipedResults = subprocess.run(["find", "/home/student", "-type" ,"l","-maxdepth", "1", "-name", fname], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
			if pipedResults.stdout.decode('utf-8') == '':
				continue
			source = pipedResults.stdout.decode('utf-8').split('\n')[0]
			deleteLink(source)
		elif(choice == '3'):
			print("Your current directory is {}".format(os.getcwd()))
			print("The number of links is {}".format(str(len(LINKS))))
			print("Symbolic Link\t\t\t\t\t\tTarget Path")
			for linkfile in LINKS:
				targetpath = os.readlink(linkfile)
				print(f'{linkfile}\t\t\t\t\t\t{targetpath}')
			print("To return to the Main Menu, pres Enter. Or select R/r to remove a link")
			while True:
				option = input()
				if option == '':
					break

if __name__ == '__main__':
	main()
