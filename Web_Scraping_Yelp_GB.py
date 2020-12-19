# Web Scraping of Yelp
import bs4 as bs
import urllib.request as url

source = url.urlopen('https://www.yelp.com/search?find_desc=Events&find_loc=Houston%2C%20TX')

page_soup = bs.BeautifulSoup(source, 'html.parser')

# For Main Attributes
mains = page_soup.find_all("div", {"class": "mainAttributes__09f24__26-vh arrange-unit__09f24__1gZC1 arrange-unit-fill__09f24__O6JFU border-color--default__09f24__R1nRO"})
main = mains[0] #First item of mains

#Empty list for main list items
business_name = []
business_url_old = []
business_rating = []
business_reviews = []

#Get Main attributes (business_name, business_rating, business_reviews)
for main in mains:
    try:
        business_name.append(main.find("a").text)
    except:
        business_name.append("")
    try:
        business_url_old.append(main.find("a").get('href'))
    except:
        business_url_old.append("")
    try:
        business_rating.append(main.find("span", {"class": "display--inline__09f24__3iACj border-color--default__09f24__R1nRO"}).div.get('aria-label'))
    except:
        business_rating.append("")
    try:
        business_reviews.append(main.find("span", {"class": "text__09f24__2tZKC reviewCount__09f24__EUXPN text-color--black-extra-light__09f24__38DtK text-align--left__09f24__3Drs0"}).text)
    except:
        business_reviews.append("")

# Loop to concat "https://www.yelp.com"
business_url = []
for i in business_url_old:
    p = 'https://www.yelp.com' + i
    business_url.append(p)

# For Secondary Attributes
secondarys = page_soup.find_all("div", {"class": "secondaryAttributes__09f24__3db5x arrange-unit__09f24__1gZC1 border-color--default__09f24__R1nRO"})
sec = secondarys[0]

#Empty list for secondary list items
business_address = []
phone = []

#Get Secondary attributes (business_address, phone)
for sec in secondarys:
    try:       
        business_address.append(sec.address.find("span", {"class": "raw__09f24__3Obuy"}).text)
    except:
        business_address.append("")
    try:
        phone.append(sec.div.div.text)
    except:
        phone.append("")

#Replace any non-phone numbers with "None"
import re
business_phone = [x if (bool(re.search(r'[(]\d\d\d[)].\d{3}.\d{4}|[(]\d\d[)].\d{4}.\d{3}|\d{4}.\d{3}.\d{3}', x)) == True) else "" for x in phone]

#Save work in excel file
import pandas as pd

data = {}
data = {'business_name': business_name, 'business_rating': business_rating, 'business_url': business_url, 'business_reviews': business_reviews, 'business_address': business_address, 'business_phone': business_phone}
rest = pd.DataFrame(data)
header = ["business_name", "business_url", "business_phone", "business_address", "business_rating", "business_reviews"]

rest.to_excel("Yelp_File.xlsx", columns = header, index = False)

##############################################################################