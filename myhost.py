import requests
from bs4 import BeautifulSoup
#from tkinter import *
import Tkinter
import webbrowser
import re

HOSTS_FILE = "C:\Windows\System32\drivers\etc\hosts"
SOURCE_URL = "http://www.360kb.com/kb/2_122.html"
def load_local_hosts():
	mapping = []
	with open(HOSTS_FILE,'r')as f:
		for line in f.readlines():
			line = line.strip()
			if not line or line.startswith("#"):
				continue
			parts = re.split(r'\s+',line)
			mapping.append((parts[0],parts[1]))
	return mapping
def dump_local_hosts(mapping):
	with open(HOSTS_FILE,'w') as f:
		for pair in mapping:
			line = u"%s %s\n" % (pair[0],pair[1])
			f.write(line)
def parse_g_hosts():
	mapping = []
	r = requests.get(SOURCE_URL)
	soup = BeautifulSoup(r.text,"html.parser")
	text = soup.find("pre").string
	lines = text.split('\n')
	for line in lines:
		line = line.strip()
		if line and line[0].isdigit():
			parts = re.split(r'\s+',line)
			print(parts)
			if not len(parts)==2:
				continue
			mapping.append((parts[0],parts[1]))
	return mapping
	
if __name__ == "__main__":
	local_hosts = load_local_hosts()
	g_hosts = parse_g_hosts()
	for pair in g_hosts:
		if pair not in local_hosts:
			local_hosts.append(pair)
	dump_local_hosts(local_hosts)
	print("Done!")