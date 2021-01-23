from bs4 import BeautifulSoup
import methods
import requests
import urllib
import parse
import json
import time
import re

import urllib.request

def uri_exists_get(uri: str) -> bool:
    try:
        response = requests.get(uri)
        try:
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError:
            return False
    except requests.exceptions.ConnectionError:
        return False


main_grade = {}



def main(username, password, link):
    main_grade = {}


    test = "https://" + link + f"/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2fHomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f"
    if uri_exists_get(test) == False:
        return "link_error"

    soup = methods.main(username, password, link)


    
    if re.findall("LogOnDetails.Password", str(soup)) != []:
         return "error"
    classes = soup.findAll("div", {"class": "AssignmentClass"}) 


    main_grade = parse.main(classes)


    return main_grade
