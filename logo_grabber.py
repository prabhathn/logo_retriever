import streamlit as st


# FUNCTION DEFINITIONS

def split_input(txt):
    '''Splits the input into a list of domains. No error checking.'''
    return txt.split(',')

def create_url_list(domains):
    '''Converts list of domains into Image URLs
    that pull from the clearbit API'''
     
    prefix = 'https://logo.clearbit.com/'
     
    urls = [prefix + d for d in domains]
    return urls

# MAIN CODE
st.header("Logo Grabber")
st.write("Get logos in bulk for sales decks!")

txt = st.text_area('List of URLs', 'snowflake.com,robling.io', 
                   placeholder='''Type a list of 
                   Company URLs separated by 
                   commas (e.g. snowflake.com,
                   robling.io). Do not put www 
                   in front.''')
    
companies = split_input(txt)
urls = create_url_list(companies)
st.image(image=urls, caption=companies)

st.markdown('[Logos provided by Clearbit](https://clearbit.com)')
st.markdown('Created by [Prabhath Nanisetty](https://www.linked.com/in/prabhathnanisetty). Code at [Github](https://github.com/prabhathn/logo_grabber)')
