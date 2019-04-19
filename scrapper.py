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

dir_path = os.path.join(base_dir,"Music")

if not os.path.exists(dir_path):
	os.mkdir(dir_path)

def getPageArticles(pageUrl):
	linklist = []
	page = requests.get(pageUrl)
	soup = BeautifulSoup(page.text,"html.parser")
	articles = soup.find_all('article','item-list')
	for article in articles:
		linklist.append(article.find('a').attrs['href'])
	return linklist

def getMp3Link(articleUrl):
	page = requests.get(articleUrl)
	soup = BeautifulSoup(page.text,"html.parser")
	mp3link = soup.find('a','zbPlayer-download')
	if mp3link is not None:
		rawlink = mp3link.attrs['href']
		return rawlink
	

def flattenList(sources):
	flatList = []
	for source in sources:
		for s in source:
			flatList.append(s)
	return flatList

def downloadFile(url):
	name = str(url.split('/')[-1])
	print("Downloading {}".format(url))
	urllib.request.urlretrieve(url,os.path.join(dir_path,name))
	time.sleep(1)

entryUrl = "https://www.ghanamotion.com/music" 
r = requests.get(entryUrl)
soup = BeautifulSoup(r.text,"html.parser")

# to store all the mp3 links from the articles
finalmp3links = []

#finalpageLinks will have the original link as part of the list because it is the first page that contain the songs
finalpageLinks = [entryUrl]

finalPageArticles = []

# get the links to all the main pages containing the articles
page_links = soup.find_all('a','page')

for pageLink in page_links:
	finalpageLinks.append(pageLink.attrs['href'])

#download only the latest songs
#can restrict the pages to only 1 since the pages are plenty; it's optional though 
for finalpageLink in finalpageLinks[4:6]:
	finalPageArticles.append(getPageArticles(finalpageLink))

#convert list of articles into one single list
allArticles = flattenList(finalPageArticles)

for allArticle in allArticles:
	finalmp3links.append(getMp3Link(allArticle))

#can restrict the links to only 2 since the links may be too much; it's optional though
for finalmp3link in finalmp3links:
	if finalmp3link is not None:
		if downloadFile(finalmp3link):
			print("Successfully downloaded",finalmp3link)
		

