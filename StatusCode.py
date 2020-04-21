#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor as executor # sudo pip install future
import argparse, requests, sys

yellow = "\033[93m"
green = "\033[92m"
blue = "\033[94m"
red = "\033[91m"
bold = "\033[1m"
end = "\033[0m"


def printer(url):
	sys.stdout.write(url+"                                                                       \r")
	sys.stdout.flush()
	return True

def check(out, url):
	#print("hell")
	printer("Testing: " + url)
	link = 'http://' + url
	try:
		req = requests.head(link, timeout=10)
		length = str(req.headers['Content-Length'])
		scode = str(req.status_code)
		if scode.startswith("2"):
			print(blue+"["+bold+green+str(scode)+end+blue+"]"+end+" | "+str(url)+length)
		elif scode.startswith("3"):
			if req.headers['Location'].startswith("https://"+url):
				print(blue+"["+bold+yellow+str(scode)+end+blue+"]"+end+" | "+str(url)+" - HTTPS | "+length)
			else:
				print(blue+"["+bold+yellow+str(scode)+end+blue+"]"+end+" | "+str(url)+" | "+req.headers['Location']+" | "+length)
		elif scode.startswith("4"):
			print(blue+"["+bold+red+str(scode)+end+blue+"]"+end+" | "+str(url)+" | "+length)
		else:
			print(blue+"["+end+str(scode)+blue+"]"+end+" | "+str(url)+" | "+length)

		if out != 'None':
			with open(out, 'a') as f:
				f.write(str(scode)+" | "+url+" | "+length+"\n")
				f.close()

		return True

	except Exception:
		return False


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-w", "--wordlist", help="Domains List File", type=str, required=True)
	parser.add_argument("-t", "--thread", help="Theads Number - (Default: 10)", type=int)
	parser.add_argument("-o", "--output", help="Save Results In a File", type=str) #action='store_true'

	args = parser.parse_args()

	wlist = str(args.wordlist)
	threads = str(args.thread)
	out = str(args.output)

	if threads == 'None':
		threads = 10
	else:
		threads = threads

	lines = len(open(wlist).readlines())
	print(blue +"["+red+"+"+blue+"] File: " + end + wlist)
	print(blue +"["+red+"+"+blue+"] Length: " + end + str(lines))
	print(blue +"["+red+"+"+blue+"] Threads: " + end + str(threads))
	print(blue +"["+red+"+"+blue+"] Output: " + end + str(out))
	print(red+bold+"\n[+] Results:\n"+end)

	urls = open(wlist, 'r')
	
	with executor(max_workers=int(threads)) as exe:
		[exe.submit(check, out, url.strip('\n')) for url in urls]

if __name__=='__main__':
	main()
