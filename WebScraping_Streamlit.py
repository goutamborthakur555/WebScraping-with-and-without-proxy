# Web Scraping - With Streamlit
import bs4 as bs
import urllib.request as url
import streamlit as st

st.markdown("<h1 style='text-align: center; color: #51cc20;'>Yelp - Web Scraping App</h1>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: #black;'>This app helps you to Scrape Data from Yelp!</h4>", unsafe_allow_html=True)

st.markdown(f'<div style="font-size: small;text-align: right;color: #51cc20;">--By Goutam Borthakur</div>',unsafe_allow_html=True)

st.header("Paste the **yelp website link** below and download data just in a single clicks!")
st.write('Sample link to paste below: www.yelp.com/search?cflt=beaches&find_loc=Los+Angeles%2C+CA')

source = st.text_input("") #www.yelp.com/search?cflt=beaches&find_loc=Los+Angeles%2C+CA

import http
source_txt = http.client.HTTPConnection(source)

submitted = st.button("Submit")
try:
    if submitted:        
        page_soup = bs.BeautifulSoup(source_txt, 'html.parser')
        
        # For Main Attributes
        mains = page_soup.find_all("div", {"class": "mainAttributes__09f24__26-vh arrange-unit__09f24__1gZC1 arrange-unit-fill__09f24__O6JFU border-color--default__09f24__R1nRO"})
        main = mains[0] #First item of mains
        
        #Empty list for main list items
        business_name = []
        business_url_old = []
        business_rating = []
        business_reviews = []
        
        #Get Main attributes (business_name, business_rating, business_reviews)
        for maina in main:
            try:
                business_name.append(maina.find("a").text)
            except:
                business_name.append("")
            try:
                business_url_old.append(maina.find("a").get('href'))
            except:
                business_url_old.append("")
            try:
                business_rating.append(maina.find("span", {"class": "display--inline__09f24__3iACj border-color--default__09f24__R1nRO"}).div.get('aria-label'))
            except:
                business_rating.append("")
            try:
                business_reviews.append(maina.find("span", {"class": "text__09f24__2tZKC reviewCount__09f24__EUXPN text-color--black-extra-light__09f24__38DtK text-align--left__09f24__3Drs0"}).text)
            except:
                business_reviews.append("")
        
        # Loop to concat "https://www.yelp.com"
        business_url = []
        for i in business_url_old:
            p = 'https://www.yelp.com' + i
            business_url.append(p)
        
        # For Secondary Attributes
        secondarys = page_soup.find_all("div", {"class": "secondaryAttributes__09f24__3db5x arrange-unit__09f24__1gZC1 border-color--default__09f24__R1nRO"}) #secondarys
        sec = secondarys[0]
        
        #Empty list for secondary list items
        business_address = []
        phone = []
        
        #Get Secondary attributes (business_address, phone) #secondarys
        for seca in sec:
            try:       
                business_address.append(seca.address.find("span", {"class": "raw__09f24__3Obuy"}).text)
            except:
                business_address.append("")
            try:
                phone.append(seca.div.div.text)
            except:
                phone.append("")
        
        #Replace any non-phone numbers with "None"
        import re
        business_phone = [x if (bool(re.search(r'[(]\d\d\d[)].\d{3}.\d{4}|[(]\d\d[)].\d{4}.\d{3}|\d{4}.\d{3}.\d{3}', x)) == True) else "None" for x in phone]
        
        #Save work in excel file
        import pandas as pd
        
        data = {}
        data = {'business_name': business_name, 'business_rating': business_rating, 'business_url': business_url, 'business_reviews': business_reviews, 'business_address': business_address, 'business_phone': business_phone}
        rest = pd.DataFrame(data)
        header = ["business_name", "business_url", "business_phone", "business_address", "business_rating", "business_reviews"]
        
        st.markdown("<h3 style='text-align: left; color: #33A1FF;'>Your's Scraped Data</h3>", unsafe_allow_html=True)
        st.write(rest)
        
        import base64
        from io import BytesIO
                
        def to_excel(rest):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            rest.to_excel(writer,columns=header,index=False,sheet_name='Sheet1')
            writer.save()
            processed_data = output.getvalue()
            return processed_data
                
        def get_table_download_link(rest):
            val = to_excel(rest)
            b64 = base64.b64encode(val)
            return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Full Scraped File.xlsx">Download Scraped File</a>'
                
        st.markdown(get_table_download_link(rest), unsafe_allow_html=True)
        
except Exception as e:
    st.write("**Error:**",e)
