import requests
from bs4 import BeautifulSoup



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

entryUrl = "https://www.ghanamotion.com" 
r = requests.get(entryUrl)
soup = BeautifulSoup(r.text,"html.parser")

finalmp3links = []
#finalpageLinks will have the original link as part of the list because it is the first page that contain the songs
finalpageLinks = [entryUrl]

finalPageArticles = []
# get the links to all the main pages containing the articles
page_links = soup.find_all('a','page')

for pageLink in page_links:
	finalpageLinks.append(pageLink.attrs['href'])


for finalpageLink in finalpageLinks:
	finalPageArticles.append(getPageArticles(finalpageLink))

allArticles = flattenList(finalPageArticles)

for allArticle in allArticles:
	finalmp3links.append(getMp3Link(allArticle))

print(finalmp3links)

