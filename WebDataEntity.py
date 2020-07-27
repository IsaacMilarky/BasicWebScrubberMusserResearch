import requests
import validators
from bs4 import BeautifulSoup
from urllib.parse import urlparse


"""
Created this class to store data from the grabbed html from each website.
Also should store functionality for writing raw data to readable format.
I want to avoid if/else overuse but also make as general as possible.
I think inevitably I need to specify how to scrape for each type of website.
"""

#Uses urllib to check if scheme,netloc and path attributes are all good
#Validates individual URL
def urlValidator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

#Verifyies urls using iteration and application of above method.
def verifyURLS(ListOfURLs):

    fixedList = []

    for url in ListOfURLs:
        if urlValidator(url):
            fixedList.append(url)

    return fixedList


class WebDataEntity:
   
    #Either contructs with a BS object or a direct URL
    def __init__(self, URL):

        #members 
        self._parsedWebText = BeautifulSoup()
        #Isolated tags for html deemed relevant. PUT DESIRED TAGS HERE
        #TODO: make this smarter. td = table data. th = table header. We use table and iterate through subtags
        self._relevantTags = ['table']
        #Isolated strings of tags that are determined to be relevant
        self._relevantEntries = []
        #Isolated links from hypertext found in page
        self._externalLinks = []
        #Rawtext for easy xml writing
        self._csvText = ""

        #initialize if URL is not proper for whatever reason
        if type(URL) is not BeautifulSoup:
            htmlPage = requests.get(URL)
            #print(htmlPage.content)
            #handle screw ups
            try:
                htmlPage.raise_for_status()
            except requests.exceptions.HTTPError as damn:
                print("URL passed to WebDataEntity not deemed valid. See constructor")
                print(damn)
            
            URL = BeautifulSoup(htmlPage.text)
        self._parsedWebText = URL

        self.isolateExternalLinks()
        self.isolateRelevantTags()
        self.convertTagsToCSV()


    #store url of all a tags from html
    def isolateExternalLinks(self):
        for entity in self._parsedWebText.find_all('a'):
            self._externalLinks.append(entity.get('href'))
        #verify that links are resolvable
        self._externalLinks = verifyURLS(self._externalLinks)
    

    #isolates HTML tags such as <table> that are relevant to data collection
    #BeautifulSoup objects have built in functionality to search tags. (thank god) 
    def isolateRelevantTags(self):
        for tag in self._relevantTags:
            for snippet in self._parsedWebText.find_all(tag):
                self._relevantEntries.append(snippet)
                #print(snippet)


    def convertTagsToCSV(self):
        #prevent redundancy by clearing the string
        self._csvText = ""

        """ This part only handles the <table> tags
            this function will be changed to accomodate 
            the various ways in which data is stored in tags.
        """
        #Iterate through each large tag that wraps data
        for parentTag in self._relevantEntries:
            #Iterate through list of rows within a table
            for tableRow in parentTag.find_all('tr'):
                #For all of the strings within an individual row
                for string in tableRow.strings:
                    self._csvText += string + ', '
                self._csvText += '\n'
            self._csvText += '------------------------------------\n'
        #

    #Might want to refractor this. Don't want to drink any chalices
    #Returns a list of WebDataEntities built from the external links of the site.
    def recurseIntoExternalLinks(self, depth = 4):
        externalEntities = []

        for link in self._externalLinks[:depth:]:
            external = WebDataEntity(link)
            externalEntities.append(external)
        return externalEntities



    def getCSVText(self):
        print(self._csvText)
        return self._csvText


    #getters and setters
    def getSoup(self):
        return self._parsedWebText
    
    def getExternals(self):
        return self._externalLinks

    #Print methods.
    def printRelevantSnippets(self):
        for snippet in self._relevantEntries:
            print(snippet.prettify())
            print('\n')

    def printExternals(self):
        for link in self._externalLinks:
            print(link)
            print('\n')