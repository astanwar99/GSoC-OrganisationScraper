#!/usr/bin/env python
import requests
import sys
import warnings
import signal
from bs4 import BeautifulSoup

url = "https://summerofcode.withgoogle.com/archive/2018/organizations/"
default = "https://summerofcode.withgoogle.com"

#To avoid warning messages 
warnings.filterwarnings("ignore")

#Control flow of control through 'Signal' from user.
def signal_handler(signal, frame):
    confirmation = raw_input("Really want to exit (y/n)? ") 
    confirmation.replace(" ", "")
    confirmation = confirmation.lower()
    if confirmation == "y" or confirmation == "yes":
        sys.exit(0)
    else:
        return

signal.signal(signal.SIGINT, signal_handler)

#Main function.
def scrape():
    if(len(sys.argv) == 2):
        user_pref = sys.argv[1]
    else:
        user_pref = raw_input("Enter a technology of preference: " )
   
    user_pref = user_pref.lower()
    user_pref.replace(" ", "")
    count = 0

    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    orgs = soup.findAll('li', attrs={'class': 'organization-card__container'})

    for org in orgs:
        link = org.find('a', attrs={'class': 'organization-card__link'})
        org_name = org['aria-label']
        org_link = default + link['href']
        response = requests.get(org_link)
        html = response.content
        soup = BeautifulSoup(html)
        tags = soup.findAll('li', attrs={
                'class': 'organization__tag organization__tag--technology'
            }
        )
        description_element = soup.find('div', attrs={'class': 'org__long-description'})
        description = description_element.p.text

        mdButton = soup.findAll('md-button', attrs={'class': 'md-primary org__meta-button'})

        contact = "No contact info available"
        for link in mdButton:
            if hasattr(link, 'href'):
                if 'mailto:' in link['href']:
                    contact = link['href']
            

        print ("Name: " + org_name)
        print ("Link: " + org_link)
        print ("Tag: ")
        print ("Description: " + description)
        print (contact)
        for tag in tags:
            print (", " + tag.text)
            count += 1

    if count == 0:
        print ("Enter a valid technology name.")

#Calling scrape().
if __name__ == "__main__":
    scrape()