#!/usr/bin/python3
import os
import requests
import validators
from bs4 import BeautifulSoup
from WebDataEntity import WebDataEntity
from WebDataEntity import verifyURLS

#URL is used in every scope but we wont make it global because practice.

def main():
    ScrubURLList = []

    print("Welcome to Isaac's basic web scraper.")
    #I know its weird. URLS use commas as a special character already so...
    #We use the accent or single quote because it can't be represented in a URL.
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

    for x in soupList:
        x.getXMLText()
           


def storeHTMLData(ListOfURLs):
    htmlStorage = []

    #Store all html data in soup object to append into list
    for site in ListOfURLs:
        htmlPage = requests.get(site)
        soup = BeautifulSoup(htmlPage.content, 'html.parser')
        htmlStorage.append(soup)
    
    return htmlStorage
    

                
main()