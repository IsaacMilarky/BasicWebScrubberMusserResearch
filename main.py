#!/usr/bin/python3
import os
import requests
import validators
from bs4 import BeautifulSoup
from WebDataEntity import WebDataEntity
from WebDataEntity import verifyURLS


def main():
    ScrubURLList = []

    print("Welcome to Isaac's basic web scraper.")
    print("Please input URL(s). If multiple web-pages are desired seperate with spaces")
    
    getTheStringRaw = input()
    ScrubURLList = getTheStringRaw.split()

    #Make sure all URLs can be resolved.
    #Basically just fixes scheme if dumb mistakes are made
    ScrubURLList = verifyURLS(ScrubURLList)

    #creates a new list that converts raw html to a soup object
    #this object is more easy to work with and manipulate via html tags
    soupList = storeHTMLData(ScrubURLList)

    #Good practice method of reassigning all elements as WebDataEntity
    soupList[:] = [WebDataEntity(i) for i in soupList]

    #If you try to do this in a regular for loop then you have an infinite loop :(
    #This is because after you extend the list it keeps going deeper into externals recursively without an endpoint.
    externalSoupObjs = []
    for x in soupList:
        externalSoupObjs.extend(x.recurseIntoExternalLinks())
    soupList.extend(externalSoupObjs)

    #Get data to write to file
    dataStr = ""
    scrapeData = open("scrapeData.csv","a")
    for x in soupList:
        dataStr += x.getCSVText()

    scrapeData.write(dataStr)
    scrapeData.close()
    

def storeHTMLData(ListOfURLs):
    htmlStorage = []

    #Store all html data in soup object to append into list
    for site in ListOfURLs:
        htmlPage = requests.get(site)
        soup = BeautifulSoup(htmlPage.content, 'html.parser')
        htmlStorage.append(soup)
    
    return htmlStorage
                
main()