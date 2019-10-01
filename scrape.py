#!/usr/bin/env python
import requests
import warnings
from bs4 import BeautifulSoup
import json
from flask import Flask, request

app = Flask(__name__)

#To avoid warning messages 
warnings.filterwarnings("ignore")

#Main function.
@app.route('/genData')
def scrape():
    url = "https://summerofcode.withgoogle.com/archive/2018/organizations/"
    default = "https://summerofcode.withgoogle.com"
    # Create an empty list to store data
    count = 0
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'lxml')
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
        # Create an ampty list tech, We will adding tag.text to it
        tech = []
        for tag in tags:
            tech.append(tag.text)
        
        description_element = soup.find('div', attrs={'class': 'org__long-description'})
        description = description_element.p.text

        mdButton = soup.findAll('md-button', attrs={'class': 'md-primary org__meta-button'})
        contact = "No contact info available"
        for link in mdButton:
            if hasattr(link, 'href'):
                if 'mailto:' in link['href']:
                    contact = link['href']
                
        output_dict = {
            "organization" : org_name,
            "link" : org_link,
            "description" : description,
            "technologies" : tech,
            "contact" : contact
        }
        genData_list.append(output_dict)
        count += 1
        print('Page: ',count)
        #Details for 10 organization - Can be changed for more or less.
        if count == 10:
            return json.dumps(genData_list)


if __name__ == '__main__':
    app.run(debug=True)
