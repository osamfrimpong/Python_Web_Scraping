# Script written by
# Osam-Frimpong Schandorf
# April 19, 2019
# @12:57 am

import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import time


base_dir = os.getcwd()

dir_path = os.path.join(base_dir,"Movies")

if not os.path.exists(dir_path):
	os.mkdir(dir_path)

#isRepeated = false
videoFormat = ["mp4","mkv","avi"]

url = "http://www.lightdl.xyz/2018/05/greys-anatomy.html"

def downloadFile(url):
	name = str(url.split('/')[-1])
	print("Downloading {}".format(url))
	urllib.request.urlretrieve(url,os.path.join(dir_path,name))
	time.sleep(1)

req = requests.get(url)
soup = BeautifulSoup(req.content,'html.parser')
mainDivLinks = soup.find('div','post-body').find_all('a')

finallinks = []

for link in mainDivLinks:
	if link is not None:
		if str(link.attrs['href'].split('.')[-1]) in videoFormat:
			finallinks.append(link.attrs['href'])

for finallink in finallinks[:2]:
	downloadFile(finallink)