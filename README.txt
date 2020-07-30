This program was written by Isaac Milarsky for a summer research course under Dale Musser.

The program functions as a web scraper that downloads table and actuarial data.

The program uses the WebDataEntity class in order to store a beautifulSoup object that stores html data. The WebDataEntity class handles the nitty gritty of the scraper's functionality. The class structure serves to hide away
the meat and potatoes of the class methods from the main program function. The methods include getters and setters along with initial methods called by the constructor to set attributes.

The first set of methods serve to gather the outside websites linked to in the given websites' a tags. The default value of how many links it applies a BeautifulSoup constructor to is 10 but can be made more dynamic through
modification. The program gets the a tags through beautifulSoup letting me use the findAll() method to return a list of all the elements under the html a tags. After these links are validated by a syntax validation method,
BeautifulSoup objects are gathered and returned to the main method in order to scrub that data as well.

The second set of methods that belong to WebDataEntity serve to download the table data presented. The findAll() method from bs4 is used again in order to find relevant <table> html tags to convert into CSV data. Moreover,
the <tr> or table row tag is used to seperate the CSV into readable lines that can be utilized by a spreadsheet program. All of this data is iterated through and makes up the bulk of the computation time. Future optimizations
should look into downloading the raw table text and processing it in C rather than using python where things like pointers are hidden. The final CSV data is added into a string attribute of the WebDataEntity object and is 
seperated by table seperators for easy viewing. 

Additionally, input is recieved through console raw input where the desired URL's are seperated by spaces and split() into a list that in turn converts the data into a WebDataEntity. 

The example websites that I used to test my program are included in the proper text document in this repo. The CSV included is the result of the data that my program scraped from the web. There is a lot of it and most of it is
from the CDC's coronavirus data tables.

Proper syntax for using this program is to run the main.py file with the following syntax: ./main.py <website1> <website2> <website3> etc.

7/29/2020
