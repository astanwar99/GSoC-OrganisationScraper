#!/usr/bin/env python
import requests
import sys
from bs4 import BeautifulSoup

url = "https://summerofcode.withgoogle.com/organizations/"
default = "https://summerofcode.withgoogle.com"

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
        print(org)
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
        print(soup)
        print(tags)
        for tag in tags:
            if user_pref in tag.text:
                print ("Name: " + org_name)
                print ("Link: " + org_link)
                print ("No. of times in GSoC: " + str(number + 1) + '\n')
                count += 1

    if count == 0:
        print ("Enter a valid technology name.")

if __name__ == "__main__":
    scrape()