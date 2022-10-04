import streamlit as st
import requests
import re


# FUNCTION DEFINITIONS

def split_input(txt):
    '''Splits the input into a list of domains. No error checking.'''
    return txt.split(',')

def create_url_list(domains):
    '''Converts list of domains into Image URLs that pull from the clearbit API. If a domain is not provided,
    then try and resolve with Clearbit Autocomplete API.'''
     
    prefix_logo = 'https://logo.clearbit.com/'
    prefix_info = 'https://autocomplete.clearbit.com/v1/companies/suggest?query='
    
    urls = []
    for d in domains:
        if valid_domain(d):
            urls.append((prefix_logo + d, d))
        else:
            # get possible domains
            possible_domains = requests.get(prefix_info + d).json()
            
            # for each domain, append to urls list
            for p in possible_domains:
                urls.append((p.logo, d + ' (guess: ' + p.name + ')'))
            
    return urls
  
def valid_domain(domain):
    '''Check string to determine if it's a valid domain'''
    
    pattern = "^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$"
    return bool(re.match(pattern, domain))


# MAIN CODE
st.header("Logo Grabber")
st.write("Get logos in bulk for sales decks! (Version 1.1)")

txt = st.text_area('List of URLs', 'snowflake.com,robling.io', 
                   placeholder='''Type a list of 
                   Company URLs separated by 
                   commas (e.g. snowflake.com,
                   robling.io). Do not put www 
                   in front.''')
    
companies = split_input(txt)
urls = create_url_list(companies)
st.image(image=urls, caption=companies)

# Credits and Notes
st.markdown('Known issues: No error-checking on text entry, no graceful fail for 404, no grayscaled images, no default sizes for images.')
st.markdown('[Logos provided by Clearbit](https://clearbit.com)')
st.markdown('Created by [Prabhath Nanisetty](https://www.linkedin.com/in/prabhathnanisetty). Code at [Github](https://github.com/prabhathn/logo_grabber)')
